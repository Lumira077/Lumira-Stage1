"""Manual selection bridge to the existing F2002 service; candidates are not authentication."""
from common import Context, require, ident, number
class FamilySession:
    def __init__(self,profiles,owner,device,clock):
        self.profiles=profiles; self.owner=owner; self.device=device; self.clock=clock
        self.context=Context(); self.application=None; self.expires=0
    def guest(self):
        # F2002 active binding is invalidated, but external queues are not implemented.
        self.profiles.set_device(self.device,self.owner,connected=False)
        self.context.reset(); self.application=None; self.expires=0
        return {'epoch':self.context.epoch,'profile_id':None,'state':'guest'}
    def select(self,pid,confirmed,ttl=300):
        ident(pid); require(confirmed is True,'NOT_AUTHORIZED')
        require(type(ttl) is int and 1<=ttl<=3600,'INVALID_INPUT')
        self.profiles.device(self.device,self.owner)
        self.guest()  # fail closed before attempting new activation
        try:
            p=self.profiles.get(pid,self.owner)
            self.profiles.set_device(self.device,self.owner,connected=True)
            a=self.profiles.activate(pid,self.owner,self.device,p['revision'])
        except Exception:
            self.guest(); raise
        self.application=a['application_id']; self.context.reset(pid)
        self.expires=self.clock()+ttl
        return {'epoch':self.context.epoch,'profile_id':pid,'state':'selected'}
    def read(self,epoch):
        self.context.check(epoch)
        require(self.application is not None,'NOT_AUTHORIZED')
        if self.clock()>=self.expires:
            self.guest(); require(False,'NOT_AUTHORIZED')
        try: return self.profiles.current_context(self.application,self.owner)
        except Exception:
            self.guest(); raise
    def candidate(self,pid,score):
        ident(pid); require(0<=number(score)<=1,'INVALID_INPUT')
        return {'action':'ask_manual_confirmation','authenticated':False}
