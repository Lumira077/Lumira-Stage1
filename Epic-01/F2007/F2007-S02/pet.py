"""Event driven character simulation. No sensory perception or actual robot output."""
from common import require, ident, number
class Pet:
    def __init__(self,context,clock):
        self.context=context; self.clock=clock; self.epoch=context.epoch
        self.state='idle'; self.seen=set(); self.cooldown=0; self.last=clock()
    def event(self,event_id,kind,stamp,epoch,policy,quiet=False):
        ident(event_id); number(stamp); self.context.check(epoch)
        require(type(quiet) is bool,'INVALID_INPUT')
        require(policy.get('mode')=='pet','NOT_SUPPORTED')
        require(kind in ('touch','call','praise','play','stop'),'INVALID_INPUT')
        if self.epoch!=epoch:
            self.epoch=epoch; self.seen.clear(); self.state='idle'; self.cooldown=0
        now=self.clock()
        if kind=='stop':
            self.context.reset(self.context.subject); self.state='rest'; self.seen.clear()
            return {'state':'rest','cancel_required':True,'executed':False}
        require(0<=now-stamp<=5,'STALE_EVENT')
        require(event_id not in self.seen,'DUPLICATE_EVENT')
        require(len(self.seen)<1000,'SESSION_EVENT_LIMIT')
        self.seen.add(event_id)
        if quiet or now<self.cooldown:
            if quiet: self.state='rest'
            return {'state':self.state,'suppressed':True,'executed':False}
        self.state={'touch':'happy','call':'curious','praise':'happy','play':'play'}[kind]
        self.cooldown=now+2; self.last=now
        return {'state':self.state,'expression_id':self.state,'sound_id':'chirp',
                'gesture_id':'none','epoch':epoch,'executed':False}
    def tick(self):
        if self.clock()-self.last>=30: self.state='rest'
        return self.state
