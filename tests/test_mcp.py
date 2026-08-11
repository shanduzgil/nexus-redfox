import tempfile
import unittest
from pathlib import Path
from nexus.mcp import result

class TestMcp(unittest.TestCase):
    def test_init(self):
        with tempfile.TemporaryDirectory() as d:
            x=result("initialize",Path(d),{})
            self.assertEqual(x["serverInfo"]["name"],"nexus")

if __name__=="__main__": unittest.main()
