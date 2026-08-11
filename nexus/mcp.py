import sys,json
from pathlib import Path
from .scanner import scan_project
from .graph import build_graph
from .config import Config
from .indexer import ProjectIndex
from .sbom import generate_spdx,generate_cyclonedx
from .playbook import explain

def result(method,root,params):
    cfg=Config.load(root)
    if method=="initialize": return {"protocolVersion":"2024-11-05","capabilities":{"tools":{"listChanged":False}},"serverInfo":{"name":"nexus","version":"0.2.0"}}
    if method=="ping": return {}
    if method=="tools/list": return {"tools":[{"name":"nexus_scan","description":"Deterministic local scan","inputSchema":{"type":"object","properties":{"deep":{"type":"boolean"}}}},{"name":"nexus_graph","description":"Project architecture graph","inputSchema":{"type":"object","properties":{}}},{"name":"nexus_search","description":"Search indexed symbols","inputSchema":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"]}},{"name":"nexus_sbom","description":"Generate SPDX and CycloneDX SBOM","inputSchema":{"type":"object","properties":{}}},{"name":"nexus_explain","description":"Explain a security rule with local remediation guidance","inputSchema":{"type":"object","properties":{"rule":{"type":"string"}},"required":["rule"]}}]}
    if method=="tools/call":
        name=params.get("name"); args=params.get("arguments") or {}
        if name=="nexus_scan": payload=scan_project(root,cfg,bool(args.get("deep"))); return {"content":[{"type":"text","text":json.dumps(payload.to_dict(),ensure_ascii=False)}]}
        if name=="nexus_graph": payload=build_graph(root,cfg); return {"content":[{"type":"text","text":json.dumps(payload.as_dict(),ensure_ascii=False)}]}
        if name=="nexus_search":
            idx=ProjectIndex(root); rows=idx.search(str(args.get("query",""))); idx.close(); return {"content":[{"type":"text","text":json.dumps([dict(id=r[0],kind=r[1],name=r[2],path=r[3],line=r[4]) for r in rows],ensure_ascii=False)}]}
        if name=="nexus_sbom": return {"content":[{"type":"text","text":json.dumps({"spdx":generate_spdx(root),"cyclonedx":generate_cyclonedx(root)},ensure_ascii=False)}]}
        if name=="nexus_explain": return {"content":[{"type":"text","text":json.dumps(explain(str(args.get("rule",""))),ensure_ascii=False)}]}
        return {"isError":True,"content":[{"type":"text","text":"Unknown tool"}]}
    return None

def serve(root):
    for line in sys.stdin:
        if not line.strip(): continue
        rid=None
        try:
            msg=json.loads(line); rid=msg.get("id"); val=result(msg.get("method"),root,msg.get("params") or {});
            if rid is not None: sys.stdout.write(json.dumps({"jsonrpc":"2.0","id":rid,"result":val},ensure_ascii=False,separators=(",",":"))+"\n"); sys.stdout.flush()
        except Exception as e:
            if rid is not None: sys.stdout.write(json.dumps({"jsonrpc":"2.0","id":rid,"error":{"code":-32000,"message":str(e)}},ensure_ascii=False)+"\n"); sys.stdout.flush()
