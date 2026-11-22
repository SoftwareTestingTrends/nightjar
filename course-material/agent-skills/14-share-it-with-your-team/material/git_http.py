"""Smart-HTTP git server on localhost for the plugin-sharing demo: hands every request to
`git http-backend` (read-only: receive-pack is off). usage: python3 git_http.py <root> <port>"""
import subprocess, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
ROOT, PORT = sys.argv[1], int(sys.argv[2])
BACKEND = subprocess.run(["git", "--exec-path"], capture_output=True, text=True).stdout.strip() + "/git-http-backend"

class H(BaseHTTPRequestHandler):
    def handle_one(self, method):
        u = urlsplit(self.path)
        body = self.rfile.read(int(self.headers.get("Content-Length") or 0)) if method == "POST" else b""
        env = {"GIT_PROJECT_ROOT": ROOT, "GIT_HTTP_EXPORT_ALL": "1", "PATH_INFO": u.path,
               "QUERY_STRING": u.query, "REQUEST_METHOD": method, "REMOTE_ADDR": "127.0.0.1",
               "CONTENT_TYPE": self.headers.get("Content-Type", ""), "CONTENT_LENGTH": str(len(body)),
               "GIT_PROTOCOL": self.headers.get("Git-Protocol", ""), "PATH": "/usr/bin:/bin"}
        out = subprocess.run([BACKEND], input=body, env=env, capture_output=True).stdout
        head, _, payload = out.partition(b"\r\n\r\n")
        status = 200
        hdrs = []
        for line in head.decode().split("\r\n"):
            k, _, v = line.partition(":")
            if k.lower() == "status": status = int(v.strip().split()[0])
            elif k: hdrs.append((k, v.strip()))
        self.send_response(status)
        for k, v in hdrs: self.send_header(k, v)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)
    def do_GET(self): self.handle_one("GET")
    def do_POST(self): self.handle_one("POST")
    def log_message(self, *a): pass

ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
