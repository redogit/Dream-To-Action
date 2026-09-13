"""Rerun the original browser suite without overwriting preserved release evidence."""
from __future__ import annotations
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> None:
    if importlib.util.find_spec('playwright') is None:
        raise SystemExit('Install the optional Python Playwright development dependency and Chromium first. The application itself does not need them.')
    subprocess.run([sys.executable, str(ROOT / 'tools' / 'verify.py')], check=True)
    started = now()
    with tempfile.TemporaryDirectory(prefix='dream-browser-') as temporary:
        work = Path(temporary) / 'prototype'
        shutil.copytree(ROOT / 'prototype', work)
        env = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8')
        subprocess.run([sys.executable, '-X', 'utf8', str(work / 'test_app.py')],
                       check=True, timeout=180, env=env)
        result_bytes = (work / 'test-results.json').read_bytes()
        result = json.loads(result_bytes)
        if result.get('result') != 'PASS' or result.get('passed') != 43 or result.get('failed') != 0:
            raise SystemExit('Unexpected browser-suite result; no passing verification record was written.')
    record = {
        'run_started_utc': started,
        'run_finished_utc': now(),
        'runner': 'Original v0.1 test_app.py, executed in a disposable copy',
        'application_sha256': hashlib.sha256((ROOT / 'index.html').read_bytes()).hexdigest(),
        'suite_result_sha256': hashlib.sha256(result_bytes).hexdigest(),
        'current_run_note': 'HTML was supplied through page.set_content. Direct local-file and HTTP navigation were not tested by this run. The suite retains its original date and historical environment wording; these wrapper timestamps identify this execution.',
        'result': result,
    }
    output = ROOT / '.test-output'
    output.mkdir(exist_ok=True)
    name = 'browser-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.json'
    with (output / name).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    subprocess.run([sys.executable, str(ROOT / 'tools' / 'verify.py')], check=True)
    print('New run record:', output / name)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        raise SystemExit('Browser checks failed: ' + str(error))
