"""Development-only contracts. No network authentication or robot command dispatch."""
import math
class Rejected(ValueError): pass
def require(ok, code):
    if not ok: raise Rejected(code)
def ident(value):
    require(isinstance(value,str) and 0<len(value)<=80 and value.isascii()
            and all(c.isalnum() or c in '-_' for c in value),'INVALID_INPUT')
    return value
def number(value):
    require(type(value) in (int,float) and math.isfinite(value),'INVALID_INPUT')
    return value
class Context:
    def __init__(self):
        self.epoch=0; self.subject=None; self.stopped=False
    def reset(self,subject=None):
        self.epoch+=1; self.subject=subject
        return self.epoch
    def check(self,epoch):
        require(type(epoch) is int and epoch==self.epoch,'STALE_CONTEXT')
        require(not self.stopped,'NOT_READY')
    def stop(self):
        self.stopped=True; self.reset()
    def resume(self):
        self.stopped=False; self.reset()
