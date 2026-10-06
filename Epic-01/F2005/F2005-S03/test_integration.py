import unittest,tempfile
from family import FamilySession
from policy import resolve,PolicySelection
from companion import Companion
from pet import Pet
from theme import Theme,MODULES
from operations import Metrics,release_assessment
from common import Rejected
from profile_service import Service
from profile_contract import DEFAULTS,CONSENTS,POLICY
class IntegrationTests(unittest.TestCase):
    def test_profile_switch_invalidates_all_plans(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=Service(tmp+'/profiles.db')
            try:
                data={'language':'ko-KR','nickname':'demo','preferred_name':'친구','purpose':'home',
                      'preferences':dict(DEFAULTS),'consent':{**{k:False for k in CONSENTS},'policy_version':POLICY}}
                a=s.create('owner',data,'a')['profile_id'];b=s.create('owner',data,'b')['profile_id'];s.provision_device('robot','owner')
                family=FamilySession(s,'owner','robot',lambda:10);e=family.select(a,True)['epoch'];family.read(e)
                p=resolve('Home','companion',DEFAULTS,{'volume':20,'gesture_level':1,'expression_level':1})
                c=Companion(family.context);c.plan('turn','talk',e,p)
                pet=Pet(family.context,lambda:10);petpolicy=resolve('Home','pet',DEFAULTS,{})
                theme=Theme(family.context,lambda:10);t=theme.prepare('outfit-blue',1,e,'Home');theme.commit(t,{m:dict(t) for m in MODULES})
                family.select(b,True)
                self.assertRaises(Rejected,c.plan,'late','talk',e,p)
                self.assertRaises(Rejected,pet.event,'late','touch',10,e,petpolicy)
                self.assertEqual(theme.tick(),'default')
                self.assertIsNotNone(family.read(family.context.epoch))
            finally:s.close()
    def test_policy_tampering_denied(self):
        p=resolve('Home','pet',{},{});p['limits']['gesture_level']=3
        self.assertRaises(Rejected,PolicySelection().apply,p,True,False,('dialogue','ui','voice','motion'))
    def test_policy_privacy_escalation_denied(self):
        p=resolve('Home','pet',{},{});p['cloud_allowed']=True
        self.assertRaises(Rejected,PolicySelection().apply,p,True,False,('dialogue','ui','voice','motion'))
    def test_end_requires_new_session(self):
        from common import Context
        context=Context();context.reset('demo');c=Companion(context);p=resolve('Friend','companion',{},{});c.plan('end','end',context.epoch,p)
        self.assertRaises(Rejected,c.plan,'late','talk',context.epoch,p)
    def test_metrics_no_free_text(self):
        m=Metrics();m.record('F2004','selected');self.assertRaises(Rejected,m.record,'F2004','private-name');self.assertEqual(m.snapshot()[0]['operations'],1)
    def test_success_never_releases_without_evidence(self):
        self.assertFalse(release_assessment({'tests':1,'passed':True,'failures':0,'errors':0})['release_ready'])
