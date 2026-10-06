"""No LLM, speech engine or motor adapter is connected in this development bridge."""
from memory_contract import Error,require
class Dialogue:
    def __init__(self,memory):self.memory=memory
    def prepare(self,actor,pid,device,query):return self.memory.prepare(actor,pid,device,query)
    def respond(self,actor,pid,device,ticket,private_output_confirmed=False):
        # Explicit output permission from trusted UI; no passive face/STT identity inference.
        require(private_output_confirmed is True,'PRIVATE_OUTPUT_CONFIRMATION_REQUIRED',403)
        ctx=self.memory.release_context(actor,pid,device,ticket)
        return {'response_mode':'structured_reference_only','context':ctx,'needs_confirmation':not bool(ctx['memories']),
            'tts_dispatch':False,'expression_dispatch':False,'control_actions':[],'real_model_connected':False}
    def safe_prepare(self,actor,pid,device,query):
        try:return {'status':'prepared',**self.prepare(actor,pid,device,query)}
        except Error as e:return {'status':'unavailable','error_code':e.code,'memories':[]}
        except Exception:return {'status':'unavailable','error_code':'MEMORY_SERVICE_UNAVAILABLE','memories':[]}
