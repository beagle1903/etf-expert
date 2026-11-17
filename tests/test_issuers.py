import importlib.util
import json
from pathlib import Path
import sys

def module(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).parents[1] / 'scripts' / (name+'.py'))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


assess = module('assess_issuers')
collect = module('check_issuers')


def test_dates_are_field_specific_and_fee_stays_percent():
    text = '''iShares Example UCITS ETF EUR Hedged
    Performance, Portfolio Breakdowns and Net Asset information as at: 31-Oct-2026.
    All other data as at 06-Nov-2026.
    ISIN : IE00BDBRDM35 Share Class Currency : EUR Total Expense Ratio : 0.10%
    Benchmark : Example Index Fund Launch Date : 21-Nov-2017
    Effective Duration : 6.06 yrs TOP ISSUERS Example 20.00% Holdings subject to change.'''
    r = assess.parse(text, 'EUNA.DE', 'https://www.ishares.com/example.pdf')
    assert r['fields']['fee']['value'] == 0.10  # not 10%, and not a decimal fraction
    assert r['fields']['fee']['as_of'] == '2026-11-06'
    assert r['fields']['duration']['as_of'] == '2026-11-06'
    assert r['fields']['composition']['as_of'] == '2026-10-31'
    assert r['listing_evidence'] is None
    spy = assess.parse('CUSIP 78462F103 Gross Expense Ratio (%) 0.0945 As of 09/30/2026', 'SPY', 'https://www.ssga.com/spy.pdf')
    assert spy['fields']['fee']['value'] == 0.0945
    assert spy['fields']['fee']['as_of'] == '2026-09-30'


def test_prose_is_not_an_identifier_and_missing_hedging_is_not_unhedged():
    r = assess.parse('IWM developments KEY FACTS CUSIP : 464287655 Expense Ratio 0.00%', 'IWM', 'https://www.ishares.com/example.pdf')
    assert r['fields']['identifier']['value'] == '464287655'
    assert r['fields']['fee']['value'] == 0
    assert r['fields']['hedging'] is None
    assert assess.parse('No facts', 'X', 'https://www.ishares.com/example.pdf')['fields']['fee'] is None


def test_vanguard_conflicting_dates_are_not_overwritten_and_footnote_is_not_duration():
    r = assess.parse('''Vanguard Global Aggregate Bond UCITS ETF EUR Hedged Accumulating
    Factsheet | 31 October 2026 Data as at 31 October 2026 unless otherwise stated.
    Average duration 6.0 years Average effective maturity 6 8.3 years
    Data as at 30 September 2026.''', 'VAGF.DE', 'https://fund-docs.vanguard.com/Global.pdf')
    assert r['source_dates']['document'] == '2026-10-31'
    assert len(r['source_dates']['statements']) == 2
    assert r['fields']['duration']['value'] == 'Average duration 6.0 years'
    assert r['fields']['duration']['as_of'] is None
    assert assess.date('31 November 2026') is None


def test_chart_title_without_numbers_is_not_credit_coverage():
    r = assess.parse('iShares Example UCITS ETF CREDIT RATINGS (%) Fund Credit quality ratings', 'X.DE', 'https://www.ishares.com/x.pdf')
    assert r['fields']['credit_quality'] is None
    assert any('chart' in warning for warning in r['warnings'])
    bnd = assess.parse('Vanguard Total Bond Market ETF As of September 30, 2026 Distribution by credit quality 2 U.S. Government 69.0 % AAA 3.1 % AA 3.6 % Portfolio management', 'BND', 'https://fund-docs.vanguard.com/F0928.pdf')
    assert bnd['fields']['credit_quality']['as_of'] == '2026-09-30'


def test_qqq_fallback_uses_only_explicit_structured_identifier():
    html = '<script type="application/ld+json">'+json.dumps({'identifier':[{'propertyID':'ISIN','value':'US46090E1038'}, {'propertyID':'Ticker','value':'QQQ'}]})+'</script>'
    r = assess.parse_product(html)
    assert r['fields']['identifier']['value'] == 'US46090E1038'
    assert r['fields']['fee'] is None
    assert r['fields']['identifier']['as_of'] is None
    assert assess.parse_product('<html>QQQ 0.18%</html>')['fields']['identifier'] is None


def test_html_200_is_not_pdf_success(tmp_path, monkeypatch):
    class Response:
        status, url, headers = 200, 'https://issuer.test/splash', {'Content-Type':'text/html'}
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def read(self, bound): return b'<html>Country selection</html>'
    monkeypatch.setattr(collect, 'urlopen', lambda *a, **k: Response())
    r = collect.collect({'symbol':'X','kind':'factsheet','url':'https://issuer.test/f.pdf'}, tmp_path, 0)
    assert r['status'] == 200 and 'non-PDF' in r['error']
    assert (tmp_path / r['raw_file']).exists()
    assert 'text_file' not in r


def test_report_keeps_all_missing_candidate_and_failures():
    rows = [{'symbol':'X','market':'EU','fields':dict.fromkeys(assess.FIELDS)}]
    attempts = [{'symbol':'X','kind':'factsheet','url':'https://issuer.test','collected_at_utc':'2026-11-17T00:00:00Z','status':404,'error':'not found','run':'test'}]
    report = assess.report(rows, attempts)
    assert '## X' in report and 'HTTP 404' in report and 'MISSING / unresolved' in report
    assert '| fee | 0 | 0 |' in report
    assert 'Not applicable to equity' not in report  # unknown intention remains missing


def test_asset_amount_does_not_consume_following_heading():
    for heading in ('FEE DETAILS', 'FEES AND EXPENSES BREAKDOWN'):
        r = assess.parse('IWM Net Assets of Fund (M) : $78,041.73 '+heading, 'IWM', 'https://www.ishares.com/x.pdf')
        assert r['fields']['net_assets']['value'] == '$78,041.73'
    for currency in ('USD', 'EUR'):
        r = assess.parse('iShares Example UCITS ETF Net Assets of Fund (M) : 14,565.57 '+currency+' SFDR Classification : Other', 'X.DE', 'https://www.ishares.com/x.pdf')
        assert r['fields']['net_assets']['value'] == '14,565.57 '+currency
    r = assess.parse('Net Assets of Fund (M) : 12.34 EUROPE', 'X', 'https://www.ishares.com/x.pdf')
    assert r['fields']['net_assets']['value'] == '12.34'


def test_subset_replay_retains_missing_bond_evidence(tmp_path, monkeypatch):
    universe = json.loads((Path(__file__).parents[1]/'data/universe.json').read_text())
    (tmp_path/'universe.json').write_text(json.dumps(universe))
    (tmp_path/'equity.txt').write_text('iShares Example UCITS ETF ISIN : IE00B5BMR087')
    attempts = [
        {'symbol':'SXR8.DE', 'kind':'factsheet', 'error':None, 'text_file':'equity.txt', 'url':'https://www.ishares.com/equity.pdf', 'collected_at_utc':'2026-11-17T00:00:00Z'},
        {'symbol':'BND', 'kind':'factsheet', 'error':'download failed', 'status':404, 'url':'https://fund-docs.vanguard.com/F0928.pdf', 'collected_at_utc':'2026-11-17T00:00:01Z'},
    ]
    (tmp_path/'collection.json').write_text(json.dumps({'results':attempts}))
    output = tmp_path/'report.md'
    monkeypatch.setattr(sys, 'argv', ['assess_issuers.py', str(tmp_path), '--output', str(output)])
    assess.main()
    rows = {r['symbol']:r for r in json.loads(output.with_suffix('.json').read_text())['rows']}
    assert len(rows) == 24
    for symbol in ('BND', 'AGG', 'SHY', 'VAGF.DE'):
        assert rows[symbol]['bond_measures_applicable'] is True
        assert rows[symbol]['fields']['duration'] is None
        section = output.read_text(encoding='utf-8').split('## '+symbol+'\n', 1)[1].split('\n## ', 1)[0]
        assert '| duration | MISSING / unresolved |' in section
        assert '| credit_quality | MISSING / unresolved |' in section
        assert 'Not applicable to equity' not in section
    assert rows['SXR8.DE']['bond_measures_applicable'] is False
    assert rows['SPY']['bond_measures_applicable'] is False
    assert assess.bond_applicability(None) is None
    assert assess.bond_applicability('Unclassified strategy') is None
