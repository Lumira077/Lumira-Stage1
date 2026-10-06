"""One-time authorized snapshot import from an F2001 Service instance."""
from profile_contract import require,from_onboarding

def import_onboarding(target,source,sid,actor,authorized_subjects=()):
    session=source.get(sid,actor)
    require(session['status']=='committed' and session['profile_id'] is not None,'COMMITTED_PROFILE_REQUIRED',409)
    source_id='F2001:'+session['profile_id']
    old=target.db.execute('SELECT owner,profile FROM imports WHERE source=?',(source_id,)).fetchone()
    if old:
        require(old[0]==actor,'NOT_FOUND',404);require(old[1] is not None,'SOURCE_IMPORT_DELETED',409);return target.get(old[1],actor)
    draft=session['draft'];data=from_onboarding(draft)
    p=target.create(actor,data,'import:'+session['profile_id'],subject=draft['registration']['subject_id'],authorized_subjects=authorized_subjects)
    with target.tx():target.db.execute('INSERT INTO imports VALUES(?,?,?)',(source_id,actor,p['profile_id']))
    return p
