"""NFC ID registry simulation. UID is not authentication; no package loading or sensor IO."""
from common import require, ident, number
REGISTRY={'outfit-blue':{'theme':'blue','models':('Friend','Home','Pet')},
          'outfit-sun':{'theme':'sun','models':('Kids','Care','Home')}}
MODULES={'face','voice','motion','dialogue'}
class Theme:
    def __init__(self,context,clock):
        self.context=context; self.clock=clock; self.value='default'; self.revision=0
        self.sequence=-1; self.expiry=0; self.epoch=context.epoch; self.pending=None
    def fallback(self):
        self.value='default'; self.pending=None; self.revision+=1; self.expiry=0
        return self.value
    def prepare(self,outfit,sequence,epoch,sku,allowed=True,presence_ttl=3):
        self.context.check(epoch); ident(outfit)
        require(type(sequence) is int and sequence>=0,'INVALID_INPUT')
        require(type(allowed) is bool,'INVALID_INPUT')
        ttl=number(presence_ttl); require(0<ttl<=10,'INVALID_INPUT')
        if self.epoch!=epoch:
            self.fallback(); self.sequence=-1; self.epoch=epoch
        require(sequence>self.sequence,'STALE_EVENT'); self.sequence=sequence
        self.fallback()  # keep default while new modules prepare
        require(outfit in REGISTRY and sku in REGISTRY[outfit]['models'],'NOT_SUPPORTED')
        require(allowed,'NOT_AUTHORIZED')
        self.pending={'theme':REGISTRY[outfit]['theme'],'sequence':sequence,'epoch':epoch}
        self.expiry=self.clock()+ttl
        return dict(self.pending)
    def commit(self,token,acks):
        try:
            require(self.pending is not None and token==self.pending,'STALE_CONTEXT')
            self.context.check(token['epoch']); require(self.clock()<self.expiry,'STALE_EVENT')
            require(isinstance(acks,dict) and set(acks)==MODULES,'NOT_READY')
            require(all(v==token and isinstance(v,dict) for v in acks.values()),'NOT_READY')
        except Exception:
            self.fallback(); raise
        self.value=self.pending['theme']; self.pending=None; self.revision+=1
        return {'theme':self.value,'revision':self.revision,'simulated':True}
    def tick(self,sensor_healthy=True):
        require(type(sensor_healthy) is bool,'INVALID_INPUT')
        if not sensor_healthy or self.context.stopped or self.context.epoch!=self.epoch or self.clock()>=self.expiry:
            self.fallback()
        return self.value
    def remove(self): return self.fallback()
