import os
os.environ.setdefault('PYOPENGL_PLATFORM','egl')
import struct,json,subprocess,wave,math
from pathlib import Path
import numpy as np
import pyrender,trimesh
from PIL import Image,ImageDraw,ImageFont,ImageOps
from scipy.spatial.transform import Rotation
ROOT=Path(__file__).resolve().parents[1];FPS=24
b=(ROOT/'assets/T02_M2_R3_Motion.glb').read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);raw=b[28+n:]
def acc(i):
 a=g['accessors'][i];v=g['bufferViews'][a['bufferView']];dt={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1',5122:'<i2'}[a['componentType']];k={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']];arr=np.frombuffer(raw,dtype=dt,count=a['count']*k,offset=v.get('byteOffset',0)+a.get('byteOffset',0)).reshape(-1,k)
 if a.get('normalized') and a['componentType']!=5126:arr=arr/np.iinfo(np.dtype(dt)).max
 return arr
scene=pyrender.Scene(bg_color=[.91,.94,.96,1],ambient_light=[.52,.52,.52]);nodes={};meshes=[]
for m in g['meshes']:
 ps=[]
 for p in m['primitives']:
  v=acc(p['attributes']['POSITION']);idx=acc(p['indices']).ravel();norm=trimesh.Trimesh(v,idx.reshape(-1,3),process=False).vertex_normals
  color=acc(p['attributes']['COLOR_0']) if 'COLOR_0'in p['attributes'] else None
  ps.append(pyrender.Primitive(positions=v,normals=norm,indices=idx,color_0=color,material=pyrender.MetallicRoughnessMaterial(baseColorFactor=[1.,1.,1.,1.],metallicFactor=0,roughnessFactor=.8,doubleSided=True)))
 meshes.append(pyrender.Mesh(ps))
def add(i,parent=None):
 x=g['nodes'][i];kw={'name':x.get('name',str(i)),'mesh':meshes[x['mesh']] if 'mesh'in x else None}
 if 'matrix'in x:kw['matrix']=np.array(x['matrix']).reshape(4,4).T
 else:kw.update(translation=x.get('translation',[0,0,0]),rotation=x.get('rotation',[0,0,0,1]),scale=x.get('scale',[1,1,1]))
 nd=pyrender.Node(**kw);scene.add_node(nd,parent);nodes[i]=nd
 for c in x.get('children',[]):add(c,nd)
for i in g['scenes'][g.get('scene',0)]['nodes']:add(i)
def look(eye,target):
 eye=np.array(eye);z=eye-np.array(target);z/=np.linalg.norm(z);x=np.cross([0,1,0],z);x/=np.linalg.norm(x);y=np.cross(z,x);m=np.eye(4);m[:3,:3]=np.array([x,y,z]).T;m[:3,3]=eye;return m
W,H=700,550;camera=pyrender.OrthographicCamera(xmag=.55,ymag=.432,znear=.01,zfar=10);cam_pose=look([.47,.52,1.8],[0,.375,0]);cam=scene.add(camera,pose=cam_pose)
for eye in [[1,2,2],[-1,1,1]]:scene.add(pyrender.DirectionalLight(color=np.ones(3),intensity=1.5),pose=look(eye,[0,.4,0]))
r=pyrender.OffscreenRenderer(W,H);font=ROOT/'assets/NotoSansCJKkr-Regular.otf';F={s:ImageFont.truetype(str(font),s) for s in [16,18,22,24,28,32]}
