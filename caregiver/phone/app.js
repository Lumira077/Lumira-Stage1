import {t,locale,initLanguage,translateError,enumText} from './i18n.js';
import {initUi,resetUi,setLocalUi,showTab,closeMessage,updateDashboard,updateCommands,updateAlerts,setCallUi,setMediaUi,remoteReady} from './ui.js';
import {readOrigin,saveOrigin} from './mobile-config.js';
const webBase=window.Capacitor?'':new URL('.',import.meta.url).pathname.replace(/\/$/,'');
const $=id=>document.getElementById(id);
let apiOrigin=readOrigin(), mediaGeneration=0, sessionGeneration=0;
let token='', robot='', local=false, version=0, call=null, peer=null, stream=null, cursor=0, pollBusy=false;
let pendingIce=[], pollingMedia=false, runtimeBusy=false, connectTimer=null;
let robotSettings={}, robotEpoch=null;
const stoppedCalls=new Set();
const translatedOutputs=new Map();
function translatedText(id,key,values={}){translatedOutputs.set(id,{key,values});text(id,t(key,values));}
let languageRefresh=false,lastError=null,settingsDirty=false;
for(const id of ['volume','quiet','camera','microphone','remote_actions'])$(id).addEventListener('input',()=>{settingsDirty=true;});
window.addEventListener('lumira:language',async()=>{for(const [id,{key,values}] of translatedOutputs)text(id,t(key,values));if(lastError)text('error',translateError(lastError));if(!token)return;languageRefresh=true;try{await refresh();}catch(e){text('error',translateError(e));}finally{languageRefresh=false;}});
const roleName=r=>({owner:t("소유자"),caregiver:t("보호자"),viewer:t("조회 전용")}[r]||t("미지정"));
const text=(id,value)=>{$(id).textContent=value;};
async function api(path,method='GET',body,extra={}){
 const r=await fetch((apiOrigin||webBase)+'/v1'+path,{method,signal:AbortSignal.timeout(8000),headers:{'Content-Type':'application/json',...(token?{Authorization:'Bearer '+token}:{}),...extra},body:body===undefined?undefined:JSON.stringify(body)});
 const data=await r.json();if(!r.ok){const error=new Error(data.error||'요청 실패');error.status=r.status;throw error;}return data;
}
const base=()=>'/robots/'+encodeURIComponent(robot);
function run(fn){return async e=>{e?.preventDefault();lastError=null;text('error','');try{await fn(e);}catch(err){lastError=err;text('error',translateError(err));}};}
function item(list,label,action){const li=document.createElement('li');li.textContent=label;if(action){const b=document.createElement('button');b.textContent=action.label;b.onclick=run(action.fn);li.append(' ',b);}$(list).append(li);}
async function loginReady(){ sessionGeneration++;resetUi();setLocalUi(local); $('login').hidden=true;$('app').hidden=false;$('logout').hidden=false;$('selectLabel').hidden=local;$('pair').hidden=local;await refresh();}
$('apiOrigin').value=apiOrigin;
$('saveOrigin').onclick=run(async()=>{apiOrigin=saveOrigin($('apiOrigin').value);text('error',t("서버 주소를 저장했습니다. 로그인해 주세요."));});
$('registerForm').onsubmit=run(async()=>{
 const pw=$('registerPassword').value;if(pw!==$('registerPasswordConfirm').value)throw new Error(t("비밀번호 확인이 일치하지 않습니다."));
 try{const r=await api('/register','POST',{name:$('registerName').value.trim(),email:$('registerEmail').value.trim(),password:pw,role:$('registerRole').value,robot_id:$('registerRobot').value.trim()});translatedText('registrationResult','가입 완료 · 신청번호 {id} · 로그인 후 승인 상태를 확인하세요.',{id:r.registration_id});$('email').value=$('registerEmail').value.trim();}
 finally{$('registerPassword').value='';$('registerPasswordConfirm').value='';}
});
$('loginForm').onsubmit=run(async()=>{const r=await api('/login','POST',{email:$('email').value,password:$('password').value});token=r.token;$('password').value='';local=false;await loginReady();});
$('robotLogin').onclick=run(async()=>{robot=$('robotId').value.trim();token=$('robotToken').value.trim();$('robotToken').value='';local=true;await api(base()+'/status');await loginReady();$('robotRuntime').hidden=false;});
$('logout').onclick=run(async()=>{sessionGeneration++;try{try{await endCall('ended');}catch{}await api('/logout','POST',{});}finally{stopMedia();resetUi();token='';robot='';call=null;$('login').hidden=false;$('app').hidden=true;$('logout').hidden=true;}});
$('claim').onclick=run(async()=>{await api('/pairings/claim','POST',{code:$('pairCode').value.trim()});$('pairCode').value='';text('error',t("로봇 현장에서 연결을 승인해 주세요."));});
$('acceptInvite').onclick=run(async()=>{await api('/invitations/accept','POST',{code:$('inviteCode').value.trim()});$('inviteCode').value='';await refresh();});
$('refresh').onclick=run(refresh);$('robots').onchange=run(async()=>{sessionGeneration++;await endCall('ended');robot=$('robots').value;settingsDirty=false;await refresh();});
async function refresh(){
 if(!local){const me=await api('/me');text('sessionSummary',(me.user.name||me.user.email)+t(" · 내 계정"));text('registrationId',t("신청번호 ")+me.user.id);text('assignmentStatus',me.robots.length?t("승인된 로봇만 연결됩니다."):me.requests.map(r=>r.device+' · '+roleName(r.requested_role)+' · '+({pending:t("승인 대기"),approved:t("승인됨"),rejected:t("반려"),revoked:t("권한 회수")}[r.status]||r.status)).join(' / ')||t("지정된 로봇이 없습니다."));text('pendingSummary',$('assignmentStatus').textContent+t(" · 신청번호 ")+me.user.id);const rows=me.robots;$('robots').replaceChildren();for(const r of rows){const o=document.createElement('option');o.value=r.id;o.textContent=r.id+' · '+r.model+' · '+roleName(r.role);$('robots').append(o);}if(!rows.some(r=>r.id===robot))robot=rows[0]?.id||'';$('robots').value=robot;const role=rows.find(r=>r.id===robot)?.role;for(const id of ['settings','family'])$(id).hidden=role!=='owner';if(role)text('assignmentStatus',t('{robot} · {role} 권한으로 연결',{robot,role:roleName(role)}));$('actions').hidden=role==='viewer';for(const id of ['audioCall','videoCall']){$(id).disabled=role==='viewer';$(id).hidden=false;}$('quickMessage').disabled=role==='viewer';$('openSchedule').disabled=role==='viewer';}
 $('robotPanels').hidden=!robot;$('noRobot').hidden=!!robot;if(robot)await panels();
}
async function panels(){
 if(local)await robotTick();
 const r=await api(base()+'/status');text('status',t('{robot} · {model} · {online} · 배터리 {battery}% · {mode} · 수신 {received}',{robot,model:r.model,online:r.online?t('연결됨'):t('연결 끊김'),battery:r.status.battery??t('미확인'),mode:r.status.mode==='simulation'?t('모의 기기'):r.status.mode==='browser-runtime'?t('브라우저 기기 · 실물 센서 미연결'):'',received:r.received_at?new Date(r.received_at*1000).toLocaleString(locale()):t('없음')}));
 updateDashboard(r);
 const s=await api(base()+'/settings');version=s.version;text('settingsStatus',t('설정 요청 버전 {version} · 보고 설정 {reported}',{version,reported:s.reported?JSON.stringify(s.reported):t('미수신')}));
 // Preserve unsaved settings while editing.
 if(!languageRefresh&&!settingsDirty&&!$('settings').contains(document.activeElement)){for(const k of ['quiet','camera','microphone','remote_actions'])$(k).checked=s.desired[k];$('volume').value=s.desired.volume;}
 $('localPair').hidden=!local;
 if(local){robotSettings=s.desired;robotEpoch=r.epoch;}
 if(local){for(const id of ['actions','settings','family','audioCall','videoCall'])$(id).hidden=true;const p=await api(base()+'/pairing');if(p.length)text('generatedPair',t("연결 요청이 있습니다. 현장 사용자 확인 후 승인해 주세요."));}
 else{
 const commandRows=await api(base()+'/commands');updateCommands(commandRows);$('commands').replaceChildren();for(const c of commandRows)item('commands',`${enumText(c.kind)} · ${enumText(c.state)} · ${enumText(c.result||'')}`);
 const alertRows=await api(base()+'/alerts');updateAlerts(alertRows);$('alerts').replaceChildren();for(const a of alertRows)item('alerts',`${enumText(a.payload.kind)} · ${a.read?t("확인함"):t("미확인")} · ${new Date(a.created*1000).toLocaleString(locale())}`,a.read?null:{label:t("확인"),fn:async()=>{await api(base()+'/alerts','PATCH',{id:a.id});await panels();}});
 if(!$('family').hidden){$('accessRequests').replaceChildren();for(const q of await api(base()+'/access-requests')){
 const li=document.createElement('li');li.textContent=q.name+' · '+q.email+' · '+roleName(q.requested_role)+t(" · 신청번호 ")+q.registration_id;
 if(q.requested_role==='caregiver')for(const [decision,label] of [['approve',t("신원 확인 후 승인")],['reject',t("반려")]]){const b=document.createElement('button');b.textContent=label;b.onclick=run(async()=>{if(!confirm(t('{email} · 신청번호 {id}의 {decision}을 진행할까요?',{email:q.email,id:q.registration_id,decision:label})))return;await api(base()+'/access-requests','PATCH',{registration_id:q.registration_id,decision});await refresh();});li.append(' ',b);}
 $('accessRequests').append(li);
 }$('members').replaceChildren();for(const m of await api(base()+'/members'))item('members',`${m.email} · ${roleName(m.role)}`,m.role==='owner'?null:{label:t("권한 회수"),fn:async()=>{await api(base()+'/members','DELETE',{user:m.user});await panels();}});}
 }
 await pollCall();
}
async function command(kind,payload){await api(base()+'/commands','POST',{kind,payload},{'Idempotency-Key':crypto.randomUUID()});await panels();closeMessage();}
$('sendMessage').onclick=run(()=>command('message',{text:$('message').value}));$('sendReminder').onclick=run(()=>command('reminder',{text:$('message').value,...($('reminderAt').value?{not_before:new Date($('reminderAt').value).getTime()/1000}:{})}));
for(const b of document.querySelectorAll('[data-kind]'))b.onclick=run(()=>command(b.dataset.kind,{name:b.dataset.name}));
$('saveSettings').onclick=run(async()=>{const patch={volume:Number($('volume').value)};for(const k of ['quiet','camera','microphone','remote_actions'])patch[k]=$(k).checked;await api(base()+'/settings','PATCH',{patch},{'If-Match':String(version)});settingsDirty=false;await panels();});
$('invite').onclick=run(async()=>{const r=await api(base()+'/invitations','POST',{role:$('inviteRole').value});translatedText('generatedInvite','10분 안에 사용할 초대 코드: {code}',{code:r.code});});
$('reset').onclick=run(async()=>{if(confirm(t("모든 보호자 연결을 해제하고 대기 명령과 통화를 종료할까요?"))){await api(base()+'/reset','POST',{});await refresh();}});
$('makePair').onclick=run(async()=>{const r=await api(base()+'/pairing','POST',{});text('generatedPair',t("5분 이내 연결 코드: ")+r.code);});
for(const [id,approve] of [['approvePair',true],['denyPair',false]])$(id).onclick=run(async()=>{await api(base()+'/pairing','PATCH',{approve});text('generatedPair',approve?t("승인 완료"):t("거절 완료"));});
for(const [id,video] of [['audioCall',false],['videoCall',true]])$(id).onclick=run(async()=>{const r=await api(base()+'/calls','POST',{video});call={...r,video};await pollCall();});
$('acceptCall').onclick=run(async()=>{
 // getUserMedia happens only after the physical user presses accept.
 try{await startMedia(Boolean(call.video));await api(base()+'/calls/'+call.id,'PATCH',{state:'active'});await pollCall();}catch(e){stopMedia();throw e;}
});
$('rejectCall').onclick=run(()=>endCall('rejected'));$('hangup').onclick=run(()=>endCall('ended'));
async function endCall(state){const id=call?.id;if(id)stoppedCalls.add(id);stopMedia();call=null;if(id){await api(base()+'/calls/'+id,'PATCH',{state});}text('callState',t("통화 종료"));}
function stopMedia(){mediaGeneration++;clearTimeout(connectTimer);connectTimer=null;if('speechSynthesis' in window)speechSynthesis.cancel();if(peer){peer.close();peer=null;}if(stream){stream.getTracks().forEach(t=>t.stop());stream=null;}$('localVideo').srcObject=null;$('remoteVideo').srcObject=null;pendingIce=[];cursor=0;text('mediaState',t("카메라·마이크 꺼짐"));$('remoteVideo').muted=false;$('playRemote').hidden=true;setMediaUi(null,null);setCallUi(null);}
async function startMedia(video){
 if(peer)return;
 if(!navigator.mediaDevices?.getUserMedia)throw new Error(t("통화에는 HTTPS와 카메라·마이크 권한이 필요합니다."));
 const generation=mediaGeneration;
 const acquired=await navigator.mediaDevices.getUserMedia({audio:true,video});
 if(generation!==mediaGeneration){acquired.getTracks().forEach(t=>t.stop());throw new Error(t("통화 요청이 종료되었습니다."));}
 stream=acquired;$('localVideo').srcObject=stream;
 const conf=$('iceConfig').value.trim()?JSON.parse($('iceConfig').value):{iceServers:[]};peer=new RTCPeerConnection(conf);
 connectTimer=setTimeout(()=>{if(peer&&peer.connectionState!=='connected')endCall('ended').catch(stopMedia).finally(()=>text('error',t("통화 연결 시간이 초과되었습니다. 네트워크와 TURN 설정을 확인한 뒤 다시 요청하세요.")));},30000);
 for(const t of stream.getTracks())peer.addTrack(t,stream);
 peer.ontrack=e=>{$('remoteVideo').srcObject=e.streams[0];remoteReady();};
 peer.onicecandidate=e=>{if(e.candidate&&call)api(base()+'/calls/'+call.id+'/signals','POST',{type:'ice',candidate:e.candidate.toJSON()}).catch(()=>stopMedia());};
 peer.onconnectionstatechange=()=>{if(peer?.connectionState==='connected'){clearTimeout(connectTimer);connectTimer=null;setMediaUi(stream,peer);}if(peer&&['failed','disconnected','closed'].includes(peer.connectionState)){endCall('ended').catch(stopMedia);text('callState',t("연결이 종료되었습니다. 다시 통화를 요청하세요."));}};
 text('mediaState',video?t("카메라·마이크 사용 중"):t("마이크 사용 중 · 카메라 꺼짐"));setMediaUi(stream,peer);
}
async function pollCall(){
 if(pollingMedia||!token)return;pollingMedia=true;
 const generation=sessionGeneration, selectedRobot=robot;
 const current=()=>generation===sessionGeneration&&selectedRobot===robot&&!!token;
 try{
 if(!call){const rows=await api(base()+'/calls');if(!current())return;call=rows[0]||null;}
 if(!call){for(const id of ['acceptCall','rejectCall','hangup'])$(id).hidden=true;setCallUi(null);return;}
 const fresh=await api(base()+'/calls/'+call.id);if(!current())return;call=fresh;if(stoppedCalls.has(fresh.id)){stopMedia();call=null;return;}text('callState',fresh.state==='ringing'?t("통화 요청 · 로봇 사용자 수락 대기"):fresh.state==='active'?t("통화 연결 중"): t("통화 종료"));
 setCallUi(fresh);
 $('acceptCall').hidden=$('rejectCall').hidden=!(local&&fresh.state==='ringing');$('hangup').hidden=!['active','ringing'].includes(fresh.state);
 if(!['ringing','active'].includes(fresh.state)){stopMedia();call=null;return;}
 if(fresh.state==='active'){
   if(!peer){await startMedia(Boolean(fresh.video));if(!local){const offer=await peer.createOffer();await peer.setLocalDescription(offer);await api(base()+'/calls/'+fresh.id+'/signals','POST',{type:'offer',sdp:offer.sdp});}}
   const rows=await api(base()+'/calls/'+fresh.id+'/signals');
   for(const s of rows){if(s.seq<=cursor)continue;const v=s.payload;
     if(v.type==='ice'){if(peer.remoteDescription)await peer.addIceCandidate(v.candidate);else pendingIce.push(v.candidate);}
     else{await peer.setRemoteDescription({type:v.type,sdp:v.sdp});for(const c of pendingIce)await peer.addIceCandidate(c);pendingIce=[];if(v.type==='offer'){const answer=await peer.createAnswer();await peer.setLocalDescription(answer);await api(base()+'/calls/'+fresh.id+'/signals','POST',{type:'answer',sdp:answer.sdp});}}
     cursor=s.seq;
   }
 }
 }catch(e){stopMedia();text('error',t("통화 중단: ")+translateError(e));throw e;}finally{pollingMedia=false;}
}
setInterval(async()=>{if(!token||pollBusy)return;pollBusy=true;try{if(local&&robot)await panels();else await refresh();}catch(e){stopMedia();text('error',translateError(e));}finally{pollBusy=false;}},3000);
window.addEventListener('pagehide',stopMedia);document.addEventListener('visibilitychange',()=>{if(document.hidden&&stream){endCall('ended').catch(stopMedia);}});
if(!window.Capacitor&&'serviceWorker' in navigator)navigator.serviceWorker.register(new URL('./sw.js',import.meta.url)).catch(()=>{});

// Browser runtime: one executor per device. Do not run the Python simulation agent concurrently.
function ledger(){return new Promise((resolve,reject)=>{const req=indexedDB.open('lumira-executions',1);req.onupgradeneeded=()=>req.result.createObjectStore('commands');req.onsuccess=()=>resolve(req.result);req.onerror=()=>reject(req.error);});}
async function reserve(id){const db=await ledger();return new Promise((resolve,reject)=>{const tx=db.transaction('commands','readwrite'),store=tx.objectStore('commands');let exists=false;const q=store.get(robot+':'+id);q.onsuccess=()=>{exists=q.result!==undefined;if(!exists)store.put('reserved',robot+':'+id);};tx.oncomplete=()=>{db.close();resolve(!exists);};tx.onerror=()=>{db.close();reject(tx.error);};});}
async function robotTick(){
 if(runtimeBusy)return;runtimeBusy=true;
 try{
 const capabilities=['expression','content'];if('speechSynthesis' in window)capabilities.push('message','reminder');
 const state=await api(base()+'/status','POST',{battery:null,capabilities,mode:'browser-runtime',reported_settings:robotSettings});if((robotEpoch!==null&&robotEpoch!==state.epoch)||state.settings.quiet){if('speechSynthesis' in window)speechSynthesis.cancel();$('localConsent').checked=false;}robotSettings=state.settings;robotEpoch=state.epoch;
 for(const c of await api(base()+'/commands')){
 let result='rejected',reason='local permission disabled';
 if(c.epoch===robotEpoch&&c.expires>Date.now()/1000&&!robotSettings.quiet&&$('localConsent').checked&&capabilities.includes(c.kind)){
   if(await reserve(c.id)){
     if(c.kind==='message'||c.kind==='reminder'){
       if(call?.state==='active'){reason='call active';}
       else{const speech=new SpeechSynthesisUtterance(c.payload.text);speech.lang=/[가-힣]/.test(c.payload.text)?'ko-KR':/[A-Za-z]/.test(c.payload.text)?'en-US':locale();speech.volume=robotSettings.volume/100;speechSynthesis.speak(speech);text('robotOutput',c.payload.text);result='applied';reason='browser speech queued';}
     }else if(c.kind==='expression'&&robotSettings.remote_actions){text('face',c.payload.name==='happy'?'●ᴗ●':c.payload.name==='listening'?'●◡●':'●_●');result='applied';reason='display updated';}
     else if(c.kind==='content'){text('robotOutput',c.payload.name==='breathing'?t("천천히 숨을 들이쉬고, 내쉬어요."):t("안녕하세요. 오늘 기분은 어떤가요?"));result='applied';reason='display updated';}
   }else{result='uncertain';reason='persistent replay prevented';}
 }else if(c.epoch!==robotEpoch)reason='owner epoch mismatch';else if(c.expires<=Date.now()/1000)reason='expired';
 await api(base()+'/commands','PATCH',{id:c.id,state:result,result:reason});
 }
 }catch(e){if('speechSynthesis' in window)speechSynthesis.cancel();throw e;}finally{runtimeBusy=false;}
}
$('localConsent').onchange=()=>{if(!$('localConsent').checked&&'speechSynthesis' in window)speechSynthesis.cancel();};

// Read-only diagnostics for verification; credentials and SDP are never exported.
export async function mediaDiagnostics(){
 const reports=peer?Array.from((await peer.getStats()).values()):[];
 return {connection:peer?.connectionState||'closed',signaling:peer?.signalingState,ice:peer?.iceConnectionState,gathering:peer?.iceGatheringState,candidateCount:reports.filter(s=>s.type==='local-candidate').length,pairs:reports.filter(s=>s.type==='candidate-pair').map(s=>({state:s.state,nominated:s.nominated})),localDescription:peer?.localDescription?.type,remoteDescription:peer?.remoteDescription?.type,inbound:reports.filter(s=>s.type==='inbound-rtp').map(s=>({kind:s.kind,bytesReceived:s.bytesReceived,packetsReceived:s.packetsReceived,framesDecoded:s.framesDecoded,totalAudioEnergy:s.totalAudioEnergy})),localTracks:stream?.getTracks().map(t=>({kind:t.kind,readyState:t.readyState}))||[]};
}

initLanguage();
initUi({
 hangup:run(()=>endCall('ended')),
 mic:()=>{for(const t of stream?.getAudioTracks()||[])t.enabled=!t.enabled;setMediaUi(stream,peer);},
 camera:()=>{for(const t of stream?.getVideoTracks()||[])t.enabled=!t.enabled;setMediaUi(stream,peer);},
 sound:()=>{$('remoteVideo').muted=!$('remoteVideo').muted;setMediaUi(stream,peer);}
});
export { endCall, stopMedia };
