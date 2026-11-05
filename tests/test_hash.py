import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from evidence_hash import inventory,verify
class HashTests(unittest.TestCase):
 def test_modify_detected(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);(root/'evidence.txt').write_text('before')
   manifest=inventory(root)
   self.assertFalse(verify(root,manifest))
   (root/'evidence.txt').write_text('after')
   self.assertEqual(verify(root,manifest)[0]['status'],'modified')
if __name__=='__main__':unittest.main()
