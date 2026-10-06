import unittest
from core import grasp_proposal, minimal_event, scene_proposal

class ReviewRegressions(unittest.TestCase):
    def test_force_stop_overrides_unknown_mass(self):
        self.assertEqual(grasp_proposal(None,1,'unknown',10,2)['action'],'stop_proposal')
    def test_force_stop_at_limit(self):
        self.assertEqual(grasp_proposal(None,1,'unknown',2,2)['action'],'stop_proposal')
    def test_unknown_below_limit_requests_support(self):
        self.assertEqual(grasp_proposal(None,1,'unknown',1,2)['action'],'request_support')
    def test_invalid_mass_not_hidden_by_unknown_fragility(self):
        with self.assertRaises(ValueError): grasp_proposal(-1,1,'unknown',0,2)
    def test_allowlist_rejects_string(self):
        with self.assertRaises(ValueError): scene_proposal([{'device':'lamp','action':'on'}],{'lamp':'turn_on'})
    def test_allowlist_exact_match(self):
        self.assertFalse(scene_proposal([{'device':'lamp','action':'on'}],{'lamp':['turn_on']})['eligible_proposal'])
    def test_scene_valid_remains_nonexecutable(self):
        result=scene_proposal([{'device':'lamp','action':'on'}],{'lamp':['on']})
        self.assertTrue(result['eligible_proposal']);self.assertFalse(result['executable'])
    def test_nested_step_rejected(self):
        with self.assertRaises(ValueError): scene_proposal([{'device':[],'action':'on'}],{'lamp':['on']})
    def test_nested_log_fields_dropped(self):
        self.assertEqual(minimal_event({'code':{'secret':'raw'},'result':[],'component':'motor','private':'raw'}),{'component':'motor'})
    def test_nonmapping_log_rejected(self):
        with self.assertRaises(ValueError): minimal_event([])
    def test_enum_log_preserved(self):
        self.assertEqual(minimal_event({'code':'E_STOP','seq':1}),{'code':'E_STOP','seq':1})
