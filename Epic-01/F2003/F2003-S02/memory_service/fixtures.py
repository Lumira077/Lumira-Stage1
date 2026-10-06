"""Synthetic development setup; never a production identity/device provisioner."""
from pathlib import Path
from profile_service import Service as Profiles
from profile_contract import DEFAULTS,CONSENTS,POLICY
from .policy import ProfilePolicy
from .service import Service

def setup(root,clock=None):
    root=Path(root);profiles=Profiles(str(root/'profiles.sqlite3'))
    d={'language':'ko-KR','nickname':'synthetic','preferred_name':'친구','purpose':'companion','preferences':dict(DEFAULTS),
       'consent':{**{k:k=='long_term_memory' for k in CONSENTS},'policy_version':POLICY}}
    p=profiles.create('demo-owner',d,'create');profiles.provision_device('demo-device','demo-owner');profiles.activate(p['profile_id'],'demo-owner','demo-device',p['revision'])
    memory=Service(str(root/'current.sqlite3'),ProfilePolicy(profiles),**({'clock':clock} if clock else {}))
    return profiles,memory,p['profile_id']
def candidate(content='산책',topic='favorite_activity'):
    return {'kind':'preference','topic':topic,'content':content,'source_ref':'1'*32,'confidence':.8,'ttl_seconds':2592000}
