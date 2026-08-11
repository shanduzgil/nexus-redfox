import tempfile
import unittest
from pathlib import Path
from nexus.config import Config
from nexus.scanner import scan_project

class TestScanner(unittest.TestCase):
    def test_secret_and_shell(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"a.py").write_text('token="ghp_abcdefghijklmnopqrstuvwxyz1234567890"\nimport subprocess\nsubprocess.run(x,shell=True)\n',encoding="utf-8")
            r=scan_project(root,Config(root))
            ids={x.rule_id for x in r.findings}
            self.assertIn("NXS003",ids)
            self.assertIn("NXS101",ids)

if __name__=="__main__": unittest.main()
