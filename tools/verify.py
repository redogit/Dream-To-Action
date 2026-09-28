"""Verify preserved predecessor in isolation, then the operational successor."""
from pathlib import Path
import json, shutil, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parents[1]

def run(args, cwd=ROOT):
    subprocess.run(args,cwd=cwd,check=True,timeout=60)

if __name__=='__main__':
    try:
        # The old verifier is retained byte-for-byte. Its root identity check is
        # evaluated against the predecessor, not falsely applied to the successor.
        with tempfile.TemporaryDirectory(prefix='dta-predecessor-') as temporary:
            d=Path(temporary)
            shutil.copytree(ROOT/'prototype',d/'prototype')
            (d/'tools').mkdir()
            shutil.copy2(ROOT/'tools/verify_v01.py',d/'tools/verify.py')
            shutil.copy2(ROOT/'redogit.json',d/'redogit.json')
            shutil.copy2(ROOT/'prototype/dream-to-action.html',d/'index.html')
            print('PREDECESSOR: original package and preserved REDOGIT policies',flush=True)
            run([sys.executable,'tools/verify.py'],d)
        print('SUCCESSOR: deterministic build, source validation, and state tests',flush=True)
        run([sys.executable,'tools/build_operations.py','--check'])
        run(['node','--check','operational/core.js'])
        run(['node','--check','operational/app.js'])
        run(['node','--test','tests/operations.test.cjs'])
        run(['node','-e',"const C=require('./operational/core.js');C.validate(require('./data/demo.json'));console.log('PASS: illustrative data validates');"])
        resources=json.loads((ROOT/'data/resources.json').read_text(encoding='utf-8'))
        assert len(resources)==6 and len({r['id'] for r in resources})==6
        assert all(r['url'].startswith('https://') and r['checked']=='2026-09-28' and r['confirm'] for r in resources)
        print('PASS: predecessor and successor checks. Reference integrity is not a live availability check.')
    except (OSError,AssertionError,subprocess.SubprocessError) as error:
        raise SystemExit('Verification failed: '+str(error))
