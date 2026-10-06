"""Development emotion contracts. No camera, trained model, medical or crisis inference."""
import math
from dataclasses import dataclass
from collections import Counter

LABELS = ('happy', 'sad', 'angry', 'anxious', 'neutral')
class Rejected(ValueError): pass
def number(x, lo, hi):
    if isinstance(x, bool) or not isinstance(x, (float, int)) or not math.isfinite(x) or not lo <= x <= hi:
        raise Rejected('invalid_number')
    return float(x)
def identity(owner, epoch):
    if not isinstance(owner,str) or not 1 <= len(owner) <= 64 or not isinstance(epoch,int) or isinstance(epoch,bool) or epoch < 0:
        raise Rejected('invalid_identity')
def probabilities(p):
    if not isinstance(p,dict) or set(p) != set(LABELS): raise Rejected('label_schema')
    out={k:number(p[k],0,1) for k in LABELS}
    if abs(sum(out.values())-1)>1e-6: raise Rejected('probability_sum')
    return out
@dataclass(frozen=True)
class Observation:
    owner: str
    epoch: int
    modality: str
    timestamp: float
    scores: dict
    quality: float
    model_version: str
    origin: str = 'external_model_fixture'
    schema: str = 'emotion-v1'

class ObservationGate:
    """Reject stale/foreign input; abstain on low confidence/quality, no model inference."""
    def __init__(self, modality):
        if modality not in ('face','audio','text'): raise Rejected('modality')
        self.modality=modality
    def accept(self, owner, epoch, now, packet, consent, quality=1, sample_count=1):
        identity(owner,epoch);now=number(now,0,1e12)
        if consent is not True: return None
        if not isinstance(packet,Observation) or packet.owner!=owner or packet.epoch!=epoch or packet.modality!=self.modality: raise Rejected('scope')
        if packet.schema!='emotion-v1' or not isinstance(packet.model_version,str) or not 1<=len(packet.model_version)<=128: raise Rejected('version')
        age=now-number(packet.timestamp,0,1e12)
        if age<0 or age>2: return None
        if not isinstance(sample_count,int) or isinstance(sample_count,bool) or sample_count != 1: return None
        q=min(number(quality,0,1),number(packet.quality,0,1));p=probabilities(packet.scores)
        ranks=sorted(p.values(),reverse=True)
        if q<.5 or ranks[0]<.6 or ranks[0]-ranks[1]<.15: return None
        return Observation(owner,epoch,self.modality,packet.timestamp,p,q,packet.model_version,packet.origin)

class AudioFeatures:
    """Synthetic normalized PCM RMS/zero crossings. No speech/emotion classifier."""
    def measure(self, samples):
        if not isinstance(samples,(tuple,list)) or not 2<=len(samples)<=160000: raise Rejected('sample_size')
        x=[number(s,-1,1) for s in samples]
        rms=math.sqrt(sum(s*s for s in x)/len(x))
        return {'rms':rms,'zero_crossing_rate':sum((a<0)!=(b<0) for a,b in zip(x,x[1:]))/(len(x)-1),
                'silence':rms<.01,'clipped':any(abs(s)>=.99 for s in x),'emotion_inferred':False}

class SelfReport:
    """Exact explicit self-report fixture, no semantic sentiment/crisis classifier."""
    PHRASES={'나는 기뻐요':'happy','나는 슬퍼요':'sad','나는 화가 나요':'angry','나는 불안해요':'anxious',
             'I feel happy':'happy','I feel sad':'sad','I feel angry':'angry','I feel anxious':'anxious'}
    def observe(self,owner,epoch,now,text,consent):
        identity(owner,epoch);now=number(now,0,1e12)
        if consent is not True: return None
        if not isinstance(text,str) or len(text)>2048: raise Rejected('text_size')
        label=self.PHRASES.get(text.strip())
        if not label:return None
        # Fixed fixture probabilities are NOT empirical or calibrated confidence.
        p={k:.025 for k in LABELS};p[label]=.9
        return Observation(owner,epoch,'text',now,p,1,'exact-self-report-v1','self_report_fixture')

class Fusion:
    def combine(self,owner,epoch,now,observations,consent):
        identity(owner,epoch);now=number(now,0,1e12)
        result={'owner':owner,'epoch':epoch,'timestamp':now,'label':'unknown','scores':{},'evidence':[],
                'state':'inferred_not_confirmed','reason':'insufficient','action':None}
        if consent is not True:result['reason']='no_consent';return result
        if not isinstance(observations,list) or len(observations)>3:raise Rejected('modalities')
        selected=[];seen=set()
        for o in observations:
            if not isinstance(o,Observation):raise Rejected('packet')
            if o.modality in seen:raise Rejected('duplicate_modality')
            seen.add(o.modality)
            accepted=ObservationGate(o.modality).accept(owner,epoch,now,o,True)
            if accepted:selected.append(accepted)
        result['evidence']=[{'modality':o.modality,'version':o.model_version,'quality':o.quality,'origin':o.origin} for o in selected]
        if len(selected)<2:return result
        if max(o.timestamp for o in selected)-min(o.timestamp for o in selected)>.3:
            result['reason']='time_skew';return result
        winners={max(o.scores,key=o.scores.get) for o in selected}
        if len(winners)>1:result['reason']='conflict';return result
        weight=sum(o.quality for o in selected)
        p={k:sum(o.scores[k]*o.quality for o in selected)/weight for k in LABELS}
        result.update(label=max(p,key=p.get),scores=p,reason='candidate')
        return result

class TrendStore:
    """Trusted caller, owner-isolated bounded in-memory development metadata only."""
    def __init__(self,ttl=60,capacity=100):
        self.ttl=number(ttl,1,86400)
        if not isinstance(capacity,int) or isinstance(capacity,bool) or not 1<=capacity<=10000:raise Rejected('capacity')
        self.capacity=capacity;self.epochs={};self.rows={};self.watermarks={}
    def activate(self,owner,epoch,consent):
        identity(owner,epoch)
        if epoch<=self.watermarks.get(owner,-1) and self.epochs.get(owner)!=epoch:raise Rejected('old_epoch')
        if epoch<self.watermarks.get(owner,-1):raise Rejected('old_epoch')
        self.watermarks[owner]=epoch
        if consent is not True:
            self.rows.pop(owner,None);self.epochs.pop(owner,None);return
        if self.epochs.get(owner)!=epoch:self.rows[owner]=[]
        self.epochs[owner]=epoch
    def _scope(self,owner,epoch):
        identity(owner,epoch)
        if self.epochs.get(owner)!=epoch:raise Rejected('not_active')
    def _prune(self,owner,now):
        self.rows[owner]=[r for r in self.rows.get(owner,[]) if 0<=now-r['timestamp']<=self.ttl]
    def append(self,owner,epoch,now,event_id,result):
        self._scope(owner,epoch);now=number(now,0,1e12);self._prune(owner,now)
        if not isinstance(event_id,str) or not 1<=len(event_id)<=128:raise Rejected('event_id')
        if result.get('owner')!=owner or result.get('epoch')!=epoch:raise Rejected('foreign_result')
        timestamp=number(result.get('timestamp'),0,1e12)
        if timestamp>now or now-timestamp>self.ttl:raise Rejected('stale_result')
        if result.get('reason')!='candidate' or result.get('label') not in LABELS:return False
        if result.get('state')!='inferred_not_confirmed' or result.get('action') is not None:raise Rejected('unsafe_state')
        probabilities(result.get('scores'))
        if any(r['id']==event_id for r in self.rows[owner]):return False
        # Explicit projection excludes raw media/text and arbitrary payload fields.
        self.rows[owner].append({'id':event_id,'timestamp':timestamp,'label':result['label']})
        self.rows[owner]=self.rows[owner][-self.capacity:];return True
    def summary(self,owner,epoch,now):
        self._scope(owner,epoch);now=number(now,0,1e12);self._prune(owner,now)
        counts=dict(Counter(r['label'] for r in self.rows[owner]))
        return {'samples':len(self.rows[owner]),'counts':counts,'interpretation':'descriptive_only',
                'sufficient':len(self.rows[owner])>=3,'clinical_risk':None,'automatic_alert':False}
    def delete(self,owner,epoch):
        self._scope(owner,epoch);self.rows.pop(owner,None);self.epochs.pop(owner,None)
