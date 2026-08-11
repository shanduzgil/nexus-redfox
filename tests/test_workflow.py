import tempfile
import unittest
from pathlib import Path
from nexus.workflows import scan_workflow

class TestWorkflow(unittest.TestCase):
    def test_permissions(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); p=root/".github/workflows/a.yml"; p.parent.mkdir(parents=True); p.write_text("name: x\non: push\njobs: {}\n",encoding="utf-8")
            ids={x.rule_id for x in scan_workflow(p,root)}
            self.assertIn("NXS115",ids)

if __name__=="__main__": unittest.main()
