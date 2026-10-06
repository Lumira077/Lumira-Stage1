import unittest,math
from profile_ops.operations import metrics,study,release,dashboard
from profile_contract import Error
class Ops(unittest.TestCase):
    def test_retry_denominator(self):m=metrics([(1,'apply_attempt','OK'),(1,'apply_failed','tts'),(2,'apply_attempt','OK'),(2,'apply_succeeded','OK')],0,3);self.assertEqual(m['apply_failure_rate'],.5)
    def test_empty_denominator(self):self.assertIsNone(metrics([],0,3)['apply_failure_rate'])
    def test_period_excludes_end(self):self.assertEqual(metrics([(3,'profile_created','OK')],0,3)['counts'],{})
    def test_invalid_period(self):self.assertRaises(Error,metrics,[],0,math.nan)
    def row(self,mode='simulated'):return {'participant_id':'a'*32,'task':'edit','mode':mode,'version':'0.1.0','completed':True,'assisted':False,'seconds':20}
    def test_synthetic_not_real(self):self.assertEqual(study([self.row()])['actual_participants'],0)
    def test_duplicate_observation(self):self.assertRaises(Error,study,[self.row(),self.row()])
    def test_pii_field_rejected(self):r=self.row();r['name']='private';self.assertRaises(Error,study,[r])
    def test_invalid_duration(self):r=self.row();r['seconds']=True;self.assertRaises(Error,study,[r])
    def test_real_label_does_not_approve(self):g=release({'failed':0,'errors':0},study([self.row('observed')]));self.assertFalse(g['release_ready'])
    def test_dashboard_escape(self):html=dashboard({'counts':{'<script>':1}},{'status':'blocked'});self.assertNotIn('<script>',html);self.assertIn('&lt;script&gt;',html)
