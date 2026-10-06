"""F2002 v1 strict profile and preference contracts, compatible with F2001."""
import copy,math
VERSION='0.1.0'
POLICY='prototype-2026-10-v1'
PURPOSES=('companion','education','care','home')
CONSENTS=('long_term_memory','conversation_storage','biometric_identity','cloud_transfer')
DEFAULTS={'voice_id':'device_default','speech_rate':1.0,'volume':20,'expression_level':1,'gesture_level':1}
MODULES=('dialogue','recognition','tts','expression','control')
class Error(Exception):
    def __init__(self,code,status=422):self.code,self.status=code,status;super().__init__(code)
def require(ok,code='INVALID_INPUT',status=422):
    if not ok:raise Error(code,status)
def text(x,limit=40):
    require(isinstance(x,str) and 1<=len(x.strip())<=limit and not any(ord(c)<32 for c in x));return x.strip()
def preferences(x):
    require(isinstance(x,dict) and set(x)==set(DEFAULTS))
    require(x['voice_id'] in ('device_default','demo_voice_a'),'UNSUPPORTED_VOICE')
    require(type(x['speech_rate']) in (int,float) and math.isfinite(x['speech_rate']) and .7<=x['speech_rate']<=1.3)
    for k,a,b in [('volume',0,100),('expression_level',0,3),('gesture_level',0,3)]:require(type(x[k]) is int and a<=x[k]<=b)
    return copy.deepcopy(x)
def consent(x):
    require(isinstance(x,dict) and set(x)==set(CONSENTS)|{'policy_version'})
    require(x['policy_version']==POLICY,'POLICY_VERSION_MISMATCH')
    require(all(type(x[k]) is bool for k in CONSENTS));return copy.deepcopy(x)
def validate(x):
    require(isinstance(x,dict) and set(x)=={'language','nickname','preferred_name','purpose','preferences','consent'})
    require(x['language'] in ('ko-KR','en-US'),'UNSUPPORTED_LANGUAGE');require(x['purpose'] in PURPOSES)
    return {**x,'nickname':text(x['nickname']),'preferred_name':text(x['preferred_name']),'preferences':preferences(x['preferences']),'consent':consent(x['consent'])}
def patch(current,changes):
    require(isinstance(changes,dict) and changes and set(changes)<=set(current))
    # Nested values replace the complete nested object, preventing ambiguous merge semantics.
    return validate({**current,**changes})
def from_onboarding(draft):
    require(isinstance(draft,dict) and set(draft)>={'registration','language','profile','purpose','preferences','consent','review'})
    require(draft['registration']['registration_type'] in ('self','guardian'),'GUEST_PROFILE_FORBIDDEN',409)
    return validate({'language':draft['language']['language'],**draft['profile'],'purpose':draft['purpose']['purpose'],
        'preferences':draft['preferences'],'consent':draft['consent']})
def context(profile):
    d=profile['data'];return {'contract_version':'f2002-context-v1','profile_id':profile['profile_id'],'revision':profile['revision'],
        'language':d['language'],'preferred_name':d['preferred_name'],'purpose':d['purpose'],'preferences':copy.deepcopy(d['preferences']),
        'permissions':{k:d['consent'][k] for k in CONSENTS}}
