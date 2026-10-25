#!/usr/bin/env python3
"""Serve ./app locally, with an optional live-model endpoint (standard library only).

  python3 tools/live_server.py            # then open http://127.0.0.1:8000/?live=1
  python3 tools/live_server.py --port 8080

Without ?live=1 the app replays app/cache.json exactly as with `python -m http.server`.
With ?live=1 the app POSTs to /api/generate for each stage; this server calls the model
(ANTHROPIC_API_KEY or OPENAI_API_KEY + DEMO_MODEL, see tools/model_client.py) and
returns its answer. The browser gives up after 5 seconds and shows the saved output,
so a slow or unreachable model never stalls the talk. The API key stays in this
process; it is never sent to the browser.

Binds to 127.0.0.1 only.
"""
import argparse
import functools
import http.server
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model_client  # noqa: E402
import regenerate_cache  # noqa: E402

APP_DIR = os.path.join(regenerate_cache.ROOT, "app")


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write("  " + (fmt % args) + "\n")

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _json(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/api/generate":
            return self._json(404, {"error": "not found"})
        try:
            req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            key = req.get("stage") if req.get("demo") == "demo1" else req.get("step")
            prompt, name, text = regenerate_cache.request_for(req.get("demo"), key)
        except (KeyError, ValueError, StopIteration) as e:
            return self._json(400, {"error": f"bad request: {e}"})
        if model_client.provider() is None:
            return self._json(503, {"error": "no API key configured; app will use saved outputs"})
        try:
            r = model_client.generate(prompt, name, text, timeout=30)
        except model_client.ModelError as e:
            return self._json(502, {"error": str(e)})
        return self._json(200, r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8000)
    a = ap.parse_args()
    handler = functools.partial(Handler, directory=APP_DIR)
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", a.port), handler)
    p = model_client.provider()
    print(f"Serving {APP_DIR} at http://127.0.0.1:{a.port}/")
    print(f"Live mode: http://127.0.0.1:{a.port}/?live=1  "
          + (f"(provider: {p}, model: {model_client.model_name()})" if p else
             "(no API key set: live mode will fall back to saved outputs)"))
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
