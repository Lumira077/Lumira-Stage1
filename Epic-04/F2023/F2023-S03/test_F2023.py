import unittest
from core import *
C=Context('u',1,'turn1')
ZERO={'neck':0,'arm':0,'waist':0}
def skin():return {'id':'lumira','version':'v1','color':'#64d9ff','states':sorted(SkinRegistry.REQUIRED),'rights':True}

class TestF2023(unittest.TestCase):
    def setUp(self):
        self.t=Timeline();self.gen=self.t.start(C)

    def test_due(self):
        self.t.add(C,self.gen,"face1","face",.5)
        self.assertEqual(self.t.due(C,self.gen,.4),[])
        self.assertEqual(self.t.due(C,self.gen,.5)[0]["channel"],"face")

    def test_exactly_once(self):
        self.t.add(C,self.gen,"face1","face",0);self.t.due(C,self.gen,0)
        self.assertEqual(self.t.due(C,self.gen,0),[])

    def test_duplicate(self):
        self.t.add(C,self.gen,"face1","face",0)
        with self.assertRaises(Rejected):self.t.add(C,self.gen,"face1","face",1)

    def test_foreign(self):
        with self.assertRaises(Rejected):self.t.add(Context("v",1,"turn1"),self.gen,"x","audio",0)

    def test_clock_reverse(self):
        self.t.due(C,self.gen,1)
        with self.assertRaises(Rejected):self.t.due(C,self.gen,.5)

    def test_cancel_flush(self):
        self.t.add(C,self.gen,"x","motion",1);r=self.t.cancel()
        self.assertEqual(self.t.queue,[]);self.assertFalse(r["physical_stop_confirmed"])
        with self.assertRaises(Rejected):self.t.due(C,self.gen,1)

    def test_cancel_block_new(self):
        self.t.cancel()
        with self.assertRaises(Rejected):self.t.start(Context("u",2,"turn2"))

    def test_ack_all(self):
        r=self.t.cancel();g=r["generation"]
        self.assertFalse(self.t.ack(g,"face"));self.assertFalse(self.t.ack(g,"audio"));self.assertTrue(self.t.ack(g,"motion"))
        self.assertGreater(self.t.start(Context("u",2,"turn2")),g)

    def test_late_ack(self):
        self.t.cancel()
        with self.assertRaises(Rejected):self.t.ack(self.gen,"audio")

    def test_late_cue(self):
        self.t.due(C,self.gen,1)
        with self.assertRaises(Rejected):self.t.add(C,self.gen,"late","face",.5)

    def test_unknown_channel(self):
        with self.assertRaises(Rejected):self.t.add(C,self.gen,"x","motor_raw",0)
