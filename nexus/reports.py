from pathlib import Path
import html,json
from .models import ScanResult

def json_report(result): return json.dumps(result.to_dict(),indent=2,ensure_ascii=False)
def sarif_report(result):
    rules={}; results=[]
    for f in result.findings:
        rules[f.rule_id]={"id":f.rule_id,"name":f.title,"shortDescription":{"text":f.title},"fullDescription":{"text":f.message},"help":{"text":f.remediation},"properties":{"severity":f.severity,"cwe":f.cwe}}
        results.append({"ruleId":f.rule_id,"level":{"critical":"error","high":"error","medium":"warning","low":"note","info":"note"}.get(f.severity,"warning"),"message":{"text":f.message},"locations":[{"physicalLocation":{"artifactLocation":{"uri":f.path},"region":{"startLine":max(1,f.line),"startColumn":max(1,f.column)}}}]})
    d={"$schema":"https://json.schemastore.org/sarif-2.1.0.json","version":"2.1.0","runs":[{"tool":{"driver":{"name":"NEXUS","version":"0.2.0","rules":list(rules.values())}},"results":results}]}
    return json.dumps(d,indent=2,ensure_ascii=False)
def html_report(result):
    d=result.to_dict(); cards="".join(f"<section><span>{html.escape(k.upper())}</span><strong>{d['counts'][k]}</strong></section>" for k in ("critical","high","medium","low","info")); rows="".join(f"<tr><td>{html.escape(f['severity'].upper())}</td><td>{html.escape(f['rule_id'])}</td><td>{html.escape(f['title'])}</td><td>{html.escape(f['path'])}:{f['line']}</td><td>{html.escape(f['message'])}</td></tr>" for f in d["findings"]) or "<tr><td colspan=5>No findings</td></tr>"
    return f"<!doctype html><html><head><meta charset=utf-8><meta name=viewport content=width=device-width,initial-scale=1><title>NEXUS report</title><style>body{{font:14px system-ui;background:#07100d;color:#eaf7ef;margin:0;padding:28px}}main{{max-width:1500px;margin:auto}}.grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}}section{{background:#0e1c16;border:1px solid #1d3a2d;padding:16px;border-radius:16px}}section span{{display:block;opacity:.7}}section strong{{font-size:32px}}table{{width:100%;border-collapse:collapse;margin-top:18px;background:#0e1c16}}th,td{{padding:10px;border-bottom:1px solid #1d3a2d;text-align:left;vertical-align:top}}@media(max-width:800px){{.grid{{grid-template-columns:repeat(2,1fr)}}}}</style></head><body><main><h1>NEXUS Security Report</h1><p>{html.escape(result.root)} · {result.files} files · {result.duration_ms} ms · {html.escape(result.mode)}</p><div class=grid>{cards}</div><table><thead><tr><th>Severity</th><th>Rule</th><th>Title</th><th>Location</th><th>Message</th></tr></thead><tbody>{rows}</tbody></table></main></body></html>"
