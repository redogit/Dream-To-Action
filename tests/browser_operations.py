"""Browser checks for the actual standalone operational artifact; uses synthetic records."""
from __future__ import annotations
import json, tempfile, os
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'.test-output'; OUT.mkdir(exist_ok=True)
checks=[]
def check(name, condition):
    if not condition: raise AssertionError(name)
    checks.append(name)
def run():
    with sync_playwright() as pw, tempfile.TemporaryDirectory() as temp:
        browser=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True)
        ctx=browser.new_context(accept_downloads=True,viewport={'width':1440,'height':1080})
        probe=ctx.new_page(); launch='file://'
        try: probe.goto((ROOT/'index.html').as_uri(),wait_until='load',timeout=5000)
        except Exception as e: launch='page.set_content (direct file launch failed: '+str(e).splitlines()[0]+')'
        probe.close()
        page=ctx.new_page(); errors=[]; requests=[]; consoles=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('console',lambda m:consoles.append(m.text) if m.type=='error' else None)
        page.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:','ws:','wss:')) else None)
        page.on('dialog',lambda d:d.accept())
        if launch=='file://': page.goto((ROOT/'index.html').as_uri(),wait_until='load')
        else: page.set_content((ROOT/'index.html').read_text(encoding='utf-8'))
        expect(page.locator('#overview-title')).to_contain_text('Make the next step')
        check('Personal workspace starts with zero goal records',page.locator('#goal-grid .goal-card').count()==0)
        check('Charts have accessible textual table equivalents',page.locator('.flow-table th').count()==4 and page.locator('.flow-svg').get_attribute('role')=='img')
        page.keyboard.press('Tab');check('First keyboard stop is the skip link',page.locator(':focus').get_attribute('class')=='skip')
        page.keyboard.press('Enter');check('Skip link focuses main content',page.locator(':focus').get_attribute('id')=='main')
        page.locator('#mode-switch').click();check('Demo has six goals',page.locator('#goal-grid .goal-card').count()==6)
        check('Demo is prominently marked synthetic', 'DEMONSTRATION ONLY' in page.locator('#mode-notice').inner_text())
        page.screenshot(path=str(OUT/'overview-desktop.png'),full_page=True)
        page.locator('nav [data-view="board"]').click();check('Demo board has eighteen actions',page.locator('.action-card').count()==18)
        page.screenshot(path=str(OUT/'board-desktop.png'),full_page=True)
        page.locator('#action-search').fill('template owner');check('Action search filters records',page.locator('.action-card').count()==1)
        page.locator('#action-search').fill('');page.locator('#mode-switch').click();check('Demo data does not leak into personal actions',page.locator('.action-card').count()==0)
        page.locator('#new-goal').click();expect(page.locator('#editor')).to_be_visible()
        page.locator('#f-title').fill('My synthetic test goal');page.locator('#f-barrier').fill('Test barrier');page.locator('#f-success').fill('A clearly observed change');page.locator('#save-editor').click()
        check('A personal goal can be created',page.locator('#goal-grid .goal-card').count()==1)
        page.locator('#new-action').click();page.locator('#f-title').fill('Synthetic action');page.locator('#f-support').select_option('not_needed');page.locator('#f-minutes').fill('15');page.locator('#f-cost').fill('0');page.locator('#save-editor').click()
        check('Explicit no-support action enters ready lane',page.locator('.lane').first.locator('.action-card').count()==1)
        page.get_by_role('button',name='Record completion',exact=True).click();page.locator('#f-note').fill('Synthetic completion; not a real outcome');page.locator('#save-editor').click()
        check('Completion is recorded in completed lane',page.locator('.lane').last.locator('.action-card').count()==1)
        page.locator('nav [data-view="evidence"]').click();check('Completion did not fabricate improvement evidence',page.locator('.evidence-card').count()==0)
        page.locator('#new-observation').click();page.locator('#f-note').fill('Synthetic observation: no change');page.locator('#f-outcome').select_option('no_change');page.locator('#save-editor').click()
        check('Observation is rendered separately',page.locator('.evidence-card').count()==1 and 'no change' in page.locator('.evidence-card').inner_text())
        with page.expect_download() as d: page.locator('#export-json').click()
        p=Path(temp)/'backup.json';d.value.save_as(p);original=json.loads(p.read_text())
        check('JSON contains real workspace history and mode',original['mode']=='personal' and len(original['events'])==4)
        page.locator('#clear-workspace').click();page.locator('#import-file').set_input_files(str(p));expect(page.locator('#status')).to_contain_text('Restored personal')
        check('Restore recovers goals actions and evidence',page.locator('.evidence-card').count()==1 and page.locator('#goal-grid .goal-card').count()==1)
        page.locator('#import-file').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'{not json'})
        expect(page.locator('#error')).to_be_visible();check('Invalid import leaves current workspace unchanged',page.locator('.evidence-card').count()==1)
        page.locator('#import-file').set_input_files({'name':'oversized.json','mimeType':'application/json','buffer':b' '*(2097152+1)})
        expect(page.locator('#error')).to_contain_text('2 MiB');check('Oversized import is rejected before replacement',page.locator('.evidence-card').count()==1)
        with page.expect_download() as d:page.locator('#export-csv').click()
        p_csv=Path(temp)/'actions.csv';d.value.save_as(p_csv);check('CSV export includes action and mode','Synthetic action' in p_csv.read_text() and 'personal' in p_csv.read_text())
        with page.expect_download() as d:page.locator('#export-report').click()
        report=Path(temp)/'report.txt';d.value.save_as(report);check('Handoff includes original goal and observation','My synthetic test goal' in report.read_text() and 'Synthetic observation' in report.read_text())
        page.locator('nav [data-view="overview"]').click();page.get_by_role('button',name='Revise goal',exact=True).click();page.locator('#f-title').fill('<img src="https://invalid.example" onerror="alert(1)">');page.locator('#f-reason').fill('Literal text test');page.locator('#save-editor').click()
        check('User markup stays literal text',page.locator('#goal-grid img').count()==0 and '<img' in page.locator('#goal-grid').inner_text())
        page.locator('nav [data-view="resources"]').click();check('Six dated primary-source references appear',page.locator('#resource-grid .goal-card').count()==6 and page.locator('#resource-grid').inner_text().count('2026-09-28')==6)
        page.locator('#resource-search').fill('housing');check('Resource search filters',page.locator('#resource-grid .goal-card').count()==1)
        page.get_by_role('button',name='Draft a next action',exact=True).click();check('Reference does not auto-confirm support',page.locator('#f-support').input_value()=='unknown');page.locator('#close-editor').click()
        page.locator('#resource-search').fill('');page.locator('#mode-switch').click();page.locator('nav [data-view="overview"]').click()
        for width in [320,390,768]:
            page.set_viewport_size({'width':width,'height':900});check('Overview fits '+str(width)+' CSS pixels',page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
        page.screenshot(path=str(OUT/'overview-mobile.png'),full_page=True)
        page.set_viewport_size({'width':320,'height':900});page.locator('nav [data-view="board"]').click();check('Action board fits 320 CSS pixels',page.evaluate('document.documentElement.scrollWidth <= innerWidth'))
        page.screenshot(path=str(OUT/'board-mobile.png'),full_page=True)
        check('No application network requests',requests==[])
        check('No uncaught errors',errors==[])
        check('No console errors',consoles==[])
        check('Every input has a label',page.evaluate("[...document.querySelectorAll('input,select,textarea')].every(x=>x.labels&&x.labels.length)"))
        version=browser.version;browser.close()
    result={'run_utc':datetime.now(timezone.utc).isoformat(),'browser':version,'launch_mode':launch,'passed':len(checks),'failed':0,'checks':checks,'limits':['Synthetic workflows only','No actual screen-reader session','No independent security or accessibility audit','No participant pilot','No hosted deployment tested']}
    (OUT/'browser-operations.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':run()
