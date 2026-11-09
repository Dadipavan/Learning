import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.spines.top": False, "axes.spines.right": False})
B, O, T, R, P = "#2b4fd6", "#b84a22", "#357a70", "#aa2d26", "#6a2fd0"

import os, threading, time, requests
os.environ["NO_PROXY"] = "127.0.0.1"
from http.server import BaseHTTPRequestHandler, HTTPServer
class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    def do_GET(self):
        b = b'{"ok": true}'
        self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def log_message(self, *a): pass
srv = HTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{srv.server_port}/"
N = 300
def bare():
    t0 = time.perf_counter()
    for _ in range(N):
        s = requests.Session(); s.trust_env = False; s.get(url); s.close()
    return (time.perf_counter() - t0) * 1000
def shared():
    s = requests.Session(); s.trust_env = False
    t0 = time.perf_counter()
    for _ in range(N):
        s.get(url)
    return (time.perf_counter() - t0) * 1000
a, b = bare(), shared(); srv.shutdown()
fig, ax = plt.subplots(figsize=(8, 4.2), dpi=110)
bars = ax.bar(["new connection each call", "one shared Session"], [a, b], color=[R, T])
for bb, v in zip(bars, [a, b]):
    ax.text(bb.get_x() + bb.get_width() / 2, v, f"{v:.0f} ms", ha="center", va="bottom")
ax.set_ylabel(f"time for {N} GET calls (ms)")
ax.set_ylim(0, max(a, b) * 1.15)
ax.set_title("Reusing connections (local server, measured, varies)")
fig.tight_layout(); fig.savefig("lib20_session.png")
