import copy,unittest,math
from profile_contract import *
def sample():return {'language':'ko-KR','nickname':'가명','preferred_name':'친구','purpose':'companion','preferences':dict(DEFAULTS),'consent':{**{k:False for k in CONSENTS},'policy_version':POLICY}}
class Contract(unittest.TestCase):
    def test_valid(self):self.assertEqual(validate(sample()),sample())
    def test_trim_names(self):x=sample();x['nickname']=' 가명 ';self.assertEqual(validate(x)['nickname'],'가명')
    def test_unknown_field_rejected(self):x=sample();x['token']='secret';self.assertRaises(Error,validate,x)
    def test_blank_name(self):x=sample();x['nickname']=' ';self.assertRaises(Error,validate,x)
    def test_control_characters(self):x=sample();x['preferred_name']='x\n';self.assertRaises(Error,validate,x)
    def test_unsupported_language(self):x=sample();x['language']='xx';self.assertRaises(Error,validate,x)
    def test_unsupported_voice(self):x=sample();x['preferences']['voice_id']='fake';self.assertRaises(Error,validate,x)
    def test_bool_volume_rejected(self):x=sample();x['preferences']['volume']=True;self.assertRaises(Error,validate,x)
    def test_nan_rate_rejected(self):x=sample();x['preferences']['speech_rate']=math.nan;self.assertRaises(Error,validate,x)
    def test_high_volume_rejected(self):x=sample();x['preferences']['volume']=101;self.assertRaises(Error,validate,x)
    def test_missing_consent(self):x=sample();del x['consent']['cloud_transfer'];self.assertRaises(Error,validate,x)
    def test_policy_version(self):x=sample();x['consent']['policy_version']='old';self.assertRaises(Error,validate,x)
    def test_partial_nested_patch_rejected(self):self.assertRaises(Error,patch,sample(),{'preferences':{'volume':30}})
    def test_no_mutation_of_input(self):x=sample();y=validate(x);y['preferences']['volume']=0;self.assertEqual(x['preferences']['volume'],20)
    def test_context_minimal(self):c=context({'data':sample(),'profile_id':'p','revision':2});self.assertNotIn('nickname',c);self.assertNotIn('subject_id',c)
