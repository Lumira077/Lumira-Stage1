import json
from core import *
c=Context('demo',1,'turn1');t=Timeline();g=t.start(c)
voice=TTSPlanner().plan(c,'안녕하세요','demo-ko','ko-KR',style='warm')
gesture=GestureSelector().choose('greeting',.9,clearance=True)
plan=GestureLibrary().plan(gesture['gesture'],True,{'neck':0,'arm':0,'waist':0})
for channel in ('face','audio','motion'):t.add(c,g,channel+'1',channel,0)
cues=t.due(c,g,0);cancel=t.cancel()
print(json.dumps({'voice':{k:v for k,v in voice.items() if k!='context'},'gesture':gesture,'joint_plan':plan,'cues':cues,'cancel':cancel,'actual_audio_or_motor_output':False},ensure_ascii=False,indent=2))
