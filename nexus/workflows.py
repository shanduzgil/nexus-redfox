from pathlib import Path
from .models import Finding
from .utils import rel,stable_id

def scan_workflow(path,root):
    if ".github" not in path.parts or "workflows" not in path.parts or path.suffix.lower() not in (".yml",".yaml"): return []
    text=path.read_text(encoding="utf-8",errors="ignore")
    out=[]; rp=rel(path,root)
    if "permissions:" not in text:
        out.append(Finding("NXS115","medium","Missing GitHub Actions permissions","Workflow does not declare explicit token permissions",rp,1,1,stable_id("NXS115",rp),"medium","CWE-732","Declare least-privilege workflow permissions"))
    if "pull_request_target:" in text and "actions/checkout@" in text:
        out.append(Finding("NXS116A","high","Privileged fork checkout","A pull_request_target workflow uses checkout and needs a trust-boundary review",rp,1,1,stable_id("NXS116A",rp),"high","Avoid checking out untrusted fork code in a privileged workflow"))
    return out
