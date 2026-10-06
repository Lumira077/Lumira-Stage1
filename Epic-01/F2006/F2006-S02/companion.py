"""Local canned dialogue planner. No LLM, diagnosis, TTS, music playback or motion dispatch."""
from common import require, ident
TEXT={'greeting':'안녕하세요. 어떤 이야기를 나눌까요?',
      'talk':'오늘 이야기하고 싶은 일이 있나요?',
      'comfort':'지금 기분을 이야기해 주시겠어요?',
      'story':'짧은 이야기를 들려드릴까요?',
      'end':'대화를 마칠게요. 편히 쉬세요.'}
class Companion:
    def __init__(self,context): self.context=context; self.turns={}; self.state='idle'
    def plan(self,turn,intent,epoch,policy,quiet=False):
        ident(turn); self.context.check(epoch)
        require(type(quiet) is bool,'INVALID_INPUT')
        require(policy.get('mode')=='companion','NOT_SUPPORTED')
        require(intent in TEXT,'NOT_SUPPORTED')
        require(self.state!='ending','NOT_READY')
        key=(epoch,turn); require(key not in self.turns,'DUPLICATE_TURN')
        self.turns[key]='finalized'; self.state='ending' if intent=='end' else 'speaking'
        return {'turn_id':turn,'epoch':epoch,'utterance':TEXT[intent],
                'backend':'local_template','expression_id':'neutral' if quiet else 'friendly',
                'gesture_id':'none','audible':not quiet,'executable_actions':[]}
    def cancel(self):
        self.context.reset(self.context.subject); self.turns.clear(); self.state='paused'
        return {'cancel_required':True,'actual_output_cancelled':False}
    def late_backend(self,turn,epoch):
        self.context.check(epoch)
        require((epoch,turn) not in self.turns,'DUPLICATE_TURN')
        return {'accepted':False,'reason':'cloud_not_connected'}
