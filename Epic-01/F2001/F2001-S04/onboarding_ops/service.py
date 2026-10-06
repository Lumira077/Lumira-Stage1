"""Instrumentation at persisted service transitions; never logs inputs or text."""
import time,uuid
from . import dependency
from onboarding_lab.adapters import LabService
from ker_onboarding.core import Error
class ObservedService(LabService):
    def __init__(self,*args,sink,**kwargs):super().__init__(*args,**kwargs);self.sink=sink;self.dropped_events=0
    def _route(self,sid,actor):return self._get(sid,actor)['draft'].get('registration',{}).get('registration_type','unknown')
    def _emit(self,*args,**kwargs):
        try:self.sink.emit(*args,**kwargs)
        except Exception:self.dropped_events+=1  # application success is not rolled back by a logger failure
    def create(self,actor,device,allowed_devices):
        x=super().create(actor,device,allowed_devices);self._emit(x['session_id'],'onboarding_started',stable_key='start');return x
    def save_step(self,sid,actor,step,data,revision):
        route=self._route(sid,actor);self._emit(sid,'step_entered',route=route,step=step,stable_key=str(revision)+':'+step)
        start=time.perf_counter()
        try:x=super().save_step(sid,actor,step,data,revision)
        except Error as e:
            code=e.code if e.code in ('REVISION_CONFLICT','INVALID_INPUT','DEVICE_DISCONNECTED','SESSION_EXPIRED') else 'INVALID_INPUT'
            self._emit(sid,'step_failed',route=route,step=step,error_code=code);raise
        route=self._route(sid,actor)
        self._emit(sid,'step_completed',route=route,step=step,latency_ms=(time.perf_counter()-start)*1000,stable_key=str(x['revision']))
        return x
    def complete(self,sid,actor,mutation_id,revision):
        route=self._route(sid,actor);r=super().complete(sid,actor,mutation_id,revision)
        if r['registration_status']=='committed':self._emit(sid,'registration_committed',route=route,stable_key='commit')
        return r
    def apply(self,sid,actor):
        route=self._route(sid,actor);before=self.application(sid,actor)['attempts'];r=super().apply(sid,actor)
        if r['attempts']>before:
            attempt=uuid.uuid4().hex;self._emit(sid,'apply_attempt',route=route,attempt_id=attempt)
            if r['apply_status']=='failed':
                module=r['error_code'].split(':')[-1];self._emit(sid,'context_apply_failed',route=route,attempt_id=attempt,module=module,error_code='MODULE_APPLY_FAILED')
        return r
    def greeting(self,sid,actor):
        r=super().greeting(sid,actor)
        self._emit(sid,'onboarding_ready',route=self._route(sid,actor),stable_key='ready');return r
    def resume(self,sid,actor):
        route=self._route(sid,actor);attempt=uuid.uuid4().hex;self._emit(sid,'resume_attempt',route=route,attempt_id=attempt)
        try:x=super().get(sid,actor)
        except Error:
            self._emit(sid,'onboarding_resumed',route=route,attempt_id=attempt,success=False);raise
        self._emit(sid,'onboarding_resumed',route=route,attempt_id=attempt,success=True);return x
    def cancel(self,sid,actor):
        route=self._route(sid,actor);x=super().cancel(sid,actor);self._emit(sid,'onboarding_cancelled',route=route,stable_key='cancel');return x
    def request_support(self,sid,actor):self._emit(sid,'support_requested',route=self._route(sid,actor),stable_key='support')
