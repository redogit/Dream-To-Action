"""Optional loopback-only launch for a stable local browser-storage origin."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import webbrowser

class LocalHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        super().end_headers()

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--port',type=int,default=8765)
    p.add_argument('--no-browser',action='store_true')
    a=p.parse_args()
    if not 1024 <= a.port <= 65535: p.error('port must be 1024 through 65535')
    handler=partial(LocalHandler,directory=str(Path(__file__).resolve().parents[1]))
    try:
        with ThreadingHTTPServer(('127.0.0.1',a.port),handler) as server:
            url=f'http://127.0.0.1:{a.port}/'
            print(f'Dream to Action: {url}\nLocal machine only. Press Ctrl+C to stop.')
            if not a.no_browser: webbrowser.open(url)
            server.serve_forever()
    except KeyboardInterrupt: pass
    except OSError as error: raise SystemExit(f'Cannot start local server: {error}. Try another --port.')
