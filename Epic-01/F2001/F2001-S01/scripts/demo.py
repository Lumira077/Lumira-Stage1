"""End-to-end HTTP contract demo. No hardware ACK simulated."""
import json
import os
from urllib.request import Request, urlopen

def send(method,path,data=None):
    req=Request(os.environ.get('KER_API_BASE', 'http://127.0.0.1:8080')+path,
                data=json.dumps(data).encode() if data is not None else None,method=method,
                headers={'Authorization':'Bearer '+os.environ['KER_DEMO_TOKEN'],'Content-Type':'application/json'})
    with urlopen(req) as res:return json.load(res)

x=send('POST','/v1/onboarding/sessions',{'device_id':'demo-device-01'})
base='/v1/onboarding/sessions/'+x['session_id']
steps=[('language',{'language':'ko-KR'}),('profile',{'nickname':'테스트','preferred_name':'박사님'}),
       ('purpose',{'purpose':'companion'}),('preferences',{'voice_id':'device_default','speech_rate':1.0,
        'volume':20,'expression_level':1,'gesture_level':1}),
       ('consent',{'long_term_memory':False,'conversation_storage':False,'biometric_identity':False,'cloud_transfer':False}),
       ('review',{'confirmed':True})]
for step,data in steps:x=send('PATCH',base+'/steps/'+step,{'expected_revision':x['revision'],'data':data})
result=send('POST',base+'/complete',{'expected_revision':x['revision'],'mutation_id':'demo-complete-1'})
print(json.dumps(result,ensure_ascii=False,indent=2))
