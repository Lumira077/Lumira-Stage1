import {t,locale,initLanguage} from './i18n.js';
const $=id=>document.getElementById(id);
let lastCommands=[],lastCall=null,lastStream=null,lastPeer=null;
let currentTab='home',lastStatus=null,callStarted=0,returnFocus=null;
const label=(id,value)=>{$(id).textContent=value;};
export function showTab(name){
 if(!['home','alerts','settings'].includes(name))return;
 currentTab=name;for(const p of document.querySelectorAll('[data-panel]'))p.hidden=p.dataset.panel!==name;
 for(const b of document.querySelectorAll('[data-tab]')){if(b.dataset.tab===name)b.setAttribute('aria-current','page');else b.removeAttribute('aria-current');}
 window.scrollTo({top:0,behavior:'instant'});
}
export function openMessage(){if($('quickMessage').disabled)return;if(!$('messageSheet').open)$('messageSheet').showModal();}
export function closeMessage(){$('messageSheet').close();}
export function setLocalUi(local){$('bottomNav').hidden=local;$('headerAlerts').hidden=local;$('quickMessage').hidden=local;$('openSchedule').disabled=local;}
export function resetUi(){closeMessage();setCallUi(null);showTab('home');}
export function initUi(callbacks){
 const native=window.Capacitor?.getPlatform?.();document.documentElement.dataset.platform=native==='ios'||(native!=='android'&&/iPhone|iPad|iPod/.test(navigator.userAgent))?'ios':'android';
 for(const b of document.querySelectorAll('[data-tab]'))b.onclick=()=>showTab(b.dataset.tab);
 document.querySelector('.brand').onclick=e=>{e.preventDefault();showTab('home');};
 $('headerAlerts').onclick=()=>showTab('alerts');$('openPair').onclick=()=>showTab('settings');
 $('quickMessage').onclick=openMessage;$('openSchedule').onclick=()=>{openMessage();$('reminderAt').focus();};$('closeMessage').onclick=closeMessage;
 $('closeCall').onclick=callbacks.hangup;$('toggleMic').onclick=callbacks.mic;$('toggleCamera').onclick=callbacks.camera;$('toggleSound').onclick=callbacks.sound;
 $('playRemote').onclick=()=>{$('remoteVideo').play().then(()=>{$('playRemote').hidden=true;}).catch(()=>{});};
 $('phoneTimezone').textContent=t("이 폰 시간 기준 · ")+Intl.DateTimeFormat().resolvedOptions().timeZone;
}
export function updateDashboard(r){
 lastStatus=r;document.documentElement.dataset.model=r.model;label('modelName','Lumira '+r.model);label('heading','Lumira '+r.model);label('callModel','Lumira '+r.model);
 const synthetic=r.status.mode==='simulation',browser=r.status.mode==='browser-runtime';
 $('dataBadge').hidden=!synthetic;label('dataBadge',t("가상 데이터"));
 $('connectionBanner').dataset.online=String(r.online);
 label('connectionText',synthetic?(r.online?t("가상 기기 연결됨"):t("가상 기기 오프라인")):browser?t("브라우저 연결 · 실물 센서 미연결"):r.online?t("로봇이 연결되어 있어요"):t("로봇 연결 끊김 · 수신 확인 필요"));
 const valid=typeof r.status.battery==='number'&&Number.isFinite(r.status.battery)&&r.status.battery>=0&&r.status.battery<=100&&!!r.received_at;
 label('batteryValue',valid?r.status.battery+'%':'—');label('batteryLabel',valid?(synthetic?t("모의 값"):r.online?t("최근 수신 값"):t("마지막 수신 값")):t("미확인"));
 label('receivedAt',r.received_at?new Date(r.received_at*1000).toLocaleTimeString(locale(),{hour:'2-digit',minute:'2-digit'}):t("수신 이력 없음"));
 label('receivedNote',r.received_at?new Date(r.received_at*1000).toLocaleDateString(locale())+(synthetic?t(" · 가상 상태"):t(" · 로봇 상태")):t("로봇 상태를 기다립니다."));
}
export function updateCommands(rows){
 lastCommands=rows;
 const pending=rows.filter(c=>c.kind==='reminder'&&c.state==='pending').sort((a,b)=>(a.not_before||a.created)-(b.not_before||b.created));
 const c=pending[0],at=c?new Date((c.not_before||c.created)*1000):null;
 label('nextReminder',at?at.toLocaleString(locale(),{month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'}):t("예약 없음"));
 label('reminderNote',c?c.payload.text:t("필요한 시간에 마음을 전하세요."));
 label('todayReminder',c?(at.toLocaleTimeString(locale(),{hour:'2-digit',minute:'2-digit'})+'  '+c.payload.text):t("예약한 알림이 여기에 표시됩니다."));
 $('commandsEmpty').hidden=rows.length>0;
}
export function updateAlerts(rows){$('alertsEmpty').hidden=rows.length>0;const unread=rows.filter(a=>!a.read).length;$('alertCount').hidden=unread===0;label('alertCount',unread>99?'99+':String(unread));}
export function setCallUi(call){
 lastCall=call;
 if(!call||!['ringing','active'].includes(call.state)){
  $('callView').hidden=true;$('app').inert=false;$('appHeader').inert=false;document.body.classList.remove('call-open');$('callView').classList.remove('has-remote');callStarted=0;
  if(returnFocus?.isConnected&&!returnFocus.closest('[hidden]'))returnFocus.focus({preventScroll:true});returnFocus=null;return;
 }
 closeMessage();if($('callView').hidden){returnFocus=document.activeElement;$('callView').hidden=false;$('app').inert=true;$('appHeader').inert=true;document.body.classList.add('call-open');$('closeCall').focus();}
 label('callBadge',lastStatus?.status.mode==='simulation'?t("가상 영상"):call.state==='ringing'?t("현장 수락 대기"):t("녹화하지 않음"));
 $('callPlaceholder').querySelector('p').textContent=call.state==='ringing'?t("현장 사용자의 응답을 기다립니다."):call.video?t("영상·음성을 연결하고 있습니다."):t("음성으로 마음을 전하고 있어요.");
}
export function setMediaUi(stream,peer){
 lastStream=stream;lastPeer=peer;
 if(stream)label('mediaState',stream.getVideoTracks().length?t('카메라·마이크 사용 중'):t('마이크 사용 중 · 카메라 꺼짐'));
 const audio=stream?.getAudioTracks()[0],video=stream?.getVideoTracks()[0];
 for(const [id,track] of [['toggleMic',audio],['toggleCamera',video]]){
  $(id).disabled=!track;$(id).setAttribute('aria-pressed',String(!!track&&!track.enabled));
 }
 $('toggleMic').querySelector('span').textContent=audio?.enabled?t("마이크"):t("음소거");
 $('toggleCamera').querySelector('span').textContent=video?(video.enabled?t("카메라"):t("영상 숨김")):t("카메라 없음");
 $('localVideo').classList.toggle('has-video',!!video&&video.enabled);
 $('toggleSound').disabled=!stream;$('toggleSound').setAttribute('aria-pressed',String($('remoteVideo').muted));
 $('toggleSound').querySelector('span').textContent=$('remoteVideo').muted?t("소리 꺼짐"):t("통화 소리");
 if(peer?.connectionState==='connected'&&!callStarted)callStarted=Date.now();
}
export function remoteReady(){
 $('callView').classList.toggle('has-remote',!!$('remoteVideo').srcObject?.getVideoTracks().length);$('remoteVideo').play().then(()=>{$('playRemote').hidden=true;}).catch(()=>{$('playRemote').hidden=false;});
}
setInterval(()=>{if(callStarted&&!$('callView').hidden){const secs=Math.floor((Date.now()-callStarted)/1000);label('callState',t("통화 중 · ")+String(Math.floor(secs/60)).padStart(2,'0')+':'+String(secs%60).padStart(2,'0'));}},1000);

window.addEventListener('lumira:language',()=>{if(lastStatus)updateDashboard(lastStatus);updateCommands(lastCommands);setCallUi(lastCall);setMediaUi(lastStream,lastPeer);$('phoneTimezone').textContent=t('이 폰 시간 기준 · ')+Intl.DateTimeFormat().resolvedOptions().timeZone;});
