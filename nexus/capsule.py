from pathlib import Path
import json,zipfile,hashlib,tempfile,shutil
from .reports import json_report,sarif_report
from .manifest import make_manifest
from .sbom import generate_spdx,generate_cyclonedx
from .graph import build_graph
from .scanner import scan_project

def create_capsule(root,cfg,out,include_source=False,deep=False):
    result=scan_project(root,cfg,deep); graph=build_graph(root,cfg); manifest=make_manifest(root,cfg); spdx=generate_spdx(root); cdx=generate_cyclonedx(root)
    with tempfile.TemporaryDirectory() as d:
        t=Path(d)
        (t/"scan.json").write_text(json_report(result),encoding="utf-8")
        (t/"scan.sarif.json").write_text(sarif_report(result),encoding="utf-8")
        (t/"graph.json").write_text(json.dumps(graph.as_dict(),indent=2,ensure_ascii=False),encoding="utf-8")
        (t/"sbom.spdx.json").write_text(json.dumps(spdx,indent=2,ensure_ascii=False),encoding="utf-8")
        (t/"sbom.cyclonedx.json").write_text(json.dumps(cdx,indent=2,ensure_ascii=False),encoding="utf-8")
        (t/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding="utf-8")
        (t/"release.txt").write_text("NEXUS 0.2.0 REDFOX\n",encoding="utf-8")
        if include_source:
            src=t/"source"; src.mkdir()
            for p,_ in __import__('nexus.utils',fromlist=['iter_files']).iter_files(root,cfg):
                rp=p.relative_to(root); dest=src/rp; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,dest)
        checks=[]
        for p in sorted(t.rglob("*")):
            if p.is_file(): checks.append(hashlib.sha256(p.read_bytes()).hexdigest()+"  "+p.relative_to(t).as_posix())
        (t/"checksums.sha256").write_text("\n".join(checks)+"\n",encoding="utf-8")
        out.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(out,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for p in sorted(t.rglob("*")):
                if p.is_file(): z.write(p,p.relative_to(t).as_posix())
    return result,graph

def verify_capsule(path):
    with zipfile.ZipFile(path) as z:
        names=set(z.namelist()); checks=z.read("checksums.sha256").decode().splitlines(); bad=[]
        for line in checks:
            if not line.strip(): continue
            digest,name=line.split("  ",1); data=z.read(name); got=hashlib.sha256(data).hexdigest();
            if got!=digest: bad.append(name)
        return {"valid":not bad,"bad":bad,"files":len(names)}
