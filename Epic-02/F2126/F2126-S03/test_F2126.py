import unittest
from core import *

class TestF2126(unittest.TestCase):
    def setUp(self):
        self.s=AudioLab()

    def test_mean_beam(self):
        self.assertEqual(self.s.beam([[.2,.4],[.4,.6]]),[.30000000000000004,.5])

    def test_reference_subtraction(self):
        self.assertEqual(self.s.subtract_reference([.5],[.4]),[.3])

    def test_frame_mismatch(self):
        self.assertRaises(Rejected,self.s.beam,[[.1],[.2,.3]])

    def test_nan(self):
        self.assertRaises(Rejected,self.s.pcm,[float("nan")])

    def test_zero_doa(self):
        self.assertEqual(self.s.doa(0,16000,.05),0)

    def test_impossible_delay(self):
        self.assertRaises(Rejected,self.s.doa,100,16000,.05)

    def test_amplitude(self):
        self.assertRaises(Rejected,self.s.pcm,[2])

    def test_zero_spacing(self):
        self.assertRaises(Rejected,self.s.doa,1,16000,0)
