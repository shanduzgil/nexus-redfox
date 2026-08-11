from pathlib import Path
import ast,re,json
from .models import Node,Edge
from .utils import iter_files,read_text,rel,stable_id,file_language

class ProjectGraph:
    def __init__(self): self.nodes=[]; self.edges=[]
    def as_dict(self): return {"nodes":[n.to_dict() for n in self.nodes],"edges":[e.to_dict() for e in self.edges]}
    def stats(self): return {"nodes":len(self.nodes),"edges":len(self.edges),"files":sum(n.kind=="file" for n in self.nodes),"symbols":sum(n.kind in ("class","function","method","symbol") for n in self.nodes)}

def _python(p,text,relpath,file_id):
    nodes=[]; edges=[]
    try: tree=ast.parse(text,filename=relpath)
    except SyntaxError: return nodes,edges
    stack=[file_id]
    for n in ast.walk(tree):
        if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
            kind="class" if isinstance(n,ast.ClassDef) else "function"; nid="sym:"+stable_id(relpath,kind,n.name,n.lineno); nodes.append(Node(nid,kind,n.name,relpath,n.lineno,{})); edges.append(Edge(file_id,nid,"contains"))
        if isinstance(n,(ast.Import,ast.ImportFrom)):
            for a in getattr(n,"names",[]):
                mod=a.name.split(".")[0]
                edges.append(Edge(file_id,"module:"+mod,"imports",{}))
    return nodes,edges

def build_graph(root:Path,cfg):
    g=ProjectGraph(); files={}; module_nodes={}
    for p,_ in iter_files(root,cfg):
        rp=rel(p,root); fid="file:"+stable_id(rp); files[rp]=fid; g.nodes.append(Node(fid,"file",p.name,rp,1,{"size":p.stat().st_size,"language":file_language(p)}))
        stem=p.stem; module_nodes.setdefault(stem,[]).append((rp,fid))
    for p,_ in iter_files(root,cfg):
        rp=rel(p,root); fid=files[rp]; text=read_text(p)
        if p.suffix==".py": ns,es=_python(p,text,rp,fid); g.nodes.extend(ns); g.edges.extend(es)
        patterns=[(r"(?m)^\s*(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_$][\w$]*)", "function"),(r"(?m)^\s*(?:export\s+)?class\s+([A-Za-z_$][\w$]*)", "class"),(r"(?m)^\s*func\s+(?:\([^)]*\)\s*)?([A-Za-z_]\w*)", "function"),(r"(?m)^\s*(?:pub\s+)?fn\s+([A-Za-z_]\w*)", "function"),(r"(?m)^\s*(?:public|private|protected)?\s*(?:static\s+)?[\w<>\[\]]+\s+([A-Za-z_]\w*)\s*\([^;]*\)\s*\{", "method")]
        for pat,kind in patterns:
            for m in re.finditer(pat,text):
                name=m.group(1); line=text.count("\n",0,m.start())+1; nid="sym:"+stable_id(rp,kind,name,line); g.nodes.append(Node(nid,kind,name,rp,line,{"language":file_language(p)})); g.edges.append(Edge(fid,nid,"contains"))
        for m in re.finditer(r"(?m)^\s*(?:import|from)\s+([A-Za-z0-9_./:@-]+)",text):
            mod=m.group(1).split("/")[-1].split(".")[0];
            if mod in module_nodes:
                target=module_nodes[mod][0][1]; g.edges.append(Edge(fid,target,"imports"))
    dedup={(e.source,e.target,e.kind):e for e in g.edges}; g.edges=list(dedup.values())
    return g
