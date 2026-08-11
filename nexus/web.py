from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
import json,urllib.parse
from .config import Config
from .scanner import scan_project
from .graph import build_graph
from .sbom import generate_spdx,generate_cyclonedx
from .indexer import ProjectIndex

WEB=Path(__file__).resolve().parent.parent/"web"

class Handler(BaseHTTPRequestHandler):
    root=Path("."); cfg=None
    def _send(self,status,ctype,data):
        b=data if isinstance(data,bytes) else data.encode(); self.send_response(status); self.send_header("Content-Type",ctype); self.send_header("Content-Length",str(len(b))); self.send_header("Cache-Control","no-store"); self.send_header("X-Content-Type-Options","nosniff"); self.send_header("X-Frame-Options","DENY"); self.send_header("Content-Security-Policy","default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'"); self.end_headers(); self.wfile.write(b)
    def _json(self,obj,status=200): self._send(status,"application/json; charset=utf-8",json.dumps(obj,ensure_ascii=False))
    def do_GET(self):
        u=urllib.parse.urlparse(self.path); path=u.path; q=urllib.parse.parse_qs(u.query)
        try:
            if path=="/api/scan": return self._json(scan_project(self.root,self.cfg,q.get("deep",["0"])[0]=="1").to_dict())
            if path=="/api/graph": return self._json(build_graph(self.root,self.cfg).as_dict())
            if path=="/api/sbom": return self._json({"spdx":generate_spdx(self.root),"cyclonedx":generate_cyclonedx(self.root)})
            if path=="/api/search":
                idx=ProjectIndex(self.root); rows=idx.search(q.get("q",[""])[0]); idx.close(); return self._json([dict(id=r[0],kind=r[1],name=r[2],path=r[3],line=r[4]) for r in rows])
            if path=="/": return self._static("index.html","text/html; charset=utf-8")
            if path in ("/app.js","/styles.css"): return self._static(path.lstrip("/"),"text/javascript; charset=utf-8" if path.endswith(".js") else "text/css; charset=utf-8")
            return self._json({"error":"not_found"},404)
        except Exception as e:
            return self._json({"error":str(e)},500)
    def _static(self,name,ctype):
        p=WEB/name
        if not p.exists(): return self._json({"error":"not_found"},404)
        return self._send(200,ctype,p.read_bytes())
    def log_message(self,*args): return

def serve(root,host="127.0.0.1",port=8765,allow_remote=False):
    if not allow_remote and host not in ("127.0.0.1","localhost","::1"): raise ValueError("Remote dashboard is disabled by default")
    Handler.root=Path(root).resolve(); Handler.cfg=Config.load(Handler.root); srv=ThreadingHTTPServer((host,port),Handler); print(f"NEXUS dashboard http://{host}:{port}",flush=True); srv.serve_forever()
