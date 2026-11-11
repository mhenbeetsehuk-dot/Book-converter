"""Minimal private localhost manuscript upload + plan + Blender script server."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from html import escape
import json
from brain import plan, blender_script

MAX_BYTES = 2 * 1024 * 1024
PAGE = """<!doctype html><html lang="en"><meta charset="utf-8">
<title>Book-converter</title><style>
body{font:16px system-ui;max-width:850px;margin:3rem auto;padding:1rem;background:#101827;color:#f0f4fa}
textarea{width:100%;height:280px;background:#1d293b;color:white;padding:1rem;box-sizing:border-box}
button{padding:.8rem 1.2rem;background:#65c9df;border:0;border-radius:6px;cursor:pointer}
a{color:#80d9ef}pre{white-space:pre-wrap}</style>
<h1>Book-converter · Stage 1</h1>
<p>Paste your manuscript (up to 2 MB) to generate an editable scene plan and a sample Blender render script.</p>
<form method="post" action="/plan"><textarea name="manuscript" required></textarea><p><button>Generate scene plan</button></p></form>
<p>Free prototype: placeholder 3D geometry, not a finished movie.</p></html>"""
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200 if self.path == "/" else 404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(PAGE.encode() if self.path == "/" else b"Not found")
    def do_POST(self):
        if self.path != "/plan":
            self.send_error(404); return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size <= 0 or size > MAX_BYTES:
                self.send_error(413, "Manuscript must be 1 byte to 2 MB"); return
            body = self.rfile.read(size).decode("utf-8")
            manuscript = parse_qs(body).get("manuscript", [""])[0]
            scenes = plan(manuscript)
            script = blender_script(scenes[0])
            result = ("<h1>Scene plan</h1><p>Scenes: " + str(len(scenes)) +
                      "</p><p>Save the JSON and Blender script below as files.</p><h2>Plan JSON</h2><pre>" +
                      escape(json.dumps(scenes, indent=2)) +
                      "</pre><h2>Blender Python script</h2><pre>" + escape(script) + "</pre>")
            data = ("<!doctype html><meta charset='utf-8'><body style='font:14px system-ui;max-width:850px;margin:auto'>" + result + "</body>").encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except (ValueError, UnicodeDecodeError) as exc:
            self.send_error(400, str(exc))
if __name__ == "__main__":
    print("Open http://localhost:8000")
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
