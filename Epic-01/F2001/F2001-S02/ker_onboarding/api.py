"""Loopback-only prototype API and static wizard. Uses no third-party services."""
import argparse
import hmac
import json
import os
import re
from pathlib import Path
from wsgiref.simple_server import make_server, WSGIRequestHandler
from .core import Error, require, STEPS, DEFAULTS
from .service import Service, POLICY_VERSION
from .adapters import SimulatedOutputs
ROOT=Path(__file__).resolve().parent.parent
class QuietHandler(WSGIRequestHandler):
    def log_message(self,*args):pass

class Application:
    def __init__(self,service,principals):self.service,self.principals=service,principals
    def __call__(self,env,start_response):
        status=200;kind='application/json; charset=utf-8'
        try:
            method,path=env['REQUEST_METHOD'],env['PATH_INFO']
            require(env.get('HTTP_HOST','').split(':')[0] in ('127.0.0.1','localhost',''), 'INVALID_HOST',403)
            origin=env.get('HTTP_ORIGIN')
            if origin:require(origin in ('http://'+env.get('HTTP_HOST',''),), 'INVALID_ORIGIN',403)
            if method=='GET' and path in ('/','/app.js','/style.css'):
                name={'/':'index.html','/app.js':'app.js','/style.css':'style.css'}[path]
                kind={'/':'text/html; charset=utf-8','/app.js':'application/javascript; charset=utf-8','/style.css':'text/css; charset=utf-8'}[path]
                result=(ROOT/'web'/name).read_bytes()
            elif method=='GET' and path=='/health':result={'status':'ok','scope':'F2001-S02 prototype','adapter_mode':'simulated'}
            elif method=='GET' and path=='/openapi.json':result=json.loads((ROOT/'docs/openapi.json').read_text())
            else:
                header=env.get('HTTP_AUTHORIZATION','');token=header[7:] if header.startswith('Bearer ') else ''
                principal=next((p for p in self.principals if hmac.compare_digest(p['token'].encode(),token.encode())),None)
                require(principal is not None,'UNAUTHORIZED',401)
                size=env.get('CONTENT_LENGTH','');require(size=='' or size.isdigit(),'INVALID_CONTENT_LENGTH',400)
                n=int(size or 0);require(n<=16384,'BODY_TOO_LARGE',413)
                try:body=json.loads(env['wsgi.input'].read(n)) if n else {}
                except (ValueError,UnicodeError):raise Error(400,'INVALID_JSON')
                require(isinstance(body,dict),'INVALID_BODY',400)
                actor=principal['actor_id'];device_ids=principal['device_ids']
                def keys(expected):require(set(body)==set(expected),'INVALID_BODY',400)
                sm=re.fullmatch(r'/v1/onboarding/sessions/([^/]+)(?:/(steps/([^/]+)|complete|cancel|application|apply|greeting|guide|preview))?',path)
                dm=re.fullmatch(r'/v1/devices/([^/]+)(/connection)?',path)
                pm=re.fullmatch(r'/v1/profiles/([^/]+)/context',path)
                if method=='GET' and path=='/v1/bootstrap':
                    result={'actor_id':actor,'device_ids':device_ids,'steps':STEPS,'defaults':DEFAULTS,
                            'policy_version':POLICY_VERSION,'adapter_mode':'simulated','hardware_connected':False,
                            'guardian_subject_id':'demo-child-01' if actor=='local-demo-guardian' else None}
                elif method=='POST' and path=='/v1/onboarding/sessions':
                    keys(['device_id']);result=self.service.create(actor,body['device_id'],device_ids);status=201
                elif dm:
                    device,action=dm.groups();require(device in device_ids,'DEVICE_NOT_AUTHORIZED',403)
                    if method=='GET' and action is None:result=self.service.devices.inspect(actor,device)
                    elif method=='POST' and action:keys(['connected']);result=self.service.devices.set_connected(actor,device,body['connected'])
                    else:raise Error(405,'METHOD_NOT_ALLOWED')
                elif pm and method=='GET':result=self.service.context(pm[1],actor)
                elif sm:
                    sid,action,step=sm.groups()
                    if method=='GET' and action is None:result=self.service.get(sid,actor)
                    elif method=='PATCH' and step:keys(['expected_revision','data']);result=self.service.save_step(sid,actor,step,body['data'],body['expected_revision'])
                    elif method=='POST' and action=='complete':keys(['expected_revision','mutation_id']);result=self.service.complete(sid,actor,body['mutation_id'],body['expected_revision'])
                    elif method=='POST' and action=='cancel':keys([]);result=self.service.cancel(sid,actor)
                    elif method=='GET' and action=='application':result=self.service.application(sid,actor)
                    elif method=='POST' and action=='apply':keys([]);result=self.service.apply(sid,actor)
                    elif method=='POST' and action=='greeting':keys([]);result=self.service.greeting(sid,actor)
                    elif method=='POST' and action=='guide':keys(['step']);result=self.service.guide(sid,actor,body['step'])
                    elif method=='POST' and action=='preview':keys(['preferences']);result=self.service.preview(sid,actor,body['preferences'])
                    else:raise Error(405,'METHOD_NOT_ALLOWED')
                else:raise Error(404,'NOT_FOUND')
        except Error as e:status,result=e.status,{'error_code':e.code}
        except Exception:status,result=500,{'error_code':'INTERNAL_ERROR'}
        payload=result if isinstance(result,bytes) else json.dumps(result,ensure_ascii=False,allow_nan=False).encode()
        labels={200:'OK',201:'Created',400:'Bad Request',401:'Unauthorized',403:'Forbidden',404:'Not Found',405:'Method Not Allowed',409:'Conflict',410:'Gone',413:'Content Too Large',422:'Unprocessable Content',500:'Internal Server Error'}
        start_response(f'{status} {labels[status]}',[('Content-Type',kind),('Content-Length',str(len(payload))),
            ('Cache-Control','no-store'),('X-Content-Type-Options','nosniff'),
            ('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; frame-ancestors 'none'; form-action 'self'; base-uri 'none'")])
        return [payload]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--db',default='data/prototype.sqlite3');parser.add_argument('--port',type=int,default=8081)
    args=parser.parse_args();token=os.environ.get('KER_DEMO_TOKEN','');guardian=os.environ.get('KER_GUARDIAN_TOKEN','')
    if len(token)<24:parser.error('Set KER_DEMO_TOKEN to a random value of at least 24 characters.')
    if guardian and (len(guardian)<24 or guardian==token):parser.error('Use a different random KER_GUARDIAN_TOKEN of at least 24 characters.')
    mode=os.environ.get('KER_ADAPTER_MODE','simulated')
    if mode!='simulated':parser.error('Only simulated adapters are implemented; hardware mode is unsupported.')
    fail=os.environ.get('KER_SIM_FAIL_ONCE','')
    if fail and fail not in SimulatedOutputs.modules:parser.error('Unknown KER_SIM_FAIL_ONCE module.')
    Path(args.db).parent.mkdir(parents=True,exist_ok=True)
    service=Service(args.db,outputs=SimulatedOutputs(fail_once=fail or None))
    principals=[{'token':token,'actor_id':'local-demo-owner','device_ids':['demo-device-01','demo-guest-01']}]
    if guardian:principals.append({'token':guardian,'actor_id':'local-demo-guardian','device_ids':['demo-guardian-01']})
    app=Application(service,principals);print(f'F2001-S02 SIMULATED prototype: http://127.0.0.1:{args.port}')
    try:
        with make_server('127.0.0.1',args.port,app,handler_class=QuietHandler) as server:
            while True:
                service.purge_expired();server.timeout=1;server.handle_request()
    except KeyboardInterrupt:pass
    finally:service.close()
if __name__=='__main__':main()
