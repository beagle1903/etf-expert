"""Replay saved issuer responses into a conservative field-availability report.

No network access. Values are source claims, not verified legal identities.
"""
import argparse
from datetime import datetime
from html import unescape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ('identifier', 'legal_entity', 'benchmark', 'benchmark_ticker', 'fee', 'net_assets', 'share_assets', 'base_currency', 'share_currency',
          'hedging', 'distribution', 'composition', 'duration', 'maturity', 'yield', 'credit_quality')


def clean(text):
    return ' '.join(text.replace('\ufffe', '-').replace('\x02', '-').split())


def date(value):
    for fmt in ('%d-%b-%Y', '%d %B %Y', '%B %d, %Y', '%m/%d/%Y'):
        try:
            return datetime.strptime(value.strip(), fmt).date().isoformat()
        except ValueError:
            pass
    return None


def match(pattern, text):
    found = re.search(pattern, text, re.I)
    return found.group(1).strip() if found else None


def bond_applicability(intent):
    """Sample intention only; unknown never means equity non-applicability."""
    if not isinstance(intent, str):
        return None
    if re.search(r'\bbonds?\b|\btreasur(?:y|ies)\b', intent, re.I):
        return True
    if re.search(r'\bequity\b', intent, re.I):
        return False
    return None


def parse(text, symbol, url):
    text = clean(text)
    fields = {name: None for name in FIELDS}
    result = {'fields': fields, 'source_dates': {}, 'listing_evidence': None,
              'header': text[:260], 'warnings': []}
    eu_ishares = 'ishares.com' in url and 'UCITS ETF' in text[:250]
    us_vanguard = 'fund-docs.vanguard.com/F' in url and 'UCITS' not in text[:250]
    eu_vanguard = 'fund-docs.vanguard.com/' in url and not us_vanguard
    # Dates are deliberately separate; a document date never overwrites a section date.
    d = match(r'(?:Factsheet\s*\||Fact Sheet as of|As of)\s*([A-Za-z]+ \d{1,2}, \d{4}|\d{1,2} [A-Za-z]+ \d{4}|\d{2}/\d{2}/\d{4})', text)
    result['source_dates']['document'] = date(d) if d else None
    d = match(r'information as at:\s*(\d{2}-[A-Za-z]{3}-\d{4})', text)
    result['source_dates']['composition'] = date(d) if d else result['source_dates']['document']
    d = match(r'All other data as at\s*(\d{2}-[A-Za-z]{3}-\d{4})', text)
    result['source_dates']['other'] = date(d) if d else result['source_dates']['document']
    # Keep all explicit section-date statements, including inconsistent ones.
    result['source_dates']['statements'] = re.findall(r'(?:Data as at|data as at|as at:)\s*\d{1,2}[- ][A-Za-z]+[- ]\d{4}', text)
    def put(field, value, unit=None, as_of=None):
        if value is not None:
            fields[field] = {'value': value, 'unit': unit, 'as_of': as_of}
    found_id = re.search(r'\b((?:IE|DE)[A-Z0-9]{8}[0-9]{2})\b', text)
    identifier = found_id[1] if found_id else None
    if identifier:
        put('identifier', identifier, 'ISIN', result['source_dates']['other'])
    else:
        put('identifier', match(r'CUSIP(?: number)?\s*:?\s*([A-Z0-9]{9})\b', text), 'CUSIP', result['source_dates']['other'])
    # Colon-delimited iShares data are constrained by the next known label.
    if 'ishares.com' in url:
        put('legal_entity', match(r'Issuing Company\s*:\s*(.*?)\s+Product Structure', text), as_of=result['source_dates']['other'])
        put('net_assets', match(r'Net Assets of Fund \(M\)\s*:\s*(\$[\d,.]+|[\d,.]+(?:\s+(?:USD|EUR|GBP|CHF|JPY|CAD|AUD)\b)?)', text), 'million; currency as printed, $ not silently treated as USD', result['source_dates']['composition'])
        put('share_assets', match(r'Net Assets of Share Class \(M\)\s*:\s*([\d,.]+\s+[A-Z]{3})', text), 'million; share class', result['source_dates']['composition'])
        put('benchmark', match(r'Benchmark\s*:\s*(.*?)\s+Fund Launch Date', text), as_of=result['source_dates']['other'])
        put('share_currency', match(r'Share Class Currency\s*:\s*([A-Z]{3})', text), as_of=result['source_dates']['other'])
        put('base_currency', match(r'Fund Base Currency\s*:\s*([A-Z]{3})', text), as_of=result['source_dates']['other'])
        put('distribution', match(r'Use of Income\s*:\s*(Accumulating|Distributing)', text), as_of=result['source_dates']['other'])
        freq = match(r'Distribution Frequency\s*:\s*(.*?)\s+(?:Net Assets|CUSIP)', text)
        if freq:
            put('distribution', ((fields['distribution']['value'] + '; ') if fields['distribution'] else '') + freq, as_of=result['source_dates']['other'])
    if us_vanguard:
        put('net_assets', match(r'Fund total net assets (\$[\d,]+ million)', text), 'USD million ($ source notation)', result['source_dates']['document'])
        put('share_assets', match(r'ETF total net assets (\$[\d,]+ million)', text), 'USD million; ETF shares, not whole fund', result['source_dates']['document'])
        put('benchmark', match(r'Quick facts Benchmark (.*?) Expense ratio', text), as_of=result['source_dates']['other'])
        put('benchmark_ticker', match(r'Index ticker \(Bloomberg\) ([A-Z0-9]+)', text), 'Bloomberg', result['source_dates']['other'])
        put('distribution', match(r'Dividend schedule (.*?) ETF total net assets', text), as_of=result['source_dates']['other'])
    if eu_vanguard:
        put('legal_entity', match(r'(Vanguard Funds plc)\s+Physical', text), as_of=result['source_dates']['other'])
        put('net_assets', match(r'Total assets \(million\) ([€$][\d,]+)', text), 'million; currency symbol as printed', result['source_dates']['other'])
        put('share_assets', match(r'Share class assets \(million\) ([€$][\d,]+)', text), 'million; share class, currency symbol as printed', result['source_dates']['other'])
        put('benchmark', match(r'Benchmark\s*[—–-]\s*(.*?)\s*(?:Annualised| - The Index)', text), as_of=result['source_dates']['other'])
        put('base_currency', match(r'Base currency.*?Domicile\s+([A-Z]{3})\b', text), as_of=result['source_dates']['other'])
        put('share_currency', match(r'(USD|EUR)\)?\s+(?:Hedged )?Accumulating', text), as_of=result['source_dates']['other'])
        put('distribution', match(r'\b(Accumulated)\b', text), as_of=result['source_dates']['other'])
    if 'ssga.com' in url:
        put('benchmark', match(r'performance of the (S&P 500[^®]*?®? Index)', text))
    fee = re.search(r'(Ongoing Charges Figure[^0-9]{0,4}|Total Expense Ratio\s*:?\s*|Expense ratio\s*1?\s*)(\d+(?:\.\d+)?)%', text, re.I)
    if fee:
        put('fee', float(fee[2]), 'percent per year; ' + clean(fee[1]), result['source_dates']['other'])
        fields['fee']['raw_text'] = fee[0]
    elif 'ssga.com' in url:
        value = match(r'Gross Expense Ratio \(%\) (\d+(?:\.\d+)?)', text)
        put('fee', float(value) if value else None, 'percent per year; gross expense ratio')
        if fields['fee']:
            fields['fee']['raw_text'] = f'Gross Expense Ratio (%) {value}'
    if 'Hedged' in text[:250]:
        put('hedging', 'EUR hedged' if re.search(r'(EUR Hedged|Hedged Euro)', text[:250]) else 'hedged; target unresolved', as_of=result['source_dates']['other'])
    # Absence of the word hedged is not evidence of unhedged status.
    for field, pattern in {
        'duration': r'((?:Effective Duration|Average duration)\s*:?\s*(?:5 )?\d+(?:\.\d+)?\s*(?:yrs|years))',
        'maturity': r'((?:Average Weighted Maturity|Weighted Avg Maturity|Average maturity|Average effective maturity)\s*:?\s*(?:6 )?\d+(?:\.\d+)?\s*(?:yrs|years))',
        'yield': r'((?:Yield to worst|Weighted Avg YTM|30 Day SEC Yield)\s*:?\s*-?\d+(?:\.\d+)?%?)',
        'credit_quality': r'(Average quality\s+[A-Z]{1,3}[+-]?)',
    }.items():
        put(field, match(pattern, text), 'years' if field in ('duration', 'maturity') else 'source label; yield unit unresolved if % absent' if field == 'yield' else 'rating', result['source_dates']['other'] if eu_ishares else result['source_dates']['composition'])
    # A numeric top-position / issuer or allocation is evidence of partial composition.
    comp = match(r'((?:TOP HOLDINGS \(%\)|Top 10 holdings|TOP ISSUERS).*?)\s*(?:Holdings (?:are )?subject|Data as at|SECTOR BREAKDOWN|Characteristics Fund)', text)
    if comp and re.search(r'\d+(?:\.\d+)?%', comp):
        put('composition', comp[:1600], 'partial weights in percent; never complete overlap', result['source_dates']['composition'])
    if us_vanguard:
        comp = match(r'((?:Ten\s*largest holdings|Distribution by credit quality|Distribution by issuer|Distibution by effective maturity).*?)\s*(?:1\.|Vanguard Marketing)', text)
        if comp and re.search(r'\d+(?:\.\d+)?\s*%', comp):
            put('composition', comp[:1600], 'partial holdings or aggregate weights in percent', result['source_dates']['composition'])
        credit = match(r'(Distribution by credit quality.*?)\s+Portfolio management', text)
        if credit and re.search(r'AAA\s+\d+(?:\.\d+)?\s*%', credit):
            put('credit_quality', credit, 'rating bucket weights in percent', result['source_dates']['composition'])
    if eu_vanguard and symbol == 'VAGF.DE':
        comp = match(r'(Market allocation.*?)\s+Distribution by credit maturity', text)
        if comp and re.search(r'\d+(?:\.\d+)?%', comp):
            put('composition', comp[:1600], 'aggregate market weights in percent', None)
    if 'ssga.com' in url:
        comp = match(r'(Top 10 Holdings.*?)(?:‡ Subject|Sector weights)', text)
        if comp and re.search(r'\d+\.\d+', comp):
            put('composition', comp, 'partial holdings; Weight (%) table', result['source_dates']['document'])
        if fields['fee']:
            fields['fee']['as_of'] = result['source_dates']['document']
        result['listing_evidence'] = 'Manual header review required: ticker is graphical; CUSIP extracted'
    credit = match(r'(CREDIT (?:RATINGS|QUALITY) \(%\).*?)\s+Credit quality ratings', text)
    if credit and re.search(r'(?:Rated|AAA|BBB).*?\d+\.\d+', credit):
        put('credit_quality', credit[:1000], 'rating bucket weights in percent', result['source_dates']['composition'])
    if '.' in symbol and re.search(r'(?<![\w.])' + re.escape(symbol) + r'(?![\w.])', text):
        result['listing_evidence'] = 'Exact listing code appears in issuer document: ' + symbol
        result['listing_match'] = 'exact_code'
    elif '.' not in symbol and re.search(r'\b' + re.escape(symbol) + r'\b', text[:300]):
        result['listing_evidence'] = 'US ticker header plus source identifier; no exchange-independent legal verification'
        result['listing_match'] = 'ticker_only'
    elif not result['listing_evidence']:
        result['warnings'].append('Exact Yahoo listing code absent; review issuer ticker, exchange and currency table. No automatic identity match.')
    if 'CREDIT RATINGS (%)' in text and not fields['credit_quality']:
        result['warnings'].append('Credit chart exists; numeric rating weights not recovered by text extractor. Manual/chart or separate download route needed.')
    if eu_vanguard:
        stated_dates = {date(re.sub(r'^.*?(\d)', r'\1', statement)) for statement in result['source_dates']['statements']}
        stated_dates.discard(None)
        if len(stated_dates) > 1:
            result['warnings'].append('Conflicting section dates; do not assign the document date to every characteristic. See dated assessment and raw PDF.')
            for field in ('duration', 'maturity', 'yield', 'credit_quality'):
                if fields[field]:
                    fields[field]['as_of'] = None
                    fields[field]['date_status'] = 'conflicting'
            if symbol == 'VAGF.DE' and fields['composition']:
                fields['composition']['date_status'] = 'conflicting'
    if us_vanguard and fields['fee']:
        fields['fee']['as_of'] = None
        result['warnings'].append('Fee refers to most recent prospectus; effective date not established by factsheet date.')
    if eu_ishares and fields['yield'] and '%' not in fields['yield']['value']:
        result['warnings'].append('Yield to Worst lacks a printed % sign in extracted value; retained raw, not normalized against YTM/SEC yield.')
    listing = match(r'(TRADING INFORMATION.*?)\s*(?:This product is also listed|MATURITY BREAKDOWN|GEOGRAPHIC BREAKDOWN)', text)
    if listing:
        result['listing_table'] = listing
        ric = match(r'RIC (.*?) SEDOL', listing)
        currencies = match(r'Listing Currency ((?:[A-Z]{3}\s*)+)', listing)
        if ric and currencies:
            codes, units = ric.split(), currencies.split()
            if len(codes) == len(units) and symbol in codes:
                result['listing_currency'] = units[codes.index(symbol)]
    return result


def parse_product(html):
    """QQQ fallback: only explicit JSON-LD properties, never inferred page values."""
    fields = dict.fromkeys(FIELDS)
    properties = {}
    for block in re.findall(r'<script[^>]*type=[\"\x27]application/ld\+json[\"\x27][^>]*>(.*?)</script>', html, re.S | re.I):
        try:
            doc = json.loads(unescape(block))
        except json.JSONDecodeError:
            continue
        def visit(node):
            if isinstance(node, dict):
                if 'propertyID' in node and 'value' in node:
                    properties[node['propertyID']] = node['value']
                for value in node.values():
                    visit(value)
            elif isinstance(node, list):
                for value in node:
                    visit(value)
        visit(doc)
    value = properties.get('ISIN')
    if value and re.fullmatch(r'US[A-Z0-9]{8}[0-9]{2}', value):
        fields['identifier'] = {'value':value, 'unit':'ISIN', 'as_of':None}
    return {'fields':fields, 'source_dates':{}, 'header':str(properties.get('Share class full name', 'QQQ product page JSON-LD')),
            'listing_evidence':'Product JSON-LD ticker QQQ; exchange and source observation date unresolved' if properties.get('Ticker')=='QQQ' else None,
            'listing_match':'ticker_only' if properties.get('Ticker')=='QQQ' else 'unresolved',
            'warnings':['Factsheet links returned HTML. Fallback only recovers explicit structured identity. Dynamic fee, holdings, currencies and distribution remain unresolved in this route.']}


def report(rows, attempts):
    observed = max(a['collected_at_utc'] for a in attempts)[:10] if attempts else 'no collection'
    lines = ['# Official issuer field coverage — '+observed, '',
             'Saved-response replay. Source claims only; no eligibility, complete identity or overlap validation. Missing is unresolved, never zero. All 24 original listings remain in the denominator.', '',
             '| Field recovered | US / 12 | EU / 12 |', '|---|---:|---:|']
    for field in FIELDS:
        lines.append('| '+field+' | '+' | '.join(str(sum(r['fields'][field] is not None for r in rows if r['market']==m)) for m in ('US','EU'))+' |')
    lines += ['', 'Counts measure extracted fields, including undated values and source candidates with unresolved listing matches. Read each record before attributing facts. Duration, maturity and credit are applicable to five bond sample intentions per market; equity absence is not an exclusion.', '']
    for row in rows:
        lines += ['## '+row['symbol'], '', 'Source: '+(f"[issuer document]({row['url']})" if row.get('url') else 'No parsed PDF'), '',
                  'Collected UTC: '+str(row.get('collected_at_utc')), '',
                  'Source dates: `'+json.dumps(row.get('source_dates', {}))+'`', '',
                  'Listing: '+str(row.get('listing_evidence') or 'Unresolved'), '',
                  'Automatically mapped listing currency: '+str(row.get('listing_currency') or 'unresolved; see source table/manual assessment'), '',
                  'Header: '+row.get('header', 'Missing'), '',
                  '| Field | Source value | Unit / scope | Observation date |', '|---|---|---|---|']
        for field,value in row['fields'].items():
            applicable = row.get('bond_measures_applicable', bond_applicability(row.get('intent')))
            absent = 'Not applicable to equity sample intention' if field in ('duration','maturity','credit_quality') and applicable is False else 'MISSING / unresolved'
            cells = [str(value['value']), str(value['unit'] or ''), str(value['as_of'] or 'unresolved')] if value else [absent, '', '']
            lines.append('| '+field+' | '+' | '.join(c.replace('|','/').replace('\n',' ') for c in cells)+' |')
        lines += ['', *['- '+w for w in row.get('warnings', [])], '', 'Attempts:', '']
        for a in attempts:
            if a['symbol']==row['symbol']:
                lines.append(f"- [{a['kind']}]({a['url']}) — {a['collected_at_utc']}; HTTP {a.get('status')}; {a.get('error') or 'saved'}; raw `{a['run']}/{a.get('raw_file', 'none')}`")
        lines += ['']
    return '\n'.join(line.rstrip() for line in lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('runs', nargs='+', type=Path, help='Saved run folders in collection order')
    parser.add_argument('--output', type=Path, required=True, help='Report path; paired JSON stays alongside it')
    args = parser.parse_args()
    attempts, selected, observations = [], {}, []
    universe = json.loads((args.runs[0]/'universe.json').read_text(encoding='utf-8'))
    for folder in args.runs:
        if json.loads((folder/'universe.json').read_text(encoding='utf-8')) != universe:
            raise ValueError('Run universe snapshots differ; do not silently merge different samples')
        for a in json.loads((folder/'collection.json').read_text(encoding='utf-8'))['results']:
            attempts.append({**a, 'run': folder.name})
            parsed = None
            if a['kind']=='factsheet' and not a['error'] and a.get('text_file'):
                parsed = parse((folder/a['text_file']).read_text(encoding='utf-8'), a['symbol'], a['url'])
            elif a['symbol']=='QQQ' and a['kind']=='product' and not a['error']:
                parsed = parse_product((folder/a['raw_file']).read_text(encoding='utf-8'))
            if parsed is not None:
                evidence = {**parsed, 'url': a['url'], 'collected_at_utc': a['collected_at_utc'], 'kind': a['kind']}
                observations.append({**evidence, 'symbol': a['symbol'], 'attempt_index': len(attempts) - 1})
                if a['kind'] == 'factsheet' or selected.get(a['symbol'], {}).get('kind') != 'factsheet':
                    selected[a['symbol']] = evidence
    rows = [{**member, **selected.get(member['symbol'], {'fields':dict.fromkeys(FIELDS), 'warnings':['No parsed factsheet; product-page fallback requires separate review.']})} for member in universe]
    for row in rows:
        row['bond_measures_applicable'] = bond_applicability(row.get('intent'))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report(rows, attempts), encoding='utf-8')
    args.output.with_suffix('.json').write_text(json.dumps(
        {'rows':rows, 'attempts':attempts, 'observations':observations}, indent=2), encoding='utf-8')
    print(args.output)


if __name__ == '__main__':
    main()
