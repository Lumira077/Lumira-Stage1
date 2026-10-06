"""Synthetic two-modality fusion -> trend -> revoke. No real inference/IO."""
import json
from core import *
p={k:.025 for k in LABELS};p['happy']=.9
face=Observation('demo',1,'face',10,p,1,'fixture-v1')
text=SelfReport().observe('demo',1,10,'나는 기뻐요',True)
fused=Fusion().combine('demo',1,10,[face,text],True)
t=TrendStore();t.activate('demo',1,True);t.append('demo',1,10,'demo-1',fused);summary=t.summary('demo',1,10)
t.activate('demo',2,False)
print(json.dumps({'fusion':fused,'trend':summary,'after_revoke_rows':len(t.rows),'actual_models':0},ensure_ascii=False,indent=2))
