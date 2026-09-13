"""Browser smoke/regression checks. Requires Python, Playwright and Chromium; the app does not."""
from __future__ import annotations
import json
import os
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parent
checks: list[dict[str, str]] = []

def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    checks.append({'check': name, 'status': 'PASS'})


def run() -> None:
    with sync_playwright() as pw:
        executable = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('google-chrome')
        options = {'headless': True}
        if executable:
            options['executable_path'] = executable
        browser = pw.chromium.launch(**options)
        context = browser.new_context(accept_downloads=True, viewport={'width': 1360, 'height': 1000})
        page = context.new_page()
        errors, bad_console, network = [], [], []
        page.on('pageerror', lambda err: errors.append(str(err)))
        page.on('console', lambda msg: bad_console.append(msg.text) if msg.type == 'error' else None)
        page.on('request', lambda req: network.append(req.url) if req.url.startswith(('http:', 'https:', 'ws:', 'wss:')) else None)
        page.on('dialog', lambda dialog: dialog.accept())
        page.set_content((ROOT/'dream-to-action.html').read_text(encoding='utf-8'))
        check('Self-contained HTML initializes when supplied directly to the browser', page.title().startswith('Dream to Action'))
        check('Blank state does not invent a plan or result', page.locator('#history-list li').count() == 0)
        page.keyboard.press('Tab')
        check('First keyboard stop is the skip link', page.evaluate('document.activeElement.className') == 'skip')
        page.keyboard.press('Enter')
        check('Skip link moves focus to the main content', page.evaluate('document.activeElement.id') == 'main')
        check('Every form control has an associated label', page.evaluate('''() => [...document.querySelectorAll('input,select,textarea')].every(el => el.labels && el.labels.length > 0)'''))
        check('Every described-by reference exists', page.evaluate(r'''() => [...document.querySelectorAll('[aria-describedby]')].every(el => el.getAttribute('aria-describedby').split(/\s+/).every(id => document.getElementById(id)))'''))
        check('No duplicate HTML IDs', page.evaluate('''() => { const ids = [...document.querySelectorAll('[id]')].map(x => x.id); return ids.length === new Set(ids).size; }'''))
        check('No positive tabindex overrides keyboard order', page.locator('[tabindex]:not([tabindex="0"]):not([tabindex="-1"])').count() == 0)
        check('Routine feedback has a status live region', page.locator('#status').get_attribute('role') == 'status')
        page.get_by_role('button',name='Save a plan snapshot', exact=True).click()
        check('Required fields are validated without creating a plan', page.locator('#errors li').count() == 4 and page.locator('#history-list li').count() == 0)
        check('Validation errors receive keyboard focus', page.evaluate('document.activeElement.id') == 'errors')
        page.locator('#errors a').first.click()
        check('Error links move focus to the relevant control', page.evaluate('document.activeElement.id') == 'goal')
        page.get_by_role('button',name='Add an observation', exact=True).click()
        check('Observation is rejected without a plan', 'Save a plan snapshot' in page.locator('#errors').inner_text())
        page.get_by_role('button',name='Load an example', exact=True).click()
        check('Example is explicitly illustrative, not a claimed real result', page.locator('#kind').input_value() == 'illustrative')
        page.get_by_role('button',name='Save a plan snapshot', exact=True).click()
        check('Saving a snapshot creates one plan and no fake outcome', page.locator('#history-list li').count() == 1)
        check('Unconfirmed required support is not treated as available', 'Required support is not confirmed' in page.locator('#preview-content').inner_text())
        page.locator('#support-details > summary').click()
        page.select_option('#readiness','ready')
        page.get_by_role('button',name='Save a plan snapshot',exact=True).click()
        check('Readiness alone does not override unconfirmed support', 'Required support is not confirmed' in page.locator('#preview-content').inner_text())
        page.select_option('#supportStatus','confirmed')
        page.get_by_role('button',name='Save a plan snapshot',exact=True).click()
        check('Confirmed support still carries an independent-verification qualification', 'not independently verified' in page.locator('#preview-content').inner_text())
        page.select_option('#supportStatus','not_needed')
        page.get_by_role('button',name='Save a plan snapshot',exact=True).click()
        check('Contradictory required-support fields are flagged', 'Clarify support' in page.locator('#preview-content').inner_text())
        page.select_option('#supportStatus','unavailable')
        page.get_by_role('button',name='Save a plan snapshot',exact=True).click()
        check('Unavailable support is not counted as opportunity', 'not available' in page.locator('#preview-content').inner_text())
        page.select_option('#readiness','paused')
        page.get_by_role('button',name='Save a plan snapshot',exact=True).click()
        check('Choosing to pause is preserved, not ranked as failure', 'Paused by choice' in page.locator('#preview-content').inner_text())
        page.locator('#goal').fill('An edited goal before saving')
        page.locator('#observation').fill('Fictional review for automated testing, not a real outcome.')
        page.get_by_role('button',name='Add an observation',exact=True).click()
        check('An observation cannot silently attach to an outdated snapshot', 'unsaved changes' in page.locator('#errors').inner_text())
        page.get_by_role('button',name='Save a plan snapshot',exact=True).click()
        page.select_option('#outcome','no_change')
        page.get_by_role('button',name='Add an observation',exact=True).click()
        check('Observation references its exact plan snapshot', 'Observation o-0001 about p-0007' in page.locator('#history-list').inner_text())
        check('Earlier plan snapshots are preserved', page.locator('#history-list li').count() == 8)
        page.locator('#goal').fill('Unrecorded draft to preserve')
        page.locator('#observation').fill('An unfinished observation draft')
        with page.expect_download() as info:
            page.get_by_role('button',name='Export journal (.json)',exact=True).click()
        download = info.value
        fixture = ROOT/'_test_journal.json'
        download.save_as(fixture)
        data = json.loads(fixture.read_text())
        check('JSON export includes unsaved plan and observation drafts', data['draft']['goal'] == 'Unrecorded draft to preserve' and data['reviewDraft']['note'] == 'An unfinished observation draft')
        check('JSON export preserves all snapshots and linked observations', len(data['plans']) == 7 and len(data['observations']) == 1 and data['observations'][0]['planId'] == 'p-0007')
        with page.expect_download() as info:
            page.get_by_role('button',name='Export readable report (.txt)',exact=True).click()
        report_path = ROOT/'_test_report.txt'
        info.value.save_as(report_path)
        report = report_path.read_text()
        check('Readable text export includes current draft, history, and unverified-data limits', all(t in report for t in ['Unrecorded draft to preserve','An unfinished observation draft','PLAN p-0001','OBSERVATION o-0001','No independent verification']))
        page.get_by_role('button',name='Clear this open journal',exact=True).click()
        check('Clear resets the open journal and form after confirmation', page.locator('#history-list li').count() == 0 and page.locator('#goal').input_value() == '')
        page.locator('#import-file').set_input_files(str(fixture))
        expect(page.locator('#status')).to_contain_text('Journal restored')
        check('Import round-trip restores current draft and history', page.locator('#goal').input_value() == 'Unrecorded draft to preserve' and page.locator('#history-list li').count() == 8)
        check('Import restores unfinished observation draft', page.locator('#observation').input_value() == 'An unfinished observation draft')
        page.locator('#import-file').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'{not json'})
        expect(page.locator('#errors')).to_contain_text('not valid JSON')
        check('Malformed JSON is rejected without overwriting current work', page.locator('#goal').input_value() == 'Unrecorded draft to preserve')
        bad = json.loads(fixture.read_text()); bad['observations'][0]['planId'] = 'p-9999'
        page.locator('#import-file').set_input_files({'name':'bad-reference.json','mimeType':'application/json','buffer':json.dumps(bad).encode()})
        expect(page.locator('#errors')).to_contain_text('plan references are invalid')
        check('Broken provenance references are rejected atomically', page.locator('#history-list li').count() == 8)
        bad = json.loads(fixture.read_text()); bad['draft']['reviewDate'] = '2026-02-30'
        page.locator('#import-file').set_input_files({'name':'bad-date.json','mimeType':'application/json','buffer':json.dumps(bad).encode()})
        expect(page.locator('#errors')).to_contain_text('valid review date')
        check('Impossible imported calendar dates are rejected', 'valid review date' in page.locator('#errors').inner_text())
        bad = json.loads(fixture.read_text()); bad['schemaVersion'] = '99.0'
        page.locator('#import-file').set_input_files({'name':'bad-version.json','mimeType':'application/json','buffer':json.dumps(bad).encode()})
        expect(page.locator('#errors')).to_contain_text('Unsupported journal')
        check('Unknown schema versions are rejected', page.locator('#goal').input_value() == 'Unrecorded draft to preserve')
        page.locator('#import-file').set_input_files({'name':'too-large.json','mimeType':'application/json','buffer':b' '*1048577})
        expect(page.locator('#errors')).to_contain_text('larger than 1 MiB')
        check('Oversized files are rejected before parsing', 'larger than 1 MiB' in page.locator('#errors').inner_text())
        bad = json.loads(fixture.read_text()); bad['draft']['goal'] = 'x'*4001
        page.locator('#import-file').set_input_files({'name':'long-field.json','mimeType':'application/json','buffer':json.dumps(bad).encode()})
        expect(page.locator('#errors')).to_contain_text('4000 characters')
        check('Imported text fields enforce length bounds', '4000 characters' in page.locator('#errors').inner_text())
        xss = json.loads(fixture.read_text()); injection = '<img src="https://invalid.example/x" onerror="window.injected=true"><script>window.injected=true</script>'
        xss['draft']['goal'] = injection; xss['plans'][-1]['fields']['goal'] = injection
        page.locator('#import-file').set_input_files({'name':'inert-text.json','mimeType':'application/json','buffer':json.dumps(xss).encode()})
        expect(page.locator('#status')).to_contain_text('Journal restored')
        check('Imported markup is rendered as literal text, not HTML', injection in page.locator('#preview-content').inner_text() and page.locator('#preview-content img').count() == 0 and page.evaluate('window.injected') is None)
        check('No application HTTP/WebSocket requests occurred during the tested workflow', network == [])
        check('App source has no browser-storage calls and no cookies were created', not any(token in (ROOT/'app.js').read_text() for token in ['localStorage','sessionStorage','indexedDB','document.cookie']) and context.cookies() == [])
        check('Content Security Policy explicitly blocks network connections', "connect-src 'none'" in page.locator('meta[http-equiv="Content-Security-Policy"]').get_attribute('content'))
        page.set_viewport_size({'width':320,'height':900})
        check('The tested screen fits a 320 CSS-pixel viewport without horizontal overflow', page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'))
        page.screenshot(path=str(ROOT/'_test_mobile.png'),full_page=True)
        page.set_viewport_size({'width':1360,'height':1000})
        page.get_by_role('button',name='Clear this open journal',exact=True).click()
        page.get_by_role('button',name='Load an example',exact=True).click()
        page.get_by_role('button',name='Save a plan snapshot',exact=True).click()
        page.locator('#support-details').evaluate('(el) => el.open = false')
        page.screenshot(path=str(ROOT/'preview.png'),full_page=True)
        check('No uncaught JavaScript errors occurred', errors == [])
        check('No browser console errors occurred in the tested workflow', bad_console == [])
        browser_version = browser.version
        browser.close()
    output = {
        'app_version':'0.1','date':'2026-09-13','environment':{'browser':'Chromium','version':browser_version,'driver':'Playwright Python','mode':'Headless Chromium with HTML supplied through page.set_content; environment policy blocks file and loopback navigation'},
        'result':'PASS','passed':len(checks),'failed':0,'checks':checks,
        'limits':['No real person or service-provider pilot was performed.','No JAWS, NVDA, VoiceOver, or other actual screen-reader session was run.','No full WCAG conformance audit or independent security audit was performed.','No real-world opportunity, income, housing, health, or employment result is claimed.','Only the included browser workflows and fixtures were tested.', 'Direct file:// and loopback-HTTP launch were blocked by test-environment policy. Browser checks supplied the identical self-contained HTML through page.set_content; direct local-file launch remains unverified.']
    }
    (ROOT/'test-results.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'passed':len(checks),'failed':0,'browser':browser_version,'errors':errors,'console_errors':bad_console},indent=2))

if __name__ == '__main__':
    run()
