import tempfile,unittest
from pathlib import Path
from onboarding_lab.safety import Broker,Rejected,SimulatedTransport,confirmed_input
class Safety(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=str(Path(self.tmp.name)/'safety.db');self.now=1000
        self.b=Broker(self.path,clock=lambda:self.now);self.epoch=self.b.begin('scope','owner')
    def tearDown(self):self.b.close();self.tmp.cleanup()
    def reject(self,code,fn):
        with self.assertRaises(Rejected) as e:fn()
        self.assertEqual(str(e.exception),code)
    def submit(self,kind='tts',payload=None,key='r1'):
        return self.b.submit('scope','owner',self.epoch,kind,payload or {'volume':20,'speech_rate':1.0},key)
    def test_volume_cap(self):self.reject('VOLUME_LIMIT',lambda:self.submit(payload={'volume':21,'speech_rate':1.0}))
    def test_mute_and_duplicate(self):
        cid=self.submit(payload={'volume':0,'speech_rate':1.0});self.b.dispatch(cid,'owner');self.b.dispatch(cid,'owner');self.assertEqual(len(self.b.transport.events),1)
    def test_boolean_is_not_volume(self):self.reject('VOLUME_LIMIT',lambda:self.submit(payload={'volume':True,'speech_rate':1.0}))
    def test_rate_limit(self):self.reject('RATE_LIMIT',lambda:self.submit(payload={'volume':20,'speech_rate':1.3}))
    def test_unapproved_motion(self):self.reject('UNAPPROVED_MOTION',lambda:self.submit('motion',{'gesture':'wave','level':1}))
    def test_arbitrary_joint_commands_rejected(self):self.reject('UNAPPROVED_MOTION',lambda:self.submit('motion',{'gesture':'none','level':1,'joint_angle':100}))
    def test_expression_limit(self):self.reject('EXPRESSION_LIMIT',lambda:self.submit('expression',{'level':2}))
    def test_expired_command_never_executes(self):
        cid=self.submit();self.now+=4;self.reject('COMMAND_EXPIRED',lambda:self.b.dispatch(cid,'owner'));self.assertEqual(self.b.transport.events,[])
    def test_stop_latched_until_inspection(self):
        self.b.stop('scope','owner');self.reject('EXPLICIT_INSPECTION_REQUIRED',lambda:self.b.rearm('scope','owner'))
        epoch=self.b._scope('scope','owner')[2];self.reject('STOP_LATCHED',lambda:self.b.submit('scope','owner',epoch,'context',{},'r1'))
    def test_stop_ack_failure_still_suppresses(self):
        self.b.transport.fail_stop=True;self.assertFalse(self.b.stop('scope','owner')['stop_ack'])
        self.assertEqual(self.b._scope('scope','owner')[3],0)
    def test_rearm_never_replays_old_queue(self):
        cid=self.submit();self.b.stop('scope','owner');self.b.rearm('scope','owner',True)
        self.reject('STALE_EPOCH',lambda:self.b.dispatch(cid,'owner'));self.assertEqual(self.b.transport.events,[])
    def test_wrong_actor_hidden(self):
        cid=self.submit();self.reject('NOT_FOUND',lambda:self.b.dispatch(cid,'other'))
    def test_disconnect_suppression(self):
        cid=self.submit();self.b.disconnect('scope','owner');self.reject('STALE_EPOCH',lambda:self.b.dispatch(cid,'owner'))
    def test_restart_invalidates_queued_outputs(self):
        cid=self.submit();self.b.close();self.b=Broker(self.path,clock=lambda:self.now)
        self.assertEqual(self.b.db.execute('SELECT state FROM commands WHERE id=?',(cid,)).fetchone()[0],'cancelled')
        self.reject('STALE_EPOCH',lambda:self.b.dispatch(cid,'owner'));self.assertEqual(self.b.transport.events,[])
    def test_uncertain_ack_fails_closed(self):
        class Invalid(SimulatedTransport):
            def execute(self,*args):return {'ack':True,'command_id':'incorrect'}
        self.b.transport=Invalid();cid=self.submit();self.reject('OUTPUT_FAILED',lambda:self.b.dispatch(cid,'owner'));self.assertEqual(self.b._scope('scope','owner')[5],1)
    def test_request_key_conflict(self):
        self.submit();self.reject('IDEMPOTENCY_CONFLICT',lambda:self.submit(payload={'volume':10,'speech_rate':1.0}))
    def test_real_adapter_rejected(self):
        class Real(SimulatedTransport):mode='hardware'
        self.reject('HARDWARE_ADAPTER_NOT_IMPLEMENTED',lambda:Broker(str(Path(self.tmp.name)/'real.db'),transport=Real()))
    def test_confirmation_requires_real_boolean(self):self.reject('USER_CONFIRMATION_REQUIRED',lambda:confirmed_input('consent',True,1))
    def test_boolean_epoch_is_rejected(self):
        self.reject('STALE_EPOCH',lambda:self.b.submit('scope','owner',True,'context',{},'r1'))
    def test_physical_claim_in_simulated_ack_is_rejected(self):
        class Incorrect(SimulatedTransport):
            def execute(self,cid,*args):return {'ack':True,'command_id':cid,'adapter_mode':'simulated','physical_output':True}
        self.b.transport=Incorrect();cid=self.submit();self.reject('OUTPUT_FAILED',lambda:self.b.dispatch(cid,'owner'))
