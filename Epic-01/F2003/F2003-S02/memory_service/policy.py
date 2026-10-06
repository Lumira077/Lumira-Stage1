"""Live authorization bridge. Profile ownership is authoritative, never face/STT labels."""
from memory_contract import Error,require
from profile_contract import Error as ProfileError
class ProfilePolicy:
    def __init__(self,profiles):self.profiles=profiles
    def inspect(self,actor,pid,device=None,active=True):
        try:p=self.profiles.get(pid,actor)
        except ProfileError:raise Error('NOT_FOUND',404)
        stamp={'profile_id':pid,'revision':p['revision'],'long_term_memory':p['data']['consent']['long_term_memory'],'cloud_transfer':p['data']['consent']['cloud_transfer']}
        if active:
            try:d=self.profiles.device(device,actor)
            except ProfileError:raise Error('NOT_FOUND',404)
            require(d['active_profile']==pid,'PROFILE_NOT_ACTIVE',409)
            # Local memory may be read offline; output dispatch is handled separately.
            stamp.update(device_id=device,generation=d['generation'])
        return stamp
