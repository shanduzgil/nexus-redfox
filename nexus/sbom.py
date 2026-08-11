from pathlib import Path
import json,re,uuid

def _deps(root):
    out=[]
    p=root/"package.json"
    if p.exists():
        try:
            d=json.loads(p.read_text(encoding="utf-8"));
            for group in ("dependencies","devDependencies","optionalDependencies"):
                for n,v in (d.get(group) or {}).items(): out.append(("npm",n,str(v)))
        except ValueError: pass
    for name in ("requirements.txt","requirements-dev.txt"):
        p=root/name
        if p.exists():
            for line in p.read_text(encoding="utf-8",errors="ignore").splitlines():
                s=line.strip(); m=re.match(r"^([A-Za-z0-9_.-]+)\s*([=!<>~].*)?$",s)
                if m and not s.startswith("#"): out.append(("pypi",m.group(1),m.group(2) or ""))
    p=root/"pyproject.toml"
    if p.exists():
        t=p.read_text(encoding="utf-8",errors="ignore")
        in_dep=False
        for line in t.splitlines():
            if line.strip().startswith("dependencies = ["): in_dep=True; continue
            if in_dep and line.strip().startswith("]"): in_dep=False; continue
            if in_dep:
                x=line.strip().strip(',').strip('"')
                m=re.match(r"^([A-Za-z0-9_.-]+)",x)
                if m: out.append(("pypi",m.group(1),x[len(m.group(1)):].strip()))
    p=root/"go.mod"
    if p.exists():
        for line in p.read_text(encoding="utf-8",errors="ignore").splitlines():
            m=re.match(r"^\s*([A-Za-z0-9./_-]+)\s+(v[0-9][^\s]*)",line);
            if m: out.append(("go",m.group(1),m.group(2)))
    p=root/"Cargo.toml"
    if p.exists():
        section=False
        for line in p.read_text(encoding="utf-8",errors="ignore").splitlines():
            if line.strip()=="[dependencies]": section=True; continue
            if line.strip().startswith("[") and line.strip()!="[dependencies]": section=False
            if section:
                m=re.match(r"^\s*([A-Za-z0-9_-]+)\s*=\s*(.+)$",line)
                if m: out.append(("crates",m.group(1),m.group(2).strip()))
    return out

def generate_spdx(root):
    deps=_deps(root); doc="SPDXRef-DOCUMENT"; packages=[]; relationships=[]
    for i,(eco,name,ver) in enumerate(sorted(set(deps))):
        sid=f"SPDXRef-Package-{i}"; packages.append({"SPDXID":sid,"name":name,"versionInfo":ver,"downloadLocation":"NOASSERTION","filesAnalyzed":False,"supplier":"NOASSERTION","licenseConcluded":"NOASSERTION","licenseDeclared":"NOASSERTION"}); relationships.append({"spdxElementId":doc,"relationshipType":"DESCRIBES","relatedSpdxElement":sid})
    return {"spdxVersion":"SPDX-2.3","dataLicense":"CC0-1.0","SPDXID":doc,"name":root.name+"-nexus-sbom","documentNamespace":"https://nexus.local/spdx/"+str(uuid.uuid4()),"creationInfo":{"created":__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),"creators":["Tool: NEXUS 0.2.0"]},"packages":packages,"relationships":relationships}

def generate_cyclonedx(root):
    deps=_deps(root); comps=[]
    for eco,name,ver in sorted(set(deps)):
        purl_map={"npm":"pkg:npm/","pypi":"pkg:pypi/","go":"pkg:golang/","crates":"pkg:cargo/"}; base=purl_map.get(eco,"pkg:generic/"); comps.append({"type":"library","name":name,"version":ver or "UNKNOWN","purl":base+name+("@"+ver if ver and not ver.startswith(('^','~','>','<','=')) else "")})
    return {"bomFormat":"CycloneDX","specVersion":"1.6","version":1,"metadata":{"timestamp":__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),"tools":[{"vendor":"Shanduzgil","name":"NEXUS","version":"0.2.0"}]},"components":comps}
