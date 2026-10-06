"""Static, escaped dashboard; no external assets, identities or credentials."""
import html,json

def build(metrics,release,alert_report):
    esc=lambda v:html.escape(str(v),quote=True)
    def fmt(r):return 'N/A' if r['value'] is None else f"{100*r['value']:.1f}% ({r['numerator']}/{r['denominator']})"
    cards=[('시작 세션',metrics['started_sessions']),('등록 완료',fmt(metrics['registration_completion'])),
           ('이용 준비',fmt(metrics['ready_completion'])),('재개 성공',fmt(metrics['resume_success'])),
           ('적용 실패',fmt(metrics['apply_failure'])),('지원 요청',fmt(metrics['support_request']))]
    cells=''.join(f'<article><h2>{esc(k)}</h2><strong>{esc(v)}</strong></article>' for k,v in cards)
    rows=''.join(f"<tr><td>{esc(k)}</td><td>{esc(fmt(v['dropout']))}</td><td>{esc(v['error_events'])}</td></tr>" for k,v in metrics['steps'].items())
    return '<!DOCTYPE html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>KER 온보딩 운영 검토</title><style>body{font-family:system-ui;background:#edf5fc;color:#17364f;margin:32px}main{max-width:1050px;margin:auto}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}article,section{background:white;border-radius:12px;padding:20px;margin:16px 0}h2{font-size:18px}strong{font-size:26px}table{width:100%;border-collapse:collapse}td,th{padding:12px;border-bottom:1px solid #ddd;text-align:left}pre{white-space:pre-wrap;overflow-wrap:anywhere}.notice{background:#fff0ce;padding:18px}</style><main><h1>KER 온보딩 운영 검토</h1><p class="notice">'+esc(metrics['scope']['mode'])+' 데이터 · 실제 사용자 평가와 운영 배포 증적을 구분합니다. Release 상태: '+esc(release['status'])+'</p><div class="grid">'+cells+'</div><section><h2>단계별 이탈</h2><table><thead><tr><th>단계</th><th>성숙한 관찰의 이탈</th><th>오류 이벤트</th></tr></thead><tbody>'+rows+'</tbody></table></section><section><h2>집계 기간·버전·분모</h2><pre>'+esc(json.dumps(metrics['scope'],ensure_ascii=False,indent=2))+'</pre><p>게스트는 등록 분모에서 제외하고 이용 준비 분모에 포함합니다. 동의 거부는 오류가 아니며 정상 취소는 이탈 집계에서 제외합니다.</p></section><section><h2>Release 차단 항목</h2><pre>'+esc(json.dumps(release,ensure_ascii=False,indent=2))+'</pre></section><section><h2>경보 검토</h2><pre>'+esc(json.dumps(alert_report,ensure_ascii=False,indent=2))+'</pre></section></main></html>'
