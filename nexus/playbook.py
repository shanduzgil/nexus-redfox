from pathlib import Path
import json

def explain(rule_id):
    p=Path(__file__).resolve().parent/"data"/"remediation_playbook.json"
    data=json.loads(p.read_text(encoding="utf-8"))
    hits=[x for x in data if x["rule_id"]==rule_id]
    return hits[:12]
