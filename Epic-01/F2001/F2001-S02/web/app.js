'use strict';
const $=id=>document.getElementById(id);
let boot=null,session=null,index=0,busy=false;
const names={registration:'등록 유형',language:'언어',profile:'닉네임·호칭',purpose:'사용 목적',preferences:'음성·표현 선호',consent:'목적별 동의',review:'최종 확인'};
const consents={long_term_memory:'장기 기억',conversation_storage:'대화 원문 저장',biometric_identity:'생체 식별',cloud_transfer:'클라우드 전송'};
function show(v){$('result').textContent=typeof v==='string'?v:JSON.stringify(v,null,2);}
async function api(method,path,data){const res=await fetch(path,{method,headers:{Authorization:'Bearer '+$('token').value,'Content-Type':'application/json'},body:data===undefined?undefined:JSON.stringify(data)});const value=await res.json();if(!res.ok)throw new Error(value.error_code||res.status);return value;}
function base(){if(!session)throw new Error('설정을 먼저 시작하세요.');return '/v1/onboarding/sessions/'+session.session_id;}
function field(key,label,type='text',value='',options=null){const l=document.createElement('label');l.textContent=label;const e=document.createElement(options?'select':'input');e.id='f_'+key;if(options)for(const [v,t] of options){const o=document.createElement('option');o.value=v;o.textContent=t;e.append(o);}else e.type=type;if(type==='checkbox')e.checked=!!value;else e.value=value;l.append(e);$('fields').append(l);return e;}
function draw(){if(!boot||!session)return;const step=boot.steps[index],data=session.draft[step]||{};$('wizard').hidden=false;$('heading').textContent=names[step];$('progress').textContent=`${index+1}/${boot.steps.length} · revision ${session.revision} · ${session.status}`;$('fields').replaceChildren();$('review').textContent='';
 if(step==='registration'){field('registration_type','등록 유형','text',data.registration_type||'self',[['self','본인'],['guardian','보호자 지원(승인된 시험 계정)'],['guest','게스트(임시 저장, 장기 기억 없음)']]);field('subject_id','대화 사용자 ID','text',data.subject_id||boot.actor_id);$('f_registration_type').onchange=()=>{$('f_subject_id').value=$('f_registration_type').value==='guest'?'guest':$('f_registration_type').value==='guardian'?(boot.guardian_subject_id||'demo-child-01'):boot.actor_id;};}
 if(step==='language')field('language','사용 언어','text',data.language||'ko-KR',[['ko-KR','한국어'],['en-US','English']]);
 if(step==='profile'){field('nickname','닉네임','text',data.nickname||'테스트 사용자');field('preferred_name','불러드릴 호칭','text',data.preferred_name||'박사님');}
 if(step==='purpose')field('purpose','사용 목적','text',data.purpose||'companion',[['companion','친구·대화'],['education','교육'],['care','돌봄'],['home','가정']]);
 if(step==='preferences'){const d={...boot.defaults,...data};field('voice_id','가상 음성 ID','text',d.voice_id,[['device_default','기본 음성'],['demo_voice_a','가상 음성 A']]);for(const [k,label] of [['speech_rate','말속도(0.7~1.3)'],['volume','음량(0~100)'],['expression_level','표정 수준(0~3)'],['gesture_level','제스처 수준(0~3)']]){const e=field(k,label,'number',d[k]);e.step=k==='speech_rate'?'0.1':'1';}}
 if(step==='consent'){for(const [k,l] of Object.entries(consents))field(k,l+' 동의','checkbox',data[k]||false);$('review').textContent='정책 버전: '+boot.policy_version+' · 모두 거부해도 기본 인사가 가능합니다. 게스트는 전부 거부해야 합니다.';}
 if(step==='review'){const confirm=field('confirmed','내용을 확인했고 등록하겠습니다.','checkbox',session.status==='committed' && !!data.confirmed);confirm.disabled=session.status!=='in_progress';$('review').textContent=JSON.stringify(session.draft,null,2);}
 $('back').disabled=index===0;$('skip').hidden=step!=='preferences';$('preview').hidden=step!=='preferences';$('next').disabled=session.status!=='in_progress';$('complete').disabled=!(session.status==='in_progress'&&session.draft.review);}
function values(){const step=boot.steps[index];const d={};$('fields').querySelectorAll('input,select').forEach(e=>d[e.id.slice(2)]=e.type==='checkbox'?e.checked:e.type==='number'?Number(e.value):e.value);if(step==='consent')d.policy_version=boot.policy_version;return d;}
function restored(x){session=x;localStorage.setItem('ker-s02-session',x.session_id);$('resumeId').value=x.session_id;const missing=boot.steps.findIndex(s=>!x.draft[s]);index=missing<0?boot.steps.length-1:missing;draw();show(x);}
function speak(r){show(r);if('speechSynthesis'in window){speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(r.text);u.lang=session?.draft.language?.language||'ko-KR';u.rate=r.preferences?.speech_rate||1;u.volume=Math.min(.2,(r.preferences?.volume??20)/100);speechSynthesis.speak(u);}}
function wire(id,fn){$(id).onclick=async()=>{if(busy)return;busy=true;try{await fn();}catch(e){show(e.message+(e.message==='REVISION_CONFLICT'?' · 세션 재개로 최신 상태를 조회하세요.':''));}finally{busy=false;}};}
wire('login',async()=>{boot=await api('GET','/v1/bootstrap');$('device').replaceChildren();for(const id of boot.device_ids){const o=document.createElement('option');o.value=id;o.textContent=id;$('device').append(o);}show(boot);});
wire('start',async()=>{if(!boot)throw new Error('먼저 연결 확인을 누르세요.');restored(await api('POST','/v1/onboarding/sessions',{device_id:$('device').value}));});
wire('resume',async()=>{if(!boot)throw new Error('먼저 연결 확인을 누르세요.');restored(await api('GET','/v1/onboarding/sessions/'+$('resumeId').value.trim()));});
for(const [id,connected]of[['reconnect',true],['disconnect',false]])wire(id,async()=>show(await api('POST','/v1/devices/'+$('device').value+'/connection',{connected})));
wire('back',async()=>{index=Math.max(0,index-1);draw();});
async function save(d){const step=boot.steps[index];session=await api('PATCH',base()+'/steps/'+step,{expected_revision:session.revision,data:d});index=Math.min(boot.steps.length-1,index+1);draw();show(session);}
wire('next',async()=>save(values()));wire('skip',async()=>save(boot.defaults));
wire('guide',async()=>speak(await api('POST',base()+'/guide',{step:boot.steps[index]})));
wire('preview',async()=>speak(await api('POST',base()+'/preview',{preferences:values()})));
wire('cancel',async()=>{session=await api('POST',base()+'/cancel',{});draw();show(session);});
wire('complete',async()=>{const r=await api('POST',base()+'/complete',{expected_revision:session.revision,mutation_id:'web-'+session.session_id});session=await api('GET',base());draw();show(r);});
wire('apply',async()=>show(await api('POST',base()+'/apply',{})));
wire('greet',async()=>{const r=await api('POST',base()+'/greeting',{});$('greeting').textContent=r.text;speak(r);});
$('resumeId').value=localStorage.getItem('ker-s02-session')||'';
