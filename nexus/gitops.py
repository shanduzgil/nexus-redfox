from pathlib import Path
from .utils import run_cmd

def summary(root):
    if not (root/".git").exists(): return {"available":False}
    _,branch,_=run_cmd(["git","branch","--show-current"],cwd=root); rc,sha,_=run_cmd(["git","rev-parse","HEAD"],cwd=root); _,status,_=run_cmd(["git","status","--short"],cwd=root)
    return {"available":rc==0,"branch":branch.strip(),"commit":sha.strip(),"clean":status.strip()==""}

def changed_files(root):
    rc,out,err=run_cmd(["git","diff","--name-only","HEAD"],cwd=root)
    return out.splitlines() if rc==0 else [err.strip()]
