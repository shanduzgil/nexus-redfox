import ast
from .utils import stable_id

def extract_symbols(path,rp):
    text=path.read_text(encoding="utf-8",errors="ignore")
    out=[]
    if path.suffix==".py":
        try: tree=ast.parse(text)
        except SyntaxError: return out
        for n in ast.walk(tree):
            if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                kind="class" if isinstance(n,ast.ClassDef) else "function"; out.append(("sym:"+stable_id(rp,kind,n.name,n.lineno),kind,n.name,rp,n.lineno))
        return out
    patterns=[(r"(?m)^\s*(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_$][\w$]*)","function"),(r"(?m)^\s*(?:export\s+)?class\s+([A-Za-z_$][\w$]*)","class"),(r"(?m)^\s*func\s+(?:\([^)]*\)\s*)?([A-Za-z_]\w*)","function"),(r"(?m)^\s*(?:pub\s+)?fn\s+([A-Za-z_]\w*)","function"),(r"(?m)^\s*(?:public|private|protected)?\s*(?:static\s+)?[\w<>\[\]]+\s+([A-Za-z_]\w*)\s*\([^;]*\)\s*\{","method")]
    for pat,kind in patterns:
        for m in __import__('re').finditer(pat,text):
            line=text.count("\n",0,m.start())+1; name=m.group(1); out.append(("sym:"+stable_id(rp,kind,name,line),kind,name,rp,line))
    return out
