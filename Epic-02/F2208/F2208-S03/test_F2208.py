import unittest
from core import *

class TestF2208(unittest.TestCase):
    def setUp(self):
        self.now=10;self.items=[{"owner":"a","id":"a1","text":"likes music","confirmed":True,"expires":20,"cloud_share":False},{"owner":"b","id":"b1","text":"likes music","confirmed":True,"expires":20,"cloud_share":True}];self.s=LocalContext(self.items,lambda:self.now)

    def test_own(self):
        self.assertEqual(self.s.search("a","music")[0]["id"],"a1")

    def test_foreign(self):
        self.assertEqual(self.s.search("c","music"),[])

    def test_unshared_cloud(self):
        self.assertEqual(self.s.search("a","music",True),[])

    def test_expiry(self):
        self.now=20;self.assertEqual(self.s.search("a","music"),[])

    def test_unconfirmed(self):
        self.s.items[0]["confirmed"]=False;self.assertEqual(self.s.search("a","music"),[])

    def test_no_match(self):
        self.assertEqual(self.s.search("a","weather"),[])
