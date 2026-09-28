"""Build/check the standalone operations app. No network or runtime dependencies."""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def render() -> str:
    read = lambda path: (ROOT / path).read_text(encoding='utf-8')
    jsdata = lambda path: json.dumps(json.loads(read(path)), ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    html = read('operational/shell.html')
    for marker, content in [('__CSS__', read('operational/style.css')), ('__CORE__', read('operational/core.js')), ('__APP__', read('operational/app.js')), ('__RESOURCES__', jsdata('data/resources.json')), ('__DEMO__', jsdata('data/demo.json'))]:
        if html.count(marker) != 1:
            raise ValueError('Missing/duplicate build marker: ' + marker)
        html = html.replace(marker, content)
    digest = lambda data: "'sha256-" + base64.b64encode(hashlib.sha256(data.encode('utf-8')).digest()).decode() + "'"
    scripts = re.findall(r'<script>(.*?)</script>', html, re.S)
    styles = re.findall(r'<style>(.*?)</style>', html, re.S)
    if len(scripts) != 3 or len(styles) != 1:
        raise ValueError('Unexpected inline block count')
    policy = "default-src 'none'; script-src " + ' '.join(map(digest, scripts)) + '; style-src ' + ' '.join(map(digest, styles)) + "; connect-src 'none'; img-src 'none'; font-src 'none'; base-uri 'none'; form-action 'none'; object-src 'none'"
    return html.replace('__CSP__', policy)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = render().encode('utf-8')
    target = ROOT / 'index.html'
    if args.check:
        if target.read_bytes() != data:
            raise SystemExit('FAIL: index.html does not match the source/data build.')
        print('PASS: operations rebuild matches; inline script/style hashes regenerated.')
    else:
        target.write_bytes(data)
        print('Built index.html:', len(data), 'bytes')
