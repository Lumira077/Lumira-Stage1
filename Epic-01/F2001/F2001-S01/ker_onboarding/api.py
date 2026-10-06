"""Loopback-only reference HTTP API; no robot/device authentication implemented."""
import argparse
import hmac
import json
import os
import re
from pathlib import Path
from wsgiref.simple_server import make_server, WSGIRequestHandler
from .service import Service, Error, require

class QuietHandler(WSGIRequestHandler):
    def log_message(self, *args):
        pass  # URLs, payloads and tokens must not enter access logs.

class Application:
    def __init__(self, service, principals):
        self.service, self.principals = service, principals

    def __call__(self, env, start_response):
        status, result = 200, None
        try:
            method, path = env['REQUEST_METHOD'], env['PATH_INFO']
            if method == 'GET' and path == '/health':
                result = {'status': 'ok', 'scope': 'F2001-S01 reference'}
            elif method == 'GET' and path == '/openapi.json':
                result = json.loads((Path(__file__).parent.parent/'docs/openapi.json').read_text())
            else:
                header = env.get('HTTP_AUTHORIZATION', '')
                token = header[7:] if header.startswith('Bearer ') else ''
                principal = next((p for p in self.principals
                                  if hmac.compare_digest(p['token'].encode(), token.encode())), None)
                require(principal is not None, 'UNAUTHORIZED', 401)
                size = env.get('CONTENT_LENGTH', '')
                require(size.isdigit() or size == '', 'INVALID_CONTENT_LENGTH', 400)
                n = int(size or 0)
                require(n <= 16384, 'BODY_TOO_LARGE', 413)
                try:
                    body = json.loads(env['wsgi.input'].read(n)) if n else {}
                except (ValueError, UnicodeError):
                    raise Error(400, 'INVALID_JSON')
                require(isinstance(body, dict), 'INVALID_BODY', 400)
                actor = principal['actor_id']
                match = re.fullmatch(r'/v1/onboarding/sessions/([^/]+)(?:/(steps/([^/]+)|complete|cancel))?', path)
                if method == 'POST' and path == '/v1/onboarding/sessions':
                    require(set(body) == {'device_id'}, 'INVALID_BODY', 400)
                    result = self.service.create(actor, body['device_id'], principal['device_ids'])
                    status = 201
                elif match:
                    sid, action, step = match.groups()
                    if method == 'GET' and action is None:
                        result = self.service.get(sid, actor)
                    elif method == 'PATCH' and step:
                        require(set(body) == {'expected_revision', 'data'}, 'INVALID_BODY', 400)
                        result = self.service.save_step(sid, actor, step, body['data'], body['expected_revision'])
                    elif method == 'POST' and action == 'complete':
                        require(set(body) == {'expected_revision', 'mutation_id'}, 'INVALID_BODY', 400)
                        result = self.service.complete(sid, actor, body['mutation_id'], body['expected_revision'])
                    elif method == 'POST' and action == 'cancel':
                        require(not body, 'INVALID_BODY', 400)
                        result = self.service.cancel(sid, actor)
                    else:
                        raise Error(405, 'METHOD_NOT_ALLOWED')
                else:
                    raise Error(404, 'NOT_FOUND')
        except Error as exc:
            status, result = exc.status, {'error_code': exc.code}
        except Exception:
            status, result = 500, {'error_code': 'INTERNAL_ERROR'}
        payload = json.dumps(result, ensure_ascii=False).encode()
        labels = {200:'OK',201:'Created',400:'Bad Request',401:'Unauthorized',403:'Forbidden',404:'Not Found',
                  405:'Method Not Allowed',409:'Conflict',410:'Gone',413:'Content Too Large',422:'Unprocessable Content',500:'Internal Server Error'}
        start_response(f'{status} {labels[status]}', [('Content-Type','application/json; charset=utf-8'),
                       ('Content-Length',str(len(payload))), ('Cache-Control','no-store')])
        return [payload]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', default='data/onboarding.sqlite3')
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()
    token = os.environ.get('KER_DEMO_TOKEN', '')
    if len(token) < 24:
        parser.error('Set KER_DEMO_TOKEN to a random value of at least 24 characters.')
    Path(args.db).parent.mkdir(parents=True, exist_ok=True)
    service = Service(args.db)
    service.purge_expired()
    app = Application(service, [{'token':token,'actor_id':'local-demo-owner','device_ids':['demo-device-01']}])
    print(f'F2001-S01 reference API: http://127.0.0.1:{args.port}/openapi.json')
    try:
        with make_server('127.0.0.1', args.port, app, handler_class=QuietHandler) as server:
            server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        service.close()

if __name__ == '__main__':
    main()
