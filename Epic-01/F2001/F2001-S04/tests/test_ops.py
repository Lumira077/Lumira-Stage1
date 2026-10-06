import copy,json,tempfile,unittest,uuid
from pathlib import Path
from onboarding_ops.telemetry import Sink,Invalid
from onboarding_ops.metrics import aggregate,alerts
from onboarding_ops.release import evaluate_users,evaluate,sign
from onboarding_ops.dashboard import build
class Events(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.now=1000;self.s=Sink(str(Path(self.tmp.name)/'events.db'),b'x'*32,clock=lambda:self.now)
    def tearDown(self):self.s.close();self.tmp.cleanup()
    def emit(self,kind='onboarding_started',sid='private-session',**kw):return self.s.emit(sid,kind,**kw)
    def metrics(self,**kw):return aggregate(self.s.read(),0,2000,4000,**kw)
    def test_pseudonym_no_raw_session_or_token(self):
        self.emit();encoded=json.dumps(self.s.read());self.assertNotIn('private-session',encoded);self.assertNotIn('xxxxxxxx',encoded)
    def test_key_required(self):
        with self.assertRaises(Invalid):Sink(':memory:',b'weak')
    def test_raw_personal_fields_rejected(self):
        for field in ['nickname','preferred_name','token','wifi_password','utterance','consent_text']:
            with self.assertRaises(Invalid):self.emit(**{field:'sensitive'})
    def test_event_idempotency(self):
        a=self.emit(stable_key='start');self.now+=10;self.assertEqual(a,self.emit(stable_key='start'));self.assertEqual(len(self.s.read()),1)
    def test_event_conflict(self):
        self.emit('step_completed',step='profile',stable_key='s1',latency_ms=1)
        with self.assertRaises(Invalid):self.emit('step_completed',step='profile',stable_key='s1',latency_ms=2)
    def test_bad_enum_or_numeric(self):
        for kw in [{'route':'real name'},{'latency_ms':float('nan')},{'latency_ms':True},{'error_code':'raw server dump'}]:
            with self.assertRaises(Invalid):self.emit(**kw)
    def test_empty_denominator_is_null(self):self.assertIsNone(self.metrics()['ready_completion']['value'])
    def test_unique_session_completion(self):
        self.emit(route='self');self.emit('registration_committed',route='self');self.emit('registration_committed',route='self');self.now+=30;self.emit('onboarding_ready',route='self')
        m=self.metrics();self.assertEqual(m['registration_completion']['value'],1);self.assertEqual(m['duration']['p50_seconds'],30)
    def test_guest_excluded_from_registration_denominator(self):
        self.emit(route='guest');self.emit('onboarding_ready',route='guest');m=self.metrics();self.assertEqual(m['registration_completion']['denominator'],0);self.assertEqual(m['ready_completion']['value'],1)
    def test_retry_attempts_are_distinct(self):
        self.emit();a,b=uuid.uuid4().hex,uuid.uuid4().hex
        self.emit('apply_attempt',attempt_id=a);self.emit('context_apply_failed',attempt_id=a,module='tts',error_code='MODULE_APPLY_FAILED');self.emit('context_apply_failed',attempt_id=a,module='tts',error_code='MODULE_APPLY_FAILED');self.emit('apply_attempt',attempt_id=b)
        self.assertEqual(self.metrics()['apply_failure']['value'],.5)
    def test_orphan_failure_not_in_denominator(self):
        self.emit();self.emit('context_apply_failed',attempt_id=uuid.uuid4().hex,module='tts');self.assertIsNone(self.metrics()['apply_failure']['value'])
    def test_resume_matching_attempt(self):
        self.emit();a=uuid.uuid4().hex;self.emit('resume_attempt',attempt_id=a);self.emit('onboarding_resumed',attempt_id=a,success=True);self.assertEqual(self.metrics()['resume_success']['value'],1)
    def test_dropouts_only_mature_entries(self):
        self.emit();self.emit('step_entered',step='profile');self.now=3900;self.emit('step_entered',step='consent');m=self.metrics();self.assertEqual(m['steps']['profile']['dropout']['value'],1);self.assertNotIn('consent',m['steps'])
    def test_cancel_not_error_or_dropout(self):
        self.emit();self.emit('step_entered',step='consent');self.emit('onboarding_cancelled');self.assertEqual(self.metrics()['steps'],{});self.assertEqual(self.metrics()['cancelled_sessions'],1)
    def test_version_and_mode_filter(self):
        self.emit();self.assertEqual(self.metrics(version='9.9.9')['started_sessions'],0);self.assertEqual(self.metrics(mode='observed')['started_sessions'],0)
    def test_last_known_route(self):
        self.emit();self.emit('step_completed',route='guardian',step='registration');self.assertEqual(self.metrics(route='guardian')['started_sessions'],1)
    def test_cohort_excludes_start_outside_period(self):
        self.emit();self.assertEqual(aggregate(self.s.read(),2000,3000,4000)['started_sessions'],0)
    def test_latest_step_entry_invalidates_old_completion(self):
        self.emit();self.emit('step_entered',step='profile');self.emit('step_completed',step='profile');self.now=1200;self.emit('step_entered',step='profile')
        self.assertEqual(self.metrics()['steps']['profile']['dropout']['value'],1)
    def test_support_is_unique_session(self):
        self.emit();self.emit('support_requested');self.emit('support_requested');self.assertEqual(self.metrics()['support_request']['value'],1)
    def test_alert_small_sample_suppressed(self):
        self.emit();a=uuid.uuid4().hex;self.emit('apply_attempt',attempt_id=a);self.emit('context_apply_failed',attempt_id=a,module='tts');self.assertEqual(alerts(self.metrics())['alerts'],[])
    def test_duplicate_is_blocker_alert(self):
        self.emit();self.emit('duplicate_registration');self.assertEqual(alerts(self.metrics())['alerts'][0]['severity'],'blocker')
    def test_retention(self):
        self.emit();self.assertEqual(self.s.purge_before(1001),1);self.assertEqual(self.s.read(),[])
    def test_dashboard_escapes_external_text(self):
        m=self.metrics();r={'status':'blocked','blockers':['<script>bad</script>']};html=build(m,r,{'alerts':[]});self.assertNotIn('<script>bad',html);self.assertIn('&lt;script&gt;',html)

def observation(i,mode='observed',task='basic_registration'):
    return {'participant_id':f'{i:032x}','group':'elderly' if i==0 else 'guardian' if i==1 else 'general','task':task,'phase':'retest','mode':mode,'completed':True,'assisted':False,'seconds':200,'normal_connection':True,'version':'0.4.0'}
def eligible_rows():
    rows=[observation(i) for i in range(10)]
    for task in ['guardian','guest','resume','connection_loss','settings_change']:rows.append(observation(1,task=task))
    return rows
class Release(unittest.TestCase):
    def evidence(self):
        return {'candidate':{'commit':'a'*40,'version':'0.4.0','mode':'hardware'},'s03':{'hardware_tests':{'status':'passed'},'release_ready':True},
                'users':evaluate_users(eligible_rows()),'rollback':{'scope':'production_approved','status':'passed'},
                'operations':{'status':'approved','data_mode':'observed'},'blocker_defects':0}
    def keys(self):return {'R1':b'R'*32,'Q1':b'Q'*32}  # synthetic unit-test keys only
    def test_simulated_users_never_eligible(self):self.assertFalse(evaluate_users([observation(i,'simulated') for i in range(10)])['eligible'])
    def test_independent_5min_threshold(self):
        rows=eligible_rows();rows[2]['assisted']=True;rows[3]['seconds']=301;self.assertTrue(evaluate_users(rows)['eligible']);rows[4]['completed']=False;self.assertFalse(evaluate_users(rows)['eligible'])
    def test_duplicate_observation_rejected(self):
        rows=eligible_rows();rows.append(rows[0])
        with self.assertRaises(Invalid):evaluate_users(rows)
    def test_real_name_field_rejected(self):
        row=observation(0);row['real_name']='name'
        with self.assertRaises(Invalid):evaluate_users([row])
    def test_multiple_versions_not_pooled(self):
        rows=eligible_rows();rows[0]['version']='0.3.0';self.assertFalse(evaluate_users(rows)['eligible'])
    def test_missing_reviewers_blocks(self):self.assertFalse(evaluate(self.evidence())['release_ready'])
    def test_valid_synthetic_signed_bundle(self):
        e=self.evidence();keys=self.keys();approvals=[sign(role,e,key) for role,key in keys.items()];self.assertTrue(evaluate(e,approvals,keys)['release_ready'])
    def test_changed_evidence_invalidates_signatures(self):
        e=self.evidence();keys=self.keys();a=[sign(role,e,key) for role,key in keys.items()];e['blocker_defects']=1
        self.assertFalse(evaluate(e,a,keys)['release_ready'])
    def test_wrong_key_or_forged_approval(self):
        e=self.evidence();a=[sign(role,e,b'wrong'*8) for role in ('R1','Q1')];self.assertFalse(evaluate(e,a,self.keys())['release_ready'])
    def test_hardware_not_run_blocks_even_signed(self):
        e=self.evidence();e['s03']['hardware_tests']['status']='not_run';keys=self.keys();a=[sign(role,e,key) for role,key in keys.items()];self.assertFalse(evaluate(e,a,keys)['release_ready'])
    def test_non_ascii_signature_blocks_cleanly(self):
        e=self.evidence();a=sign('R1',e,b'R'*32);a['signature']='위조';self.assertFalse(evaluate(e,[a],self.keys())['release_ready'])
    def test_unknown_defect_count_blocks(self):
        e=self.evidence();e['blocker_defects']=None;self.assertIn('OPEN_OR_UNKNOWN_BLOCKER_DEFECTS',evaluate(e)['blockers'])
    def test_release_version_matches_study(self):
        e=self.evidence();e['candidate']['version']='0.5.0';self.assertIn('USER_STUDY_VERSION_MISMATCH',evaluate(e)['blockers'])
