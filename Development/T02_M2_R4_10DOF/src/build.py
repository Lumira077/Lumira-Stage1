from pathlib import Path
import json,struct,numpy as np
from scipy.spatial.transform import Rotation as R
ROOT=Path(__file__).resolve().parents[1]
b=(ROOT/'models/R4_13DOF_Source.glb').read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);raw=bytearray(b[28+n:]);g['animations']=[]
ids={x.get('name'):i for i,x in enumerate(g['nodes'])}
for old,new in [('neck_pitch','HEAD_FIXED_FRAME'),('R_UPPERARM_TWIST','R_UPPERARM_FIXED_FRAME'),('L_UPPERARM_TWIST','L_UPPERARM_FIXED_FRAME')]:
 x=g['nodes'][ids[old]];x['name']=new;x['rotation']=[0,0,0,1];x['extras']={'motor':False,'reason':'R3-equivalent 10DOF; rigid connection'}
base=ids['base'];factor=.925
# Outer lower shells, base plate, bumper and wheel covers. Real wheels and ports are not scaled.
selected=[i for i in g['nodes'][base]['children'] if g['nodes'][i].get('name','').startswith(('B01_','B02_','B05_','B40_','D08_'))]
wi=len(g['nodes']);g['nodes'].append({'name':'LOWER_BODY_WIDTH_92P5PCT','scale':[factor,1,1],'children':selected});g['nodes'][base]['children']=[i for i in g['nodes'][base]['children'] if i not in selected]+[wi]
for name in ['R_wheel','L_wheel']:
 g['nodes'][ids[name]]['translation'][0]*=factor
# Reposition shell-mounted ports/fasteners without shrinking the parts.
for i in g['nodes'][base]['children']:
 nd=g['nodes'][i]
 if not nd.get('name','').startswith(('B20_','B21_','B23_','B24_','B41_','U41_')) or 'mesh'not in nd:continue
 mat=np.array(nd.get('matrix',np.eye(4).T.flatten())).reshape(4,4).T;pts=[]
 for prim in g['meshes'][nd['mesh']]['primitives']:
  ac=g['accessors'][prim['attributes']['POSITION']];bv=g['bufferViews'][ac['bufferView']];ar=np.frombuffer(raw,'<f4',ac['count']*3,bv.get('byteOffset',0)+ac.get('byteOffset',0)).reshape(-1,3);pts.append((mat@np.c_[ar,np.ones(len(ar))].T).T[:,:3])
 ar=np.vstack(pts);cx=(ar[:,0].min()+ar[:,0].max())/2;mat[0,3]+=(factor-1)*cx;nd['matrix']=mat.T.flatten().tolist()
# Preserve head, torso, wheel diameter/width and caster positions.
joints=['waist','neck','R_J1','R_J2','R_J3','R_J4_WRIST','L_J1','L_J2','L_J3','L_J4_WRIST'];axes=[1,1,0,2,0,0,0,2,0,0]
poses={'01_friendly_greet':[4,18,-45,15,-50,10,-25,-10,-35,8],'02_bilateral_response':[-4,-18,-48,24,-50,12,-48,-24,-50,12],'03_hand_held_head_only':[0,20,0,0,0,0,0,0,0,0]}
def add(arr,kind):
 while len(raw)%4:raw.append(0)
 arr=np.asarray(arr,'<f4');vi=len(g['bufferViews']);g['bufferViews'].append({'buffer':0,'byteOffset':len(raw),'byteLength':arr.nbytes});raw.extend(arr.tobytes());a={'bufferView':vi,'componentType':5126,'count':len(arr),'type':kind}
 if kind=='SCALAR':a.update(min=[float(arr.min())],max=[float(arr.max())])
 ai=len(g['accessors']);g['accessors'].append(a);return ai
T=np.linspace(0,5,151);pulse=np.sin(np.pi*T/5)**2;tr={}
for name,pose in poses.items():
 q=pulse[:,None]*np.array(pose)[None,:];a={'name':'PREVIEW_NOT_RL_'+name,'samplers':[],'channels':[]};ti=add(T,'SCALAR')
 for k,(j,axis) in enumerate(zip(joints,axes)):
  rv=np.zeros((len(T),3));rv[:,axis]=np.deg2rad(q[:,k]);oi=add(R.from_rotvec(rv).as_quat(),'VEC4');a['samplers'].append({'input':ti,'output':oi,'interpolation':'LINEAR'});a['channels'].append({'sampler':k,'target':{'node':ids[j],'path':'rotation'}})
 g['animations'].append(a);tr[name]={'time_s':T.tolist(),'q_deg':q.tolist()}
g['extras']={'version':'R4-10DOF-0.1','upper_body_motor_count':10,'wheel_drive_motors_excluded':2,'lower_shell_width_factor':factor,'wheel_geometry_scaled':False,'wheel_lateral_positions_factor':factor,'neck_pitch_motor':False,'upper_arm_twist_motors':False,'status':'kinematic and interaction software prototype; no hardware fit or RL approval'}
g['buffers'][0]['byteLength']=len(raw);j=json.dumps(g,separators=(',',':')).encode();j+=b' '*((-len(j))%4);raw+=b'\0'*((-len(raw))%4);out=struct.pack('<III',0x46546c67,2,28+len(j)+len(raw))+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(raw),0x004e4942)+raw;(ROOT/'models/T02_M2_R4_10DOF_Slim.glb').write_bytes(out)
(ROOT/'config/model.json').write_text(json.dumps(g['extras']|{'joints':joints,'axes_xyz':axes},ensure_ascii=False,indent=2));(ROOT/'results/preview_trajectories.json').write_text(json.dumps(tr))
print('10 DOF / lower shell -7.5% / 3 non-RL preview clips')
