from pathlib import Path
import json,datetime,hashlib
from .utils import sha256_file,iter_files,rel,safe_json_write

def make_manifest(root, cfg):
    entries=[]
    for p,_ in iter_files(root,cfg): entries.append({"path":rel(p,root),"sha256":sha256_file(p),"size":p.stat().st_size})
    payload={"format":"nexus-manifest-1","project":root.name,"created":datetime.datetime.now(datetime.timezone.utc).isoformat(),"files":entries}
    payload["root_hash"]=hashlib.sha256("".join(x["path"]+x["sha256"] for x in entries).encode()).hexdigest()
    return payload

def write_manifest(root,cfg,out): safe_json_write(out,make_manifest(root,cfg))

def verify_manifest(root,manifest):
    failures=[]
    for e in manifest.get("files",[]):
        p=root/e["path"]
        if not p.exists(): failures.append({"path":e["path"],"reason":"missing"}); continue
        got=sha256_file(p)
        if got!=e["sha256"]: failures.append({"path":e["path"],"reason":"hash_mismatch","expected":e["sha256"],"actual":got})
    return failures
