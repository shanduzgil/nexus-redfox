import tempfile
import unittest
from pathlib import Path
from nexus.config import Config
from nexus.manifest import make_manifest,verify_manifest

class TestManifest(unittest.TestCase):
    def test_verify(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/"x.txt").write_text("ok",encoding="utf-8"); m=make_manifest(root,Config(root)); self.assertFalse(verify_manifest(root,m)); (root/"x.txt").write_text("bad",encoding="utf-8"); self.assertTrue(verify_manifest(root,m))

if __name__=="__main__": unittest.main()
