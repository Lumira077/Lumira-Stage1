"""Immutable sample SKU policy resolver; operational signer and real entitlements pending."""
from common import require, number
CATALOG={
 'Friend':{'modes':('companion',),'contents':('greeting','talk','music'),'ui':'friend'},
 'Kids':{'modes':('companion','pet'),'contents':('greeting','story','quiz'),'ui':'kids'},
 'Care':{'modes':('companion',),'contents':('greeting','talk','reminiscence'),'ui':'care'},
 'Home':{'modes':('companion','pet'),'contents':('greeting','talk'),'ui':'home'},
 'Pet':{'modes':('pet',),'contents':('play','rest'),'ui':'pet'},
}
def resolve(sku,mode,preferences,capabilities,quiet=False):
    require(sku in CATALOG,'NOT_SUPPORTED')
    p=CATALOG[sku]; require(mode in p['modes'],'NOT_SUPPORTED')
    require(type(quiet) is bool,'INVALID_INPUT')
    require(isinstance(preferences,dict) and isinstance(capabilities,dict),'INVALID_INPUT')
    out={}
    for key,maxdev in [('volume',100),('gesture_level',3),('expression_level',3)]:
        user=number(preferences.get(key,0)); device=number(capabilities.get(key,0))
        require(0<=user<=maxdev and 0<=device<=maxdev,'INVALID_INPUT')
        # Example software ceiling, not a validated physical safety limit.
        out[key]=min(user,device,40 if key=='volume' else 1)
    if quiet: out.update(volume=0,gesture_level=0)
    return {'schema_version':1,'policy_version':'sample-1','sku':sku,'mode':mode,
            'content_ids':list(p['contents']),'ui_id':p['ui'],'limits':out,
            'cloud_allowed':False,'health_actions':False,'approved_for_release':False}
class PolicySelection:
    def __init__(self): self.value=None; self.revision=0
    def apply(self,policy,administrator=False,guardian=False,acks=()):
        require(administrator is True,'NOT_AUTHORIZED')
        require(isinstance(policy,dict) and policy.get('sku') in CATALOG,'INVALID_INPUT')
        if policy['sku']=='Kids': require(guardian is True,'NOT_AUTHORIZED')
        require(set(policy)=={'schema_version','policy_version','sku','mode','content_ids','ui_id','limits','cloud_allowed','health_actions','approved_for_release'},'INVALID_INPUT')
        require(type(policy['schema_version']) is int and policy['schema_version']==1 and policy['policy_version']=='sample-1','NOT_SUPPORTED')
        spec=CATALOG[policy['sku']]
        require(policy['mode'] in spec['modes'] and policy['content_ids']==list(spec['contents']) and policy['ui_id']==spec['ui'],'INVALID_INPUT')
        require(all(policy[k] is False for k in ('approved_for_release','cloud_allowed','health_actions')),'NOT_AUTHORIZED')
        require(isinstance(policy['limits'],dict) and set(policy['limits'])=={'volume','gesture_level','expression_level'},'INVALID_INPUT')
        for k,cap in [('volume',40),('gesture_level',1),('expression_level',1)]:
            require(0<=number(policy['limits'][k])<=cap,'INVALID_INPUT')
        # Simulation only: explicit ACK names represent fake modules, not real receipts.
        require(set(acks)=={'dialogue','ui','voice','motion'},'NOT_READY')
        import copy
        self.value=copy.deepcopy(policy); self.revision+=1
        return self.revision
