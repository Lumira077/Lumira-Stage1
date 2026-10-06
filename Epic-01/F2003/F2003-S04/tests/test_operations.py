import unittest,math
from memory_ops.operations import metrics,study,release,dashboard
from memory_contract import Error
class Operations(unittest.TestCase):
    def row(self):return {'participant_id':'a'*32,'task':'remember','mode':'simulated','completed':True,'assisted':False,'seconds':10,'version':'0.1.0'}
    def test_event_period(self):m=metrics([(1,'0.1.0','search_completed','OK'),(3,'0.1.0','memory_deleted','OK')],0,3);self.assertEqual(m['counts'],{'search_completed':1})
    def test_empty_events(self):self.assertEqual(metrics([],0,3)['counts'],{})
    def test_nan_period(self):self.assertRaises(Error,metrics,[],0,math.nan)
    def test_synthetic_is_not_real(self):self.assertEqual(study([self.row()])['actual_participants'],0)
    def test_duplicate_observation(self):self.assertRaises(Error,study,[self.row(),self.row()])
    def test_private_fields_rejected(self):r=self.row();r['name']='private';self.assertRaises(Error,study,[r])
    def test_no_approval_from_test_pass(self):self.assertFalse(release({'failed':0,'errors':0})['release_ready'])
    def test_dashboard_escapes(self):self.assertNotIn('<script>',dashboard({'<script>':1},{'status':'blocked'}))
