"""Authenticated loopback development API. Caller identity/profile/device are server-bound."""
import json,secrets
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlsplit
from memory_contract import Error,require

def server(service,token,actor,pid,device,port=0):
    require(isinstance(token,str) and len(token)>=32,'TOKEN_REQUIRED')
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def respond(self,status,value):
            raw=json.dumps(value,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
        def request(self):
            try:
                require(secrets.compare_digest(self.headers.get('Authorization','').encode(),('Bearer '+token).encode()),'UNAUTHORIZED',401)
                parts=urlsplit(self.path).path.strip('/').split('/');data={}
                if self.command!='GET':
                    try:n=int(self.headers.get('Content-Length','0'))
                    except ValueError:raise Error('INVALID_CONTENT_LENGTH',400)
                    require(0<n<=16384,'BODY_TOO_LARGE',413);require(self.headers.get('Content-Type','').split(';')[0]=='application/json','JSON_REQUIRED',415)
                    try:data=json.loads(self.rfile.read(n))
                    except (ValueError,UnicodeDecodeError):raise Error('INVALID_JSON',400)
                    require(isinstance(data,dict))
                if parts==['memories'] and self.command=='GET':value=service.list(actor,pid,device)
                elif parts==['memories'] and self.command=='POST':
                    require(set(data)=={'data','mutation_id'});value=service.create(actor,pid,device,data['data'],data['mutation_id'])
                elif parts==['search'] and self.command=='POST':
                    require(set(data)=={'query'});value=service.search(actor,pid,device,data['query'])
                elif len(parts)==2 and parts[0]=='memories' and self.command=='GET':value=service.get(actor,pid,device,parts[1])
                elif parts==['capture'] and self.command=='POST':
                    require(set(data)=={'utterance','source_ref','mutation_id'});value=service.capture(actor,pid,device,data['utterance'],data['source_ref'],data['mutation_id'])
                elif parts in (['privacy','delete-all'],['privacy','revoke'],['privacy','grant']) and self.command=='POST':
                    require(set(data)=={'confirmed'} and data['confirmed'] is True)
                    if parts[1]=='delete-all':service.delete_all(actor,pid)
                    elif parts[1]=='revoke':service.revoke(actor,pid)
                    else:service.grant(actor,pid)
                    value={'processed':True}
                elif len(parts)==3 and parts[0]=='memories' and parts[2]=='confirm' and self.command=='POST':
                    require(set(data)=={'revision','mutation_id'});value=service.confirm(actor,pid,device,parts[1],data['revision'],data['mutation_id'])
                elif len(parts)==2 and parts[0]=='memories' and self.command=='PATCH':
                    require(set(data)=={'content','revision','mutation_id'});value=service.correct(actor,pid,device,parts[1],data['content'],data['revision'],data['mutation_id'])
                elif len(parts)==2 and parts[0]=='memories' and self.command=='DELETE':
                    require(set(data)=={'revision'});service.delete(actor,pid,parts[1],data['revision']);value={'deleted':True}
                else:raise Error('NOT_FOUND',404)
                self.respond(200,value)
            except Error as e:self.respond(e.status,{'error_code':e.code})
            except Exception:self.respond(500,{'error_code':'INTERNAL_ERROR'})
        do_GET=do_POST=do_PATCH=do_DELETE=request
    return HTTPServer(('127.0.0.1',port),Handler)
