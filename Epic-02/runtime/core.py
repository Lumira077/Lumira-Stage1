"""Epic-02 development prototype. No actual Cloud, LLM, STT, TTS or robot IO."""
import copy,math,threading,unicodedata

class Rejected(ValueError): pass
def need(ok,reason='INVALID_INPUT'):
    if not ok: raise Rejected(reason)
def num(x,lo=0,hi=float('inf')):
    need(type(x) in (int,float) and math.isfinite(x) and lo<=x<=hi);return x
def integer(x,lo=0,hi=1_000_000):
    need(type(x) is int and lo<=x<=hi);return x
def ident(x):
    need(isinstance(x,str) and 0<len(x)<=80 and x.isascii() and all(c.isalnum() or c in '-_' for c in x));return x
def flag(x): need(type(x) is bool);return x
def text(x,limit=2000):
    need(isinstance(x,str) and 0<len(x)<=limit)
    need(not any(unicodedata.category(c).startswith('C') and c not in '\n\t' for c in x));return x

class PolicyEngine:  # F2205: classification and authority must come from trusted caller
    def decide(self,x):
        required={'sensitivity','safety_command','cloud_consent','visual_needed','network_ok','credits','robot_ready'}
        need(isinstance(x,dict) and set(x)==required)
        need(x['sensitivity'] in ('public','personal','sensitive','unknown'))
        for k in required-{'sensitivity','credits'}:flag(x[k])
        integer(x['credits'])
        if x['safety_command']:route,reason='local','SAFETY_LOCAL'
        elif x['sensitivity'] in ('sensitive','unknown'):route,reason='local','PRIVATE_LOCAL'
        elif not x['cloud_consent']:route,reason='local','NO_CLOUD_CONSENT'
        elif not x['robot_ready']:route,reason='deny','ROBOT_NOT_READY'
        elif not x['network_ok']:route,reason='local','NETWORK_DEGRADED'
        elif x['credits']==0:route,reason='local','NO_CREDIT'
        elif x['visual_needed']:route,reason='hybrid','VISUAL_ALLOWED'
        else:route,reason='cloud','CLOUD_ALLOWED'
        return {'route':route,'reason':reason,'policy_version':'prototype-1'}

class Gateway:  # F2206: deliberately uses fake adapters only
    def __init__(self,adapters):
        need(isinstance(adapters,dict) and 0<len(adapters)<=4)
        for k in adapters:need(k in ('openai_sample','gemini_sample','local_sample'),'PROVIDER_NOT_APPROVED')
        self.adapters=dict(adapters)
    def complete(self,provider,request_id,max_output=256):
        ident(request_id);integer(max_output,1,2000)
        need(provider in self.adapters,'PROVIDER_NOT_APPROVED')
        try:r=self.adapters[provider](request_id,max_output)
        except Exception:raise Rejected('PROVIDER_FAILED') from None
        need(isinstance(r,dict) and set(r)=={'text','usage_tokens'},'INVALID_PROVIDER_RESPONSE')
        text(r['text']);integer(r['usage_tokens'],0,max_output)
        return {'text':r['text'],'usage_tokens':r['usage_tokens'],'provider':provider,'simulated':True}

class RealtimeGate:  # F2207: metadata admission, not transport
    def __init__(self,epoch,cloud_consent,video_consent,visual_needed):
        integer(epoch);self.epoch=epoch;self.cloud=flag(cloud_consent)
        self.video=flag(video_consent);self.visual=flag(visual_needed);self.seq={};self.closed=False
    def accept(self,modality,seq,epoch):
        integer(seq);integer(epoch);need(not self.closed and epoch==self.epoch,'STALE_SESSION')
        need(modality in ('text','audio','video'));need(self.cloud,'NO_CONSENT')
        if modality=='video':need(self.video and self.visual,'VIDEO_NOT_ALLOWED')
        need(seq>self.seq.get(modality,-1),'STALE_EVENT');need(seq<=10000,'SESSION_LIMIT')
        self.seq[modality]=seq;return {'accepted':True,'transmitted':False}
    def close(self):self.closed=True;self.seq.clear()

class LocalContext:  # F2208: synthetic fixtures only; not a persistent F2003 store
    def __init__(self,items,clock):
        need(isinstance(items,list) and len(items)<=1000)
        for x in items:
            need(isinstance(x,dict) and set(x)=={'owner','id','text','confirmed','expires','cloud_share'})
            ident(x['owner']);ident(x['id']);text(x['text']);flag(x['confirmed']);flag(x['cloud_share']);num(x['expires'])
        self.items=copy.deepcopy(items);self.clock=clock
    def search(self,actor,query,cloud=False,limit=3):
        ident(actor);text(query,100);flag(cloud);integer(limit,1,5)
        words=set(query.casefold().split());out=[]
        for x in self.items:
            if x['owner']!=actor or x['confirmed'] is not True or x['expires']<=self.clock():continue
            if cloud and x['cloud_share'] is not True:continue
            score=len(words & set(x['text'].casefold().split()))
            if score:out.append((score,x['id'],x['text']))
        out.sort(key=lambda x:(-x[0],x[1]))
        return [{'id':i,'text':t} for _,i,t in out[:limit]]

class Budget:  # F2209: integer units, process-local ledger
    def __init__(self,available):
        self.available=integer(available);self.reservations={};self.lock=threading.RLock()
    def reserve(self,key,units):
        ident(key);integer(units,1)
        with self.lock:
            if key in self.reservations:
                r=self.reservations[key];need(r['max']==units,'IDEMPOTENCY_CONFLICT');return dict(r)
            need(self.available>=units,'NO_CREDIT');self.available-=units
            self.reservations[key]={'max':units,'actual':None,'state':'reserved'};return dict(self.reservations[key])
    def settle(self,key,actual):
        ident(key);integer(actual)
        with self.lock:
            need(key in self.reservations,'NOT_FOUND');r=self.reservations[key]
            if r['state']=='settled':need(actual==r['actual'],'IDEMPOTENCY_CONFLICT');return dict(r)
            need(r['state']=='reserved','INVALID_STATE');need(actual<=r['max'],'OVER_RESERVED')
            self.available+=r['max']-actual;r.update(actual=actual,state='settled');return dict(r)
    def cancel(self,key):
        ident(key)
        with self.lock:
            need(key in self.reservations,'NOT_FOUND');r=self.reservations[key]
            if r['state']=='cancelled':return dict(r)
            need(r['state']=='reserved','INVALID_STATE');self.available+=r['max'];r['state']='cancelled';return dict(r)

class NetworkMonitor:  # F2210: thresholds are examples, not measured product limits
    def __init__(self,clock):self.clock=clock;self.route='local';self.recovery=0;self.last_stamp=-1
    def observe(self,rtt,loss,bandwidth,stamp):
        num(rtt);num(loss,0,1);num(bandwidth);num(stamp)
        age=self.clock()-stamp;need(age>=0,'INVALID_TIMESTAMP')
        need(stamp>self.last_stamp,'STALE_MEASUREMENT');self.last_stamp=stamp
        poor=age>5 or rtt>350 or loss>.1 or bandwidth<128
        if poor:self.route='local';self.recovery=0
        elif rtt<200 and loss<.03 and bandwidth>=256:
            self.recovery+=1
            if self.recovery>=3:self.route='cloud'
        else:self.recovery=0
        return {'route':self.route,'sample_age':age,'thresholds':'prototype'}

class PrivacyGuard:  # F2211: this is enforcement, not semantic PII classification
    def check(self,classification,consent,safety,provider):
        need(classification in ('public','personal','sensitive','unknown'));flag(consent);flag(safety)
        allowed=consent and not safety and classification in ('public','personal') and provider in ('openai_sample','gemini_sample')
        return {'allow_cloud':allowed,'local_only':not allowed,'reason':'ALLOWED' if allowed else 'PRIVACY_OR_SAFETY_LOCAL'}

class Recovery:  # F2212: no streaming or retry timers; one final result per turn
    def __init__(self):self.finalized=set()
    def complete(self,turn,adapters,emitted=False):
        ident(turn);flag(emitted);need(turn not in self.finalized,'DUPLICATE_TURN')
        need(not emitted,'PARTIAL_OUTPUT_REQUIRES_CANCEL')
        need(isinstance(adapters,list) and 0<len(adapters)<=3)
        attempted=0
        for adapter in adapters:
            attempted+=1
            try:r=adapter();text(r)
            except Exception:continue
            self.finalized.add(turn);return {'text':r,'attempts':attempted,'simulated':True}
        self.finalized.add(turn)
        return {'text':'연결이 원활하지 않습니다. 기본 안내를 도와드릴게요.','attempts':attempted,'backend':'local_template'}

class QualityTelemetry:  # F2213: allowlisted numeric metadata, never transcripts
    def __init__(self):self.rows=[]
    def record(self,row):
        need(isinstance(row,dict) and set(row)=={'provider','status','latency_ms','usage_tokens','cost_units'})
        need(row['provider'] in ('openai_sample','gemini_sample','local_sample'))
        need(row['status'] in ('ok','error','cancelled'))
        num(row['latency_ms'],0,600000);integer(row['usage_tokens']);integer(row['cost_units'])
        need(len(self.rows)<10000,'EVENT_LIMIT');self.rows.append(dict(row))
    def snapshot(self):
        latency=sorted(r['latency_ms'] for r in self.rows);n=len(latency)
        return {'operations':n,'success_rate':None if not n else sum(r['status']=='ok' for r in self.rows)/n,
                'p50_ms':None if not n else latency[math.ceil(n*.5)-1],
                'p95_ms':None if not n else latency[math.ceil(n*.95)-1],
                'cost_units':sum(r['cost_units'] for r in self.rows),'scope':'simulated_operations'}

class WakeGate:  # F2008: consumes model scores, does not recognize audio
    def __init__(self,clock):self.clock=clock;self.until=0;self.seen=set()
    def trigger(self,event,score,stamp,mute=False,echo=False):
        ident(event);num(score,0,1);num(stamp);flag(mute);flag(echo)
        need(0<=self.clock()-stamp<=2,'STALE_EVENT');need(event not in self.seen,'DUPLICATE_EVENT')
        need(len(self.seen)<1000,'SESSION_LIMIT');self.seen.add(event)
        accepted=not mute and not echo and score>=.8 and self.clock()>=self.until
        if accepted:self.until=self.clock()+2
        return {'start_session':accepted,'detector_connected':False}

class TranscriptAssembler:  # F2009: consumes transcription events, no speech model
    def __init__(self,epoch):integer(epoch);self.epoch=epoch;self.seq=-1;self.value='';self.final=False
    def update(self,sequence,value,final,epoch):
        integer(sequence);integer(epoch);text(value);flag(final)
        need(epoch==self.epoch,'STALE_SESSION');need(not self.final,'ALREADY_FINAL');need(sequence>self.seq,'STALE_EVENT')
        self.seq=sequence;self.value=value;self.final=final
        return {'text':value,'ready_for_dialogue':final,'stt_connected':False}

class ConversationSession:  # F2011: transient history only
    def __init__(self,clock):self.clock=clock;self.actor=None;self.epoch=0;self.expires=0;self.history=[];self.turns=set()
    def open(self,actor,ttl=300):
        ident(actor);integer(ttl,1,3600);self.epoch+=1;self.actor=actor;self.expires=self.clock()+ttl
        self.history.clear();self.turns.clear();return self.epoch
    def check(self,actor,epoch):
        ident(actor);integer(epoch)
        if self.clock()>=self.expires:self.cancel();raise Rejected('SESSION_EXPIRED')
        need(self.actor==actor and self.epoch==epoch,'STALE_SESSION')
    def append(self,actor,epoch,turn,value):
        self.check(actor,epoch);ident(turn);text(value);need(turn not in self.turns,'DUPLICATE_TURN')
        need(len(self.turns)<1000,'SESSION_LIMIT');self.turns.add(turn);self.history.append(value);self.history=self.history[-8:]
    def cancel(self):
        self.epoch+=1;self.actor=None;self.history.clear();self.turns.clear();self.expires=0

class InterruptController:  # F2012: tracks fake ACKs; does not stop physical outputs
    MODULES={'generation','tts','motion'}
    def __init__(self,session):self.session=session;self.pending=set();self.cancel_epoch=None
    def cancel(self):
        self.session.cancel();self.cancel_epoch=self.session.epoch;self.pending=set(self.MODULES)
        return {'epoch':self.cancel_epoch,'modules':sorted(self.pending),'actual_cancelled':False}
    def ack(self,module,epoch):
        integer(epoch);need(module in self.MODULES and epoch==self.cancel_epoch,'INVALID_ACK')
        self.pending.discard(module);return not self.pending
    def accept_output(self,epoch):
        integer(epoch);need(not self.pending and epoch==self.session.epoch and self.session.actor is not None,'OUTPUT_BLOCKED')
        self.session.check(self.session.actor,epoch);return True

class LanguageResolver:  # F2013: capability intersection only
    def choose(self,requested,stt,llm,tts):
        need(requested in ('ko-KR','en-US'),'LANGUAGE_NOT_SUPPORTED')
        for supported in (stt,llm,tts):
            need(isinstance(supported,(list,tuple)) and requested in supported,'LANGUAGE_CAPABILITY_MISMATCH')
        return requested

class SafetyPolicy:  # F2014: risk tags must come from an independent trusted classifier
    def review(self,age,risk):
        need(age in ('child','adult','elder','unknown'))
        need(risk in ('clear','medical','crisis','harm','private','unknown'))
        if risk in ('harm','private'):action,reply='deny','그 요청은 도와드릴 수 없습니다.'
        elif risk=='crisis':action,reply='local_guidance','지금 주변의 믿을 수 있는 사람에게 도움을 요청해 주세요. 저는 연락을 대신 실행하지 않았습니다.'
        elif risk=='medical':action,reply='local_guidance','정확한 판단은 의료 전문가와 상의해 주세요.'
        elif risk=='unknown' or age=='unknown':action,reply='local_guidance','기본 안내부터 도와드릴게요.'
        else:action,reply='allow',None
        return {'action':action,'safe_reply':reply,'policy_version':'prototype-1','semantic_classifier_connected':False}

class LocalCommands:  # F2121: exact phrase allowlist, proposals are never execution claims
    TABLE={'정지':'stop','멈춰':'stop','stop':'stop','상태 확인':'status','status':'status',
           '개인정보 삭제':'privacy_delete','delete my data':'privacy_delete','도와줘':'help','help':'help','안녕':'greet','hello':'greet'}
    def parse(self,value):
        text(value,100);value=unicodedata.normalize('NFKC',value).strip().casefold()
        intent=self.TABLE.get(value,'unsupported')
        return {'intent':intent,'proposal_only':True,'executed':False,'cloud_required':False}

class LocalModelGate:  # F2122: manifest admission only, no model or NPU inference
    def validate(self,manifest,free_mb,temperature):
        num(free_mb);num(temperature,-40,150)
        need(isinstance(manifest,dict) and set(manifest)=={'runtime','model_hash','ram_required_mb','hardware'})
        need(manifest['runtime'] in ('llama.cpp','rknn-approved-adapter'),'RUNTIME_NOT_SUPPORTED')
        need(isinstance(manifest['model_hash'],str) and len(manifest['model_hash'])==64 and all(c in '0123456789abcdef' for c in manifest['model_hash']))
        integer(manifest['ram_required_mb'],1,100000);need(manifest['hardware'] in ('cpu-lab','rk3588-lab','jetson-lab'))
        need(free_mb>=manifest['ram_required_mb']*1.2,'INSUFFICIENT_RAM');need(temperature<70,'THERMAL_LIMIT')
        return {'configuration_admitted':True,'inference_executed':False,'npu_verified':False}
    def propose(self,action):
        need(action in ('status','stop'),'TOOL_NOT_APPROVED');return {'action':action,'executed':False}

class HybridRouter:  # F2123: combines process-local snapshots, not live distributed state
    def route(self,x,provider='openai_sample'):
        PolicyEngine().decide(x)  # strict validation before privacy enforcement
        guarded=PrivacyGuard().check(x['sensitivity'],x['cloud_consent'],x['safety_command'],provider)
        decision=PolicyEngine().decide(x)
        if not guarded['allow_cloud'] and decision['route'] in ('cloud','hybrid'):
            decision.update(route='local',reason='PROVIDER_NOT_APPROVED')
        return {**decision,'privacy':guarded,'executed':False}

class Dialogue:  # F2010: integrated routing + tagged safety + fake Gateway + session fence
    def __init__(self,session,gateway):self.session=session;self.gateway=gateway
    def answer(self,actor,epoch,turn,x,age='unknown',risk='unknown',provider='openai_sample'):
        self.session.check(actor,epoch);ident(turn);need(turn not in self.session.turns,'DUPLICATE_TURN')
        route=HybridRouter().route(x,provider);safety=SafetyPolicy().review(age,risk)
        if safety['action']!='allow':reply=safety['safe_reply'];backend='local_safety_template'
        elif route['route'] in ('cloud','hybrid'):
            result=self.gateway.complete(provider,turn);reply=result['text'];backend=provider
        else:reply='연결 없이 기본 안내를 도와드릴게요.';backend='local_template'
        # Recheck after adapter returned; a switch during generation must block output.
        self.session.check(actor,epoch);self.session.append(actor,epoch,turn,reply)
        return {'text':reply,'backend':backend,'epoch':epoch,'route':route,'tts_executed':False,'simulated':True}

class AudioLab:  # F2126: simple reference calculations, NOT adaptive AEC or TDOA estimation
    def pcm(self,samples):
        need(isinstance(samples,list) and 0<len(samples)<=48000)
        return [num(x,-1,1) for x in samples]
    def beam(self,channels):
        need(isinstance(channels,list) and 1<=len(channels)<=8)
        validated=[self.pcm(c) for c in channels];need(len({len(c) for c in validated})==1,'FRAME_LENGTH_MISMATCH')
        return [sum(v)/len(validated) for v in zip(*validated)]
    def subtract_reference(self,mic,reference,gain=.5):
        mic=self.pcm(mic);reference=self.pcm(reference);num(gain,0,1);need(len(mic)==len(reference),'FRAME_LENGTH_MISMATCH')
        return [max(-1,min(1,m-gain*r)) for m,r in zip(mic,reference)]
    def doa(self,delay_samples,sample_rate,spacing_m):
        num(delay_samples,-1000,1000);integer(sample_rate,8000,48000);num(spacing_m,.01,.5)
        ratio=343*delay_samples/sample_rate/spacing_m;need(abs(ratio)<=1,'IMPOSSIBLE_DELAY')
        return math.degrees(math.asin(ratio))
