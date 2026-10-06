"""Connect S02 profile/context to a persistent software safety broker."""
import hashlib,json
from . import dependency
from ker_onboarding.adapters import SimulatedOutputs

class GuardedOutputs(SimulatedOutputs):
    def __init__(self,broker,fail_once=None):super().__init__(fail_once);self.broker=broker
    @staticmethod
    def context_key(context):return hashlib.sha256(json.dumps(context,sort_keys=True).encode()).hexdigest()
    def apply(self,application_id,module,context):
        # Validate the S02 contract/failure injection before marking any guarded output complete.
        original=super().apply(application_id,module,context)
        actor=context['actor_id'];epoch=self.broker.begin(application_id,actor,self.context_key(context))
        p=context['preferences']
        payload={'context':{},'tts':{'volume':p['volume'],'speech_rate':p['speech_rate']},
                 'expression':{'level':p['expression_level']},'motion':{'gesture':'none','level':p['gesture_level']}}[module]
        cid=self.broker.submit(application_id,actor,epoch,module,payload,'apply-v1')
        self.broker.dispatch(cid,actor)
        return {**original,'applied_settings':p,'guarded':True,'physical_output':False}
    def greeting_for_application(self,application_id,context):
        row=self.broker._scope(application_id,context['actor_id'])
        if row[6] != self.context_key(context):raise RuntimeError('Context does not match application')
        p=context['preferences'];cid=self.broker.submit(application_id,context['actor_id'],row[2],'first_greeting',
            {'volume':p['volume'],'speech_rate':p['speech_rate']},'first-greeting-v1')
        before=len(self.broker.transport.events);self.broker.dispatch(cid,context['actor_id'])
        return {**super().greeting(context),'logical_output_started':len(self.broker.transport.events)>before,
                'command_id':cid,'physical_output':False}
    def greeting(self,context):
        raise RuntimeError('An explicit application ID is required for safe greeting output')

from ker_onboarding.service import Service
from ker_onboarding.core import require
class LabService(Service):
    def greeting(self,sid,actor):
        session,row=self._application(sid,actor)
        require(row[2]=='applied','SETTINGS_NOT_APPLIED',409)
        self.devices.ready(actor,session['device_id'])
        return self.outputs.greeting_for_application(row[1],json.loads(row[4]))
    def preview(self,sid,actor,preferences):
        result=super().preview(sid,actor,preferences)
        scope='preview:'+sid;epoch=self.outputs.broker.begin(scope,actor)
        # Queue for explicit dispatch; cancellation can invalidate all commands before output.
        key=hashlib.sha256(json.dumps(preferences,sort_keys=True).encode()).hexdigest()
        payloads={'tts':{'volume':preferences['volume'],'speech_rate':preferences['speech_rate']},
                  'expression':{'level':preferences['expression_level']},
                  'motion':{'gesture':'none','level':preferences['gesture_level']}}
        # Validate every payload before queuing any of the preview bundle.
        for kind,payload in payloads.items():self.outputs.broker.validate(kind,payload)
        ids=[self.outputs.broker.submit(scope,actor,epoch,kind,payload,key) for kind,payload in payloads.items()]
        return {**result,'preview_scope':scope,'epoch':epoch,'command_ids':ids,'preview_state':'queued'}
    def dispatch_preview(self,sid,actor,command_ids):
        session=self.get(sid,actor);self._active(session);self.devices.ready(actor,session['device_id'])
        result=[]
        for cid in command_ids:
            row=self.outputs.broker.db.execute('SELECT scope FROM commands WHERE id=?',(cid,)).fetchone()
            require(row is not None and row[0]=='preview:'+sid,'NOT_FOUND',404)
            result.append(self.outputs.broker.dispatch(cid,actor))
        return result
    def stop_outputs(self,sid,actor,latch=True):
        self._get(sid,actor)
        scopes=['preview:'+sid]
        app=self.db.execute('SELECT id FROM applications WHERE session_id=?',(sid,)).fetchone()
        if app:scopes.append(app[0])
        result=[]
        for scope in scopes:
            if self.outputs.broker.db.execute('SELECT 1 FROM scopes WHERE id=?',(scope,)).fetchone():
                result.append(self.outputs.broker.stop(scope,actor,latch=latch))
        return result
    def cancel(self,sid,actor):
        result=super().cancel(sid,actor)
        self.stop_outputs(sid,actor,latch=False)
        return result
