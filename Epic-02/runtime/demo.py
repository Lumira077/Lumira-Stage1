"""Fake wake/STT events to fake dialogue, then cancellation; no audio or Cloud IO."""
import json
from core import *
def demo():
    session=ConversationSession(lambda:10);epoch=session.open('demo')
    wake=WakeGate(lambda:10).trigger('wake',.9,10)
    transcript=TranscriptAssembler(epoch).update(1,'안녕하세요',True,epoch)
    language=LanguageResolver().choose('ko-KR',['ko-KR'],['ko-KR'],['ko-KR'])
    gateway=Gateway({'openai_sample':lambda i,n:{'text':'안녕하세요. 가상 대화 시험입니다.','usage_tokens':5}})
    x={'sensitivity':'public','safety_command':False,'cloud_consent':True,'visual_needed':False,'network_ok':True,'credits':1,'robot_ready':True}
    reply=Dialogue(session,gateway).answer('demo',epoch,'turn',x,'adult','clear')
    cancel=InterruptController(session).cancel()
    return {'wake':wake,'transcript':transcript,'locale':language,'reply':reply,'cancel':cancel,'actual_cloud_calls':0,'actual_audio_output':False}
if __name__=='__main__':print(json.dumps(demo(),ensure_ascii=False,indent=2))
