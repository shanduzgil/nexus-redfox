from pathlib import Path
import json,urllib.request,urllib.parse
from .utils import is_loopback_url
from .scanner import scan_project
from .graph import build_graph

class LocalAgent:
    def __init__(self,base_url,model,timeout=180,allow_remote=False):
        if not allow_remote and not is_loopback_url(base_url): raise ValueError("Remote agent URL is disabled by default")
        self.base_url=base_url.rstrip("/"); self.model=model; self.timeout=timeout
    def _post(self,path,payload):
        req=urllib.request.Request(self.base_url+path,data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=self.timeout) as r: return json.loads(r.read().decode("utf-8"))
    def ask(self,root,cfg,question,deep=False):
        scan=scan_project(root,cfg,deep); graph=build_graph(root,cfg);
        context={"scan":scan.to_dict(),"graph":graph.stats()}
        prompt="You are NEXUS, a local-first codebase analyst. Use only the supplied project facts. Do not claim a fix was applied. Ask for the file if exact code is needed.\nProject facts:\n"+json.dumps(context,ensure_ascii=False)+"\nUser request:\n"+question
        try:
            return self._post("/api/chat",{"model":self.model,"messages":[{"role":"user","content":prompt}],"stream":False})
        except Exception:
            return self._post("/api/generate",{"model":self.model,"prompt":prompt,"stream":False})
