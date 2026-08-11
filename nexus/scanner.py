from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import math, re
from .models import Finding,ScanResult
from .config import Config
from .rules import load_rules
from .utils import iter_files,read_text,now_ms,rel,stable_id,file_language
from .indexer import ProjectIndex
from .workflows import scan_workflow

def entropy(s):
    if not s: return 0.0
    n=len(s); counts={c:s.count(c) for c in set(s)}
    return -sum((v/n)*math.log2(v/n) for v in counts.values())

def _apply_rules(p,root,rules):
    text=read_text(p)
    if not text: return []
    lang=file_language(p); ext=p.suffix.lower(); out=[]
    for rule in rules:
        if rule.extensions and ext not in rule.extensions and lang not in rule.languages: continue
        if rule.languages and lang not in rule.languages and not rule.extensions: continue
        if rule.needles and not any(x.lower() in text.lower() for x in rule.needles): continue
        try: rx=rule.regex()
        except re.error: continue
        for m in rx.finditer(text):
            line,col=_linecol(text,m.start()); value=m.group(0)[:240]
            if rule.id.startswith("NXS0") and any(x in value.lower() for x in ("example","placeholder","changeme","dummy","your_","replace_me")): continue
            fp=stable_id(rule.id,rel(p,root),line,col)
            out.append(Finding(rule.id,rule.severity,rule.title,rule.message.replace("{match}",value),rel(p,root),line,col,fp,rule.confidence,rule.cwe,rule.remediation,{}))
    return out

def _linecol(text,pos):
    line=text.count("\n",0,pos)+1; last=text.rfind("\n",0,pos); return line,pos-last

def scan_project(root:Path,cfg=None,deep=False):
    root=root.resolve(); cfg=cfg or Config.load(root); started=now_ms(); result=ScanResult(str(root),mode="deep" if deep else "fast")
    rules=load_rules(deep); items=list(iter_files(root,cfg)); result.files=len(items)
    results=[]
    workers=cfg.workers or min(32,max(4,(os_cpu:=__import__('os').cpu_count() or 4)*2))
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs=[ex.submit(lambda x: _apply_rules(x,root,rules)+scan_workflow(x,root),p) for p,_ in items]
        for fut in as_completed(futs):
            try: results.extend(fut.result()); result.scanned_files+=1
            except Exception: result.skipped_files+=1
    result.findings=sorted(results,key=lambda f:(f.severity,f.path,f.line),reverse=False); result.duration_ms=now_ms()-started
    return result
