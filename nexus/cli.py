import argparse,json,sys,os
from pathlib import Path
from . import __version__,RELEASE_CODENAME
from .config import Config
from .scanner import scan_project
from .graph import build_graph
from .reports import json_report,html_report,sarif_report
from .indexer import ProjectIndex
from .sbom import generate_spdx,generate_cyclonedx
from .manifest import make_manifest,verify_manifest
from .capsule import create_capsule,verify_capsule
from .gitops import summary,changed_files
from .utils import stable_id

def root_of(v):
    p=Path(v).expanduser().resolve()
    if not p.exists() or not p.is_dir(): raise SystemExit(f"Path is not a directory: {p}")
    return p

def cmd_init(args):
    r=root_of(args.path); cfg=Config.load(r); cfg.save(); print(r/".nexus/config.json"); return 0

def cmd_scan(args):
    r=root_of(args.path); cfg=Config.load(r); result=scan_project(r,cfg,args.deep); data={"json":json_report,"html":html_report,"sarif":sarif_report}[args.format](result)
    if args.out: Path(args.out).expanduser().resolve().write_text(data,encoding="utf-8"); print(args.out)
    else: print(data)
    return 1 if any(f.severity in ("critical","high") for f in result.findings) and args.fail_on_high else 0

def cmd_graph(args):
    r=root_of(args.path); g=build_graph(r,Config.load(r)); data=json.dumps(g.as_dict(),indent=2,ensure_ascii=False);
    if args.out: Path(args.out).write_text(data,encoding="utf-8"); print(args.out)
    else: print(data)
    return 0

def symbol_rows(r):
    idx=ProjectIndex(r); changed,removed=idx.update_files(Config.load(r),lambda p,rp: []); idx.close(); return changed,removed

def cmd_index(args):
    r=root_of(args.path); cfg=Config.load(r); idx=ProjectIndex(r); from .cli_helpers import extract_symbols; changed,removed=idx.update_files(cfg,extract_symbols); idx.close(); print(json.dumps({"changed":len(changed),"removed":len(removed)},ensure_ascii=False)); return 0

def cmd_search(args):
    r=root_of(args.path); idx=ProjectIndex(r); rows=idx.search(args.query); idx.close(); print(json.dumps([dict(id=a,kind=b,name=c,path=d,line=e) for a,b,c,d,e in rows],indent=2,ensure_ascii=False)); return 0

def cmd_impact(args):
    r=root_of(args.path); g=build_graph(r,Config.load(r)); needle=args.query.lower(); nodes=[n for n in g.nodes if needle in n.name.lower() or needle in n.path.lower() or needle==n.node_id.lower()]; ids={n.node_id for n in nodes}; hits=[]
    rev={e.target:[] for e in g.edges}
    for e in g.edges: rev.setdefault(e.target,[]).append(e.source)
    seen=set(ids); queue=list(ids)
    while queue:
        x=queue.pop();
        for src in rev.get(x,[]):
            if src not in seen: seen.add(src); queue.append(src)
    lookup={n.node_id:n for n in g.nodes}
    for x in seen: hits.append(lookup[x].to_dict())
    print(json.dumps({"query":args.query,"matches":[n.to_dict() for n in nodes],"affected":hits},indent=2,ensure_ascii=False)); return 0

def cmd_snapshot(args):
    r=root_of(args.path); m=make_manifest(r,Config.load(r)); out=Path(args.out) if args.out else r/".nexus"/"snapshot.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(m,indent=2,ensure_ascii=False),encoding="utf-8"); print(out); return 0

def cmd_verify(args):
    r=root_of(args.path); m=json.loads(Path(args.manifest).read_text(encoding="utf-8")); bad=verify_manifest(r,m); print(json.dumps({"valid":not bad,"failures":bad},indent=2,ensure_ascii=False)); return 1 if bad else 0

def cmd_sbom(args):
    r=root_of(args.path); d={"spdx":generate_spdx(r),"cyclonedx":generate_cyclonedx(r)}; data=json.dumps(d,indent=2,ensure_ascii=False);
    if args.out: Path(args.out).write_text(data,encoding="utf-8"); print(args.out)
    else: print(data)
    return 0

def cmd_capsule(args):
    r=root_of(args.path); out=Path(args.out).expanduser().resolve() if args.out else r/".nexus"/(r.name+".nexus.zip"); result,graph=create_capsule(r,Config.load(r),out,args.include_source,args.deep); print(json.dumps({"out":str(out),"files":result.files,"findings":len(result.findings),"graph":graph.stats()},ensure_ascii=False)); return 0

def cmd_capsule_verify(args): print(json.dumps(verify_capsule(Path(args.file).expanduser().resolve()),indent=2,ensure_ascii=False)); return 0

def cmd_ask(args):
    from .agent import LocalAgent
    r=root_of(args.path); cfg=Config.load(r); agent=LocalAgent(args.url or cfg.agent_url,args.model or cfg.agent_model,args.timeout or cfg.agent_timeout,args.allow_remote);
    try: result=agent.ask(r,cfg,args.question,args.deep); print(result.get("message",{}).get("content") or result.get("response") or json.dumps(result,ensure_ascii=False)); return 0
    except Exception as e: print(f"error: {e}",file=sys.stderr); return 2

def cmd_mcp(args): from .mcp import serve; serve(root_of(args.path)); return 0
def cmd_serve(args): from .web import serve; serve(root_of(args.path),args.host,args.port,args.allow_remote); return 0
def cmd_explain(args):
    from .playbook import explain
    print(json.dumps(explain(args.rule),indent=2,ensure_ascii=False))
    return 0

def cmd_doctor(args):
    import importlib.util
    r=root_of(args.path); g=build_graph(r,Config.load(r)); checks={"python":sys.version.split()[0],"git":bool((r/".git").exists()),"ollama_reachable":False,"graph":g.stats()};
    try:
        import urllib.request; urllib.request.urlopen((Config.load(r)).agent_url+"/api/tags",timeout=2); checks["ollama_reachable"]=True
    except Exception: pass
    print(json.dumps(checks,indent=2,ensure_ascii=False)); return 0

def parser():
    p=argparse.ArgumentParser(prog="nexus"); p.add_argument("--version",action="version",version=f"NEXUS {__version__} {RELEASE_CODENAME}"); sp=p.add_subparsers(dest="cmd",required=True)
    x=sp.add_parser("init"); x.add_argument("path",nargs="?",default="."); x.set_defaults(fn=cmd_init)
    x=sp.add_parser("scan"); x.add_argument("path",nargs="?",default="."); x.add_argument("--format",choices=["html","json","sarif"],default="html"); x.add_argument("--out"); x.add_argument("--deep",action="store_true"); x.add_argument("--fail-on-high",action="store_true"); x.set_defaults(fn=cmd_scan)
    x=sp.add_parser("graph"); x.add_argument("path",nargs="?",default="."); x.add_argument("--out"); x.set_defaults(fn=cmd_graph)
    x=sp.add_parser("index"); x.add_argument("path",nargs="?",default="."); x.set_defaults(fn=cmd_index)
    x=sp.add_parser("search"); x.add_argument("query"); x.add_argument("path",nargs="?",default="."); x.set_defaults(fn=cmd_search)
    x=sp.add_parser("impact"); x.add_argument("query"); x.add_argument("path",nargs="?",default="."); x.set_defaults(fn=cmd_impact)
    x=sp.add_parser("snapshot"); x.add_argument("path",nargs="?",default="."); x.add_argument("--out"); x.set_defaults(fn=cmd_snapshot)
    x=sp.add_parser("verify"); x.add_argument("manifest"); x.add_argument("path",nargs="?",default="."); x.set_defaults(fn=cmd_verify)
    x=sp.add_parser("sbom"); x.add_argument("path",nargs="?",default="."); x.add_argument("--out"); x.set_defaults(fn=cmd_sbom)
    x=sp.add_parser("capsule"); x.add_argument("path",nargs="?",default="."); x.add_argument("--out"); x.add_argument("--include-source",action="store_true"); x.add_argument("--deep",action="store_true"); x.set_defaults(fn=cmd_capsule)
    x=sp.add_parser("capsule-verify"); x.add_argument("file"); x.set_defaults(fn=cmd_capsule_verify)
    x=sp.add_parser("serve"); x.add_argument("path",nargs="?",default="."); x.add_argument("--host",default="127.0.0.1"); x.add_argument("--port",type=int,default=8765); x.add_argument("--allow-remote",action="store_true"); x.set_defaults(fn=cmd_serve)
    x=sp.add_parser("ask"); x.add_argument("question"); x.add_argument("path",nargs="?",default="."); x.add_argument("--model"); x.add_argument("--url"); x.add_argument("--timeout",type=int); x.add_argument("--allow-remote",action="store_true"); x.add_argument("--deep",action="store_true"); x.set_defaults(fn=cmd_ask)
    x=sp.add_parser("mcp"); x.add_argument("path",nargs="?",default="."); x.set_defaults(fn=cmd_mcp)
    x=sp.add_parser("explain"); x.add_argument("rule"); x.set_defaults(fn=cmd_explain)
    x=sp.add_parser("doctor"); x.add_argument("path",nargs="?",default="."); x.set_defaults(fn=cmd_doctor)
    x=sp.add_parser("git-summary"); x.add_argument("path",nargs="?",default="."); x.set_defaults(fn=lambda a: (print(json.dumps(summary(root_of(a.path)),indent=2,ensure_ascii=False)) or 0))
    return p

def main(argv=None):
    try: args=parser().parse_args(argv); return args.fn(args)
    except KeyboardInterrupt: return 130
    except BrokenPipeError: return 0
    except Exception as e: print(f"error: {e}",file=sys.stderr); return 2

if __name__=="__main__": raise SystemExit(main())
