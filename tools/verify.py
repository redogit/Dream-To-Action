"""Check the preserved release, entry point, rebuild, and inline policy hashes."""
from __future__ import annotations
import base64
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'prototype'
EXPECTED = {
    'dream-to-action.html', 'README.md', 'README.txt', 'PILOT.md', 'TESTING.md',
    'build.py', 'app.js', 'style.css', 'test_app.py', 'test-results.json',
    'example-journal.json',
}
GENERATED = ('dream-to-action.html', 'app.js', 'style.css')


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    entries: dict[str, str] = {}
    for line in (SOURCE / 'MANIFEST.sha256').read_text(encoding='utf-8').splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  ([A-Za-z0-9_.-]+)', line)
        require(match is not None, 'Malformed release manifest entry')
        digest, name = match.groups()
        require(name not in entries, 'Duplicate release manifest entry: ' + name)
        entries[name] = digest
    require(set(entries) == EXPECTED, 'Release manifest membership changed')
    require({p.name for p in SOURCE.iterdir()} == EXPECTED | {'MANIFEST.sha256'},
            'The preserved prototype has missing or extra entries')
    for name, digest in entries.items():
        path = SOURCE / name
        require(path.is_file() and not path.is_symlink(), 'Not a regular release file: ' + name)
        require(hashlib.sha256(path.read_bytes()).hexdigest() == digest,
                'Release hash mismatch: ' + name)
    application = (SOURCE / 'dream-to-action.html').read_bytes()
    require((ROOT / 'index.html').read_bytes() == application,
            'index.html differs from the preserved standalone application')
    with tempfile.TemporaryDirectory(prefix='dream-build-') as temporary:
        work = Path(temporary) / 'prototype'
        shutil.copytree(SOURCE, work)
        subprocess.run([sys.executable, '-X', 'utf8', str(work / 'build.py')],
                       check=True, timeout=30, capture_output=True, text=True)
        for name in GENERATED:
            # Python text output may use CRLF on Windows; canonical release text is LF.
            rebuilt = (work / name).read_bytes().replace(b'\r\n', b'\n')
            require(rebuilt == (SOURCE / name).read_bytes(), 'Canonical rebuild differs: ' + name)
    text = application.decode('utf-8')
    policies = re.findall(r'http-equiv="Content-Security-Policy" content="([^"]+)"', text)
    require(len(policies) == 1, 'Expected exactly one inline security policy')
    policy = policies[0]
    for tag, directive in [('script', 'script-src'), ('style', 'style-src')]:
        blocks = re.findall('<' + tag + '>(.*?)</' + tag + '>', text, flags=re.S)
        require(len(blocks) == 1, 'Expected exactly one inline ' + tag + ' block')
        encoded = base64.b64encode(hashlib.sha256(blocks[0].encode('utf-8')).digest()).decode('ascii')
        require(directive + " 'sha256-" + encoded + "'" in policy,
                'Inline security-policy hash does not match ' + tag)
    require("connect-src 'none'" in policy, 'Application connection restriction changed')
    for name in ('test-results.json', 'example-journal.json'):
        json.loads((SOURCE / name).read_text(encoding='utf-8'))
    print(json.dumps({'result': 'PASS', 'release_hashes': len(entries),
                      'preserved_files': len(EXPECTED) + 1,
                      'canonical_rebuild_matches': len(GENERATED),
                      'root_entry_point_identical': True, 'inline_policy_hashes_match': True}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        raise SystemExit('Verification failed: ' + str(error))
