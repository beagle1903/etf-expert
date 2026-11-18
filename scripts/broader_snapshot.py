"""Parse saved venue and catalogue evidence for the broader-coverage pilot."""

from collections import Counter, defaultdict
import csv
from datetime import datetime
from html.parser import HTMLParser
from io import StringIO
import json
import re
from urllib.parse import urljoin, urlsplit


GROUPS = ("US/equity", "US/bond", "EU/equity", "EU/bond")
BOND = re.compile(r"\b(bonds?|treasury|treasuries|muni|municipal|fixed income|TIPS)\b", re.I)
EQUITY = re.compile(r"MSCI|S[&+]P|Russell|STOXX|NASDAQ|DAX|FTSE", re.I)
OTHER = re.compile(r"futures|commodity|commodities|\bVIX\b|\bETN\b|\binverse\b|\bleveraged\b", re.I)
XETRA_ISSUER = re.compile(r"^(?:ISHS|ISHARES|IS C\.)", re.I)
ISIN = re.compile(r"[A-Z]{2}[A-Z0-9]{9}[0-9]")


def table(text, delimiter, required):
    reader = csv.DictReader(StringIO(text), delimiter=delimiter, strict=True)
    if not required <= set(reader.fieldnames or ()):
        raise ValueError("Expected columns missing")
    return reader


def require_row(row, columns, line):
    missing = sorted(column for column in columns if row[column] is None)
    if missing:
        raise ValueError(f"Incomplete source row at line {line}; missing {', '.join(missing)}")


def parse_nasdaq(text):
    columns = {"Symbol", "Security Name", "Listing Exchange", "ETF", "Test Issue", "Nasdaq Traded"}
    raw = table(text, "|", columns)
    rows, date = [], None
    for row in raw:
        first = row["Nasdaq Traded"]
        if first.startswith("File Creation Time:"):
            date = datetime.strptime(first.split(": ", 1)[1], "%m%d%Y%H:%M").isoformat(timespec="minutes")
            continue
        require_row(row, columns, raw.line_num)
        name = row["Security Name"].strip()
        if row["ETF"] != "Y" or row["Test Issue"] != "N" or first != "Y":
            continue
        strategy = None
        if "ishares" in name.casefold() and not OTHER.search(name):
            strategy = "bond" if BOND.search(name) else "equity" if EQUITY.search(name) else None
        rows.append({"market": "US", "venue": row["Listing Exchange"], "symbol": row["Symbol"],
                     "name": name, "strategy": strategy, "currency": None, "isin": None,
                     "source": "nasdaq"})
    if not date or not rows:
        raise ValueError("Expected a populated directory and its file creation time")
    return rows, date


def parse_xetra(text):
    market, timestamp, content = text.split("\n", 2)
    if market.strip() != "Market:;XETR" or not timestamp.startswith("Date Last Update:;"):
        raise ValueError("Expected the XETR reference-file preamble")
    date = datetime.strptime(timestamp.split(";", 1)[1].strip(), "%d.%m.%Y").date().isoformat()
    columns = {"Product Status", "Instrument Status", "Instrument Type", "MIC Code", "Mnemonic",
               "Instrument", "ISIN", "Currency", "Product Assignment Group Description"}
    raw = table(content, ";", columns)
    rows = []
    for row in raw:
        require_row(row, columns, raw.line_num + 2)
        if (row["Instrument Type"], row["MIC Code"], row["Instrument Status"], row["Product Status"]) != (
            "ETF", "XETR", "Active", "Active"
        ):
            continue
        name = row["Instrument"]
        group = row["Product Assignment Group Description"]
        strategy = None
        if XETRA_ISSUER.search(name):
            if group == "EXCHANGE TRADED FUNDS - RENTEN":
                strategy = "bond"
            elif group == "EXCHANGE TRADED FUNDS - PASSIV" and EQUITY.search(name):
                strategy = "equity"
        rows.append({"market": "EU", "venue": "XETR", "symbol": row["Mnemonic"], "name": name,
                     "strategy": strategy, "currency": row["Currency"] or None, "isin": row["ISIN"] or None,
                     "source": "xetra", "venue_group": group})
    if not rows:
        raise ValueError("Expected a populated Xetra ETF snapshot")
    return rows, date


class CatalogueRows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.row = None
        self.cell = None
        self.link = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.row = []
        elif tag in ("th", "td") and self.row is not None:
            self.cell = []
            self.link = None
        elif tag == "a" and self.cell is not None:
            self.link = dict(attrs).get("href")

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag in ("th", "td") and self.cell is not None:
            self.row.append((" ".join("".join(self.cell).split()), self.link))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None


def parse_issuer_us(text, url):
    parser = CatalogueRows()
    parser.feed(text)
    headers = None
    records = defaultdict(list)
    required = {"Ticker", "Name", "Gross Expense Ratio (%)", "Net Expense Ratio (%)"}
    for row in parser.rows:
        values = [value for value, _ in row]
        if required <= set(values):
            headers = values
        elif headers and len(row) == len(headers):
            fields = dict(zip(headers, values))
            link = row[headers.index("Ticker")][1]
            if link and re.fullmatch(r"[A-Z][A-Z0-9.-]*", fields["Ticker"]):
                entry = {k: fields[k] for k in ("Name", "Gross Expense Ratio (%)", "Net Expense Ratio (%)")}
                entry["product_url"] = urljoin(url, link)
                if entry not in records[fields["Ticker"]]:
                    records[fields["Ticker"]].append(entry)
    if not records:
        raise ValueError("No US catalogue rows matched the expected fee table")
    return dict(records), None


def parse_sec(text):
    columns = {"Class Ticker", "Class ID", "Series ID"}
    records = defaultdict(list)
    raw = table(text, ",", columns)
    for row in raw:
        require_row(row, columns, raw.line_num)
        ticker = row["Class Ticker"].strip()
        if ticker and re.fullmatch(r"C\d{9}", row["Class ID"]) and re.fullmatch(r"S\d{9}", row["Series ID"]):
            item = {key: row[key] for key in ("Class ID", "Series ID")}
            if item not in records[ticker]:
                records[ticker].append(item)
    if not records:
        raise ValueError("No tagged series/class rows")
    return dict(records), "2026-06-01"


def parse_danimoth(text):
    columns = {"isin", "provider", "name", "index_name", "investment_focus", "asset_class", "ter", "is_hedged",
               "number_of_holdings", "snapshot_date", "scraped_at", "source_backend", "source_url"}
    records = defaultdict(list)
    dates = set()
    raw = table(text, ",", columns)
    for row in raw:
        require_row(row, columns, raw.line_num)
        entry = {k: row[k] for k in sorted(columns)}
        if ISIN.fullmatch(row["isin"]):
            records[row["isin"]].append(entry)
            dates.add(row["snapshot_date"])
    if not records:
        raise ValueError("No ISIN rows in the published snapshot")
    return dict(records), ", ".join(sorted(dates))


def review_german_catalogue(text):
    page = CatalogueRows()
    page.feed(text)
    if not page.rows:
        raise ValueError("No fund rows in the saved German catalogue response")
    raise ValueError("German catalogue table requires an explicit ISIN/field mapping")


def parse_product_data(text):
    document = json.loads(text)
    if not isinstance(document, dict) or not document.get("data"):
        raise ValueError("Published product-data response returned empty data")
    raise ValueError("Product-data payload has no supported field mapping")


def parse_issuer_screener(text, market):
    document = json.loads(text)
    if not isinstance(document, dict) or not document or not all(
        re.fullmatch(r"\d+", key) and isinstance(row, dict) for key, row in document.items()
    ):
        raise ValueError("Expected a populated issuer screener keyed by product number")
    fields = ("isin", "cusip", "localExchangeTicker", "fundName", "productPageUrl", "aladdinAssetClass",
              "aladdinSubAssetClass", "aladdinRegion", "fees", "netr", "ter", "effectiveDuration",
              "modelOad", "seriesBaseCurrencyCode")
    records = defaultdict(list)
    for product_id, row in document.items():
        if row.get("productType") != "ISHARES_FUND_DATA" or "etf" not in (row.get("productView") or ()):
            continue
        isin = row.get("isin")
        key = row.get("localExchangeTicker") if market == "US" else isin
        if not isinstance(isin, str) or not ISIN.fullmatch(isin) or not isinstance(key, str) or not key:
            continue
        if market == "US" and not isin.startswith("US"):
            continue
        records[key].append({"product_id": product_id, **{name: row.get(name) for name in fields}})
    if not records:
        raise ValueError("No attributable ETF identifiers in issuer screener")
    # The feed has dates for various market observations. It supplies no
    # field date for its expense ratios or effective duration.
    return dict(records), None


PARSERS = {
    "nasdaq": parse_nasdaq, "xetra": parse_xetra, "sec": parse_sec, "danimoth": parse_danimoth,
    "ishares-de": review_german_catalogue, "ishares-de-legacy": review_german_catalogue,
    "ishares-de-data": parse_product_data, "ishares-us-data": parse_product_data,
    "ishares-de-screener": lambda text: parse_issuer_screener(text, "EU"),
    "ishares-us-screener": lambda text: parse_issuer_screener(text, "US"),
}


def select_candidates(venues, baseline, per_group):
    scoped = defaultdict(list)
    excluded = Counter()
    for row in venues:
        strategy = row["strategy"]
        if strategy is None:
            excluded["outside_issuer_and_strategy_filters"] += 1
            continue
        baseline_symbol = row["symbol"] + ".DE" if row["market"] == "EU" else row["symbol"]
        if baseline_symbol in baseline:
            excluded["original_symbol"] += 1
            continue
        scoped[f"{row['market']}/{strategy}"].append(row)
    candidates, counts = [], {}
    for group in GROUPS:
        ordered = sorted(scoped[group], key=lambda r: (r["symbol"], r["venue"], r["currency"] or "", r["isin"] or ""))
        distinct, seen = [], set()
        for row in ordered:
            key = row["isin"] or row["symbol"]
            if key in seen:
                excluded["duplicate_class_or_symbol_within_group"] += 1
                continue
            distinct.append(row)
            seen.add(key)
        selected = distinct[:per_group]
        excluded["outside_pilot_quota"] += len(distinct) - len(selected)
        counts[group] = {"target": per_group, "scope_matches": len(ordered), "requested": len(selected),
                         "shortfall": per_group - len(selected)}
        candidates.extend(selected)
    return candidates, counts, dict(excluded)


def research(listing, parsed, sources, attempted_sources):
    us = listing["market"] == "US"
    symbol, isin = listing["symbol"], listing["isin"]
    candidates = parsed.get("ishares-us", {}).get(symbol, []) if us else parsed.get("danimoth", {}).get(isin, [])
    issuer_source = "ishares-us" if us else "danimoth"
    matches = [row for row in candidates if us or row["provider"].casefold().strip() == "ishares"]
    facts = {}
    issues = []
    if len(matches) == 1:
        facts[issuer_source] = matches[0]
    elif len(matches) > 1:
        issues.append("multiple_catalogue_matches")
    else:
        issues.append("no_attributable_catalogue_row")
    if candidates and len(matches) != 1:
        facts["unresolved_catalogue_candidates"] = candidates
    if not us and issuer_source in facts and facts[issuer_source]["asset_class"] != listing["strategy"]:
        issues.append("catalogue_and_venue_strategy_disagree")

    screener_source = "ishares-us-screener" if us else "ishares-de-screener"
    screener_rows = parsed.get(screener_source, {}).get(symbol if us else isin, [])
    matched = screener_rows
    if us and screener_rows:
        catalogue_url = facts.get("ishares-us", {}).get("product_url", "")
        product = re.match(r"^/us/products/(\d+)(?:/|$)", urlsplit(catalogue_url).path)
        matched = [row for row in screener_rows if product and row["product_id"] == product[1]]
    if len(matched) == 1:
        facts[screener_source] = matched[0]
        expected_class = {
            ("US", "equity"): "Equity", ("US", "bond"): "Fixed Income",
            ("EU", "equity"): "Aktien", ("EU", "bond"): "Anleihen",
        }[(listing["market"], listing["strategy"])]
        if matched[0]["aladdinAssetClass"] != expected_class:
            issues.append("issuer_screener_and_venue_strategy_disagree")
    elif screener_rows:
        facts["unresolved_screener_candidates"] = screener_rows
        issues.append("ambiguous_or_unattributed_issuer_screener_match")
    elif screener_source in attempted_sources:
        issues.append("no_attributable_issuer_screener_row")

    # SEC identifiers corroborate the symbol only if the published join is unique.
    sec = parsed.get("sec", {}).get(symbol, []) if us else []
    if len(sec) == 1:
        facts["sec"] = sec[0]
    elif len(sec) > 1:
        facts["unresolved_sec_candidates"] = sec
        issues.append("multiple_sec_matches")

    venue_source = sources[listing["source"]]
    class_key = None
    if not us and isin and ISIN.fullmatch(isin):
        class_key = f"ISIN:{isin}"
    if us and screener_source in facts:
        class_key = f"ISIN:{facts[screener_source]['isin']}"
    elif us and "sec" in facts:
        class_key = f"SEC_CLASS:{facts['sec']['Class ID']}"

    required = {
        "listing_venue": bool(listing["venue"]),
        "share_class_identity": bool(class_key),
        "trading_currency": bool(listing["currency"]),
        # None of the supported bulk catalogues supplies a fee-effective/observation date.
        "dated_annual_fee": False,
        "exposure_description": bool(facts.get("danimoth", {}).get("index_name")),
    }
    if listing["strategy"] == "bond":
        required.update(dated_duration=False, dated_credit=False)
    issues.extend(f"missing:{name}" for name, known in required.items() if not known)
    research_sources = {"ishares-us", "ishares-us-data", "sec"} if us else {
        "ishares-de", "ishares-de-legacy", "ishares-de-data", "danimoth"
    }
    research_sources.add(screener_source)
    return {
        "listing": listing, "listing_source_date": venue_source["source_date"], "share_class_key": class_key,
        "facts": facts,
        "research_attempted": bool(research_sources & attempted_sources),
        "research_collected": any(key in facts for key in (issuer_source, screener_source, "sec")),
        "normalized": True,
        "unresolved": not all(required.values()) or bool(issues),
        "comparison_ready": all(required.values()) and not issues,
        "required_evidence": required, "issues": issues,
    }
