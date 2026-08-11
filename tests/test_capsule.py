import tempfile
import unittest
from pathlib import Path
from nexus.config import Config
from nexus.capsule import create_capsule,verify_capsule

class TestCapsule(unittest.TestCase):
    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/"a.py").write_text('print(1)\n',encoding="utf-8"); out=root/"x.zip"
            create_capsule(root,Config(root),out)
            self.assertTrue(verify_capsule(out)["valid"])

if __name__=="__main__": unittest.main()
