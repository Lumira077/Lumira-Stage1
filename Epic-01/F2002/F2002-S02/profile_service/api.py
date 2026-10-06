"""Loopback-only development HTTP adapter, opaque Bearer token -> fixed identity."""
import argparse,json,os,secrets
from http.server import HTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlsplit
from . import Service
from profile_contract import Error,require

def server(service,token,actor='local-demo-owner',port=8082):
    require(isinstance(token,str) and len(token)>=32,'TOKEN_REQUIRED')
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass # URLs/headers/bodies may contain private values.
        def handle_request(self):
            try:
                require(secrets.compare_digest(self.headers.get('Authorization','').encode(),('Bearer '+token).encode()),'UNAUTHORIZED',401)
                path=urlsplit(self.path).path.strip('/').split('/');method=self.command
                data={}
                if method in ('POST','PATCH','DELETE'):
                    try:n=int(self.headers.get('Content-Length','0'))
                    except ValueError:raise Error('INVALID_CONTENT_LENGTH')
                    require(0<n<=16384,'BODY_TOO_LARGE',413)
                    require(self.headers.get('Content-Type','').split(';')[0]=='application/json','JSON_REQUIRED',415)
                    try:data=json.loads(self.rfile.read(n))
                    except (ValueError,UnicodeDecodeError):raise Error('INVALID_JSON',400)
                    require(isinstance(data,dict))
                if path==['profiles'] and method=='GET':result=service.list(actor)
                elif path==['profiles'] and method=='POST':
                    require(set(data)=={'data','mutation_id'});result=service.create(actor,data['data'],data['mutation_id'])
                elif len(path)==2 and path[0]=='profiles':
                    pid=path[1]
                    if method=='GET':result=service.get(pid,actor)
                    elif method=='PATCH':
                        require(set(data)=={'changes','revision','mutation_id'});result=service.update(pid,actor,data['changes'],data['revision'],data['mutation_id'])
                    elif method=='DELETE':
                        require(set(data)=={'revision'});service.delete(pid,actor,data['revision']);result={'deleted':True}
                    else:raise Error('METHOD_NOT_ALLOWED',405)
                else:raise Error('NOT_FOUND',404)
                self.respond(200,result)
            except Error as e:self.respond(e.status,{'error_code':e.code})
            except Exception:self.respond(500,{'error_code':'INTERNAL_ERROR'})
        def respond(self,status,body):
            raw=json.dumps(body,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
        do_GET=do_POST=do_PATCH=do_DELETE=handle_request
    return HTTPServer(('127.0.0.1',port),Handler)
def main():
    p=argparse.ArgumentParser();p.add_argument('--db',default='profiles.sqlite3');p.add_argument('--port',type=int,default=8082);args=p.parse_args()
    token=os.environ.get('KER_PROFILE_DEV_TOKEN');require(token is not None,'SET_KER_PROFILE_DEV_TOKEN')
    s=Service(args.db);http=server(s,token,port=args.port)
    print('Development-only profile API listening on loopback; authentication required.')
    try:http.serve_forever()
    except KeyboardInterrupt:pass
    finally:http.server_close();s.close()
if __name__=='__main__':main()
