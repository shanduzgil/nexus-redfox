import tempfile
import unittest
from pathlib import Path
from nexus.config import Config
from nexus.graph import build_graph

class TestGraph(unittest.TestCase):
    def test_python_symbols(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/"a.py").write_text('class A:\n    def run(self):\n        return 1\n',encoding="utf-8")
            g=build_graph(root,Config(root))
            self.assertTrue(any(n.kind=="class" for n in g.nodes))
            self.assertTrue(any(n.kind=="function" for n in g.nodes))

if __name__=="__main__": unittest.main()
