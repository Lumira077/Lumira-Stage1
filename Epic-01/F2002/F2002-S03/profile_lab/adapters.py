"""Simulated settings receivers. Never dispatch real speech, recognition or motion."""
import copy
from profile_contract import require,MODULES
class SimulatedOutputs:
    mode='simulated';hardware_connected=False
    def __init__(self,fail_once=None,bad_ack=False):self.fail_once=fail_once;self.bad_ack=bad_ack;self.receipts={};self.calls=[];self.settings={}
    def apply(self,aid,module,ctx):
        require(module in MODULES)
        if (aid,module) in self.receipts:return copy.deepcopy(self.receipts[(aid,module)])
        self.calls.append(module)
        if self.fail_once==module:self.fail_once=None;raise RuntimeError('SIMULATED_FAILURE')
        pref=ctx['preferences'];effective={**pref,'volume':min(pref['volume'],40),'expression_level':min(pref['expression_level'],2),'gesture_level':min(pref['gesture_level'],1)}
        # Module-specific minimum payload. Recognition cannot infer consent from preference.
        value={'language':ctx['language'],'purpose':ctx['purpose']} if module=='dialogue' else {'permissions':copy.deepcopy(ctx['permissions'])} if module=='recognition' else effective if module in ('tts','expression','control') else {}
        self.settings[module]=copy.deepcopy(value)
        ack={'application_id':aid,'module':module,'revision':ctx['revision'],'ack':not self.bad_ack,'mode':'simulated'}
        self.receipts[(aid,module)]=ack;return copy.deepcopy(ack)
