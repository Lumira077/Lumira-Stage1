"""HTTP demo: register, simulated failure/retry, context and first greeting."""
import json
import os
from urllib.request import Request,urlopen
base=os.environ.get('KER_API_BASE','http://127.0.0.1:8081')
def send(method,path,data=None,token=None):
    req=Request(base+path,data=json.dumps(data).encode() if data is not None else None,method=method,
                headers={'Authorization':'Bearer '+(token or os.environ['KER_DEMO_TOKEN']),'Content-Type':'application/json'})
    with urlopen(req,timeout=5) as res:return json.load(res)
def run(device='demo-device-01',kind='self',token=None):
    boot=send('GET','/v1/bootstrap',token=token)
    x=send('POST','/v1/onboarding/sessions',{'device_id':device},token);sid=x['session_id'];path='/v1/onboarding/sessions/'+sid
    subject='guest' if kind=='guest' else 'demo-child-01' if kind=='guardian' else boot['actor_id']
    data={'registration':{'registration_type':kind,'subject_id':subject},'language':{'language':'ko-KR'},
          'profile':{'nickname':'샘플 사용자','preferred_name':'박사님'},'purpose':{'purpose':'companion'},'preferences':boot['defaults'],
          'consent':{'long_term_memory':False,'conversation_storage':False,'biometric_identity':False,'cloud_transfer':False,'policy_version':boot['policy_version']},'review':{'confirmed':True}}
    for step in boot['steps']:x=send('PATCH',path+'/steps/'+step,{'expected_revision':x['revision'],'data':data[step]},token)
    payload={'expected_revision':x['revision'],'mutation_id':'demo-'+sid}
    result=send('POST',path+'/complete',payload,token)
    for _ in range(3):assert send('POST',path+'/complete',payload,token)==result
    application=send('POST',path+'/apply',{},token)
    if application['apply_status']=='failed':
        print('Simulated failure recorded:',application['error_code']);application=send('POST',path+'/apply',{},token)
    assert application['apply_status']=='applied' and application['hardware_connected'] is False
    assert len(application['acks'])==4
    greeting=send('POST',path+'/greeting',{},token);assert '박사님' in greeting['text']
    if result['profile_id']:
        context=send('GET','/v1/profiles/'+result['profile_id']+'/context',token=token)
        assert all(v is False for v in context['permissions'].values())
    else:assert kind=='guest'
    print(json.dumps({'registration_type':kind,'registration_status':result['registration_status'],
                      'apply_status':application['apply_status'],'adapter_mode':'simulated',
                      'hardware_connected':False,'greeting':greeting['text']},ensure_ascii=False))
    return result
if __name__=='__main__':
    run();run('demo-guest-01','guest')
    if os.environ.get('KER_GUARDIAN_TOKEN'):run('demo-guardian-01','guardian',os.environ['KER_GUARDIAN_TOKEN'])
