from pathlib import Path
import json,struct,numpy as np
from scipy.spatial.transform import Rotation
ROOT=Path(__file__).resolve().parents[1]
def measure(path):
 b=path.read_bytes();assert struct.unpack_from('<I',b,8)[0]==len(b);n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);raw=b[28+n:];points={};world={}
 def walk(i,par):
  x=g['nodes'][i]
  if 'matrix'in x:t=np.array(x['matrix']).reshape(4,4).T
  else:
   t=np.eye(4);t[:3,:3]=Rotation.from_quat(x.get('rotation',[0,0,0,1])).as_matrix()@np.diag(x.get('scale',[1,1,1]));t[:3,3]=x.get('translation',[0,0,0])
  world[i]=par@t;name=x.get('name','')
  if 'mesh'in x:
   for p in g['meshes'][x['mesh']]['primitives']:
    a=g['accessors'][p['attributes']['POSITION']];v=g['bufferViews'][a['bufferView']];ar=np.frombuffer(raw,'<f4',a['count']*3,v.get('byteOffset',0)+a.get('byteOffset',0)).reshape(-1,3);w=(world[i]@np.c_[ar,np.ones(len(ar))].T).T[:,:3];points.setdefault(name,[]).append(w)
  for c in x.get('children',[]):walk(c,world[i])
 for i in g['scenes'][g.get('scene',0)]['nodes']:walk(i,np.eye(4))
 def width(prefix):
  ar=np.vstack([p for n,ps in points.items() if n.startswith(prefix) for p in ps]);return float(np.ptp(ar[:,0])*1000)
 ids={x.get('name'):i for i,x in enumerate(g['nodes'])}
 return g,{'lower_shell_max_width_mm':width(('B01_','B02_')),'chest_width_mm':width('C01_'),'right_wheel_width_mm':width(('D01_R_','D02_R_')),'wheel_pivot_spacing_mm':float(abs(world[ids['R_wheel']][0,3]-world[ids['L_wheel']][0,3])*1000)}
a,old=measure(ROOT/'models/R4_13DOF_Source.glb');g,new=measure(ROOT/'models/T02_M2_R4_10DOF_Slim.glb');assert abs(new['lower_shell_max_width_mm']/old['lower_shell_max_width_mm']-.925)<1e-5;assert abs(new['right_wheel_width_mm']-old['right_wheel_width_mm'])<1e-5
config=json.loads((ROOT/'config/model.json').read_text());assert len(config['joints'])==10
for anim in g['animations']:
 assert len(anim['channels'])==10
 assert {g['nodes'][c['target']['node']]['name'] for c in anim['channels']}==set(config['joints'])
tr=json.loads((ROOT/'results/preview_trajectories.json').read_text())
for t in tr.values():
 q=np.array(t['q_deg']);assert q.shape[1]==10 and np.isfinite(q).all() and abs(q[[0,-1]]).max()<1e-9
assert np.max(np.abs(np.array(tr['03_hand_held_head_only']['q_deg'])[:,2:]))==0
out={'passed':True,'before':old,'after':new,'motor_count_without_wheels':10,'preview_clips':3,'hand_held_preview_arm_motion':False,'collision_validation':False,'hardware_validation':False,'RL_retrained':False}
(ROOT/'results/model_validation.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
