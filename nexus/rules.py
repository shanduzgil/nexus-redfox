from pathlib import Path
import json, re
from importlib.resources import files

class Rule: 
    __slots__=("id","severity","title","message","pattern","needles","extensions","languages","cwe","confidence","remediation")
    def __init__(self,d):
        self.id=d["id"]; self.severity=d["severity"]; self.title=d["title"]; self.message=d["message"]; self.pattern=d["pattern"]; self.needles=tuple(d.get("needles",[])); self.extensions=tuple(d.get("extensions",[])); self.languages=tuple(d.get("languages",[])); self.cwe=d.get("cwe",""); self.confidence=d.get("confidence","medium"); self.remediation=d.get("remediation","")
    def regex(self): return re.compile(self.pattern,re.I|re.M)

def load_rules(deep=False):
    p=Path(__file__).resolve().parent/"data"/"rulepack.json"
    data=json.loads(p.read_text(encoding="utf-8"))
    rules=[]
    for d in data:
        if not deep and not d.get("active",True): continue
        rules.append(Rule(d))
    return rules
