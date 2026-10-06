import json
from core import *
c=Context('demo',1);f=FaceRegistry();v=[1,0,0,0,0,0,0,0];f.enroll('demo',1,v,'fixture_v1',True,True,True)
candidate=f.identify(v,'fixture_v1',10,10,True,True)
track={'id':'anonymous1','epoch':1,'angle_deg':20,'quality':1,'timestamp':10}
speaker=SpeakerAssociator().associate(c,20,10,[track],10,True,False,True)
head=HeadAligner().propose(c,0,.1,10,10,face_x=.3,clearance=True)
f.revoke('demo',2)
print(json.dumps({'face_candidate':candidate,'speaker_candidate':speaker,'head_proposal':head,'templates_after_revoke':len(f.templates),'actual_model_or_motor_calls':0},ensure_ascii=False,indent=2))
