import tempfile,unittest
from family import FamilySession
from profile_service import Service
from profile_contract import DEFAULTS,CONSENTS,POLICY
from common import Rejected
class FamilyTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.s=Service(self.tmp.name+'/db');self.now=10
        d={'language':'ko-KR','nickname':'demo','preferred_name':'친구','purpose':'companion',
           'preferences':dict(DEFAULTS),'consent':{**{k:False for k in CONSENTS},'policy_version':POLICY}}
        self.a=self.s.create('owner',d,'a')['profile_id'];self.b=self.s.create('owner',d,'b')['profile_id']
        self.other=self.s.create('other',d,'other')['profile_id'];self.s.provision_device('robot','owner')
        self.f=FamilySession(self.s,'owner','robot',lambda:self.now)
    def tearDown(self):self.s.close();self.tmp.cleanup()
    def test_manual_selection(self):
        x=self.f.select(self.a,True);self.assertIsNotNone(self.f.read(x['epoch']))
    def test_switch_invalidates_previous(self):
        x=self.f.select(self.a,True);self.f.select(self.b,True);self.assertRaises(Rejected,self.f.read,x['epoch'])
    def test_confirmation_required(self):self.assertRaises(Rejected,self.f.select,self.a,False)
    def test_foreign_profile(self):
        self.f.select(self.a,True);self.assertRaises(Exception,self.f.select,self.other,True);self.assertIsNone(self.f.context.subject)
    def test_expiry_guest(self):
        x=self.f.select(self.a,True,1);self.now=11;self.assertRaises(Rejected,self.f.read,x['epoch']);self.assertIsNone(self.f.context.subject);self.assertFalse(self.s.device('robot','owner')['connected'])
    def test_candidate_not_auth(self):
        self.assertFalse(self.f.candidate(self.a,.99)['authenticated']);self.assertIsNone(self.f.context.subject)
    def test_nan_score(self):self.assertRaises(Rejected,self.f.candidate,self.a,float('nan'))
    def test_profile_delete_invalidates(self):
        x=self.f.select(self.a,True);self.s.delete(self.a,'owner',1);self.assertRaises(Exception,self.f.read,x['epoch']);self.assertIsNone(self.f.context.subject)
    def test_profile_change_invalidates(self):
        x=self.f.select(self.a,True);self.s.update(self.a,'owner',{'nickname':'new'},1,'change');self.assertRaises(Exception,self.f.read,x['epoch'])
    def test_stop_blocks(self):
        x=self.f.select(self.a,True);self.f.context.stop();self.assertRaises(Rejected,self.f.read,x['epoch'])
