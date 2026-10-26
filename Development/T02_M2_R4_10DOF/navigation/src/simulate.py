from pathlib import Path
import json,math,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from navigation import Grid,Navigator,sensors,RES,RADIUS
ROOT=Path(__file__).resolve().parents[1];FONT=ROOT.parent/'assets/NotoSansCJKkr-Regular.otf'
def map_for(kind):
 a=np.zeros((80,100),bool);a[:2]=a[-2:]=True;a[:,:2]=a[:,-2:]=True
 rects=[(3,3,4.8,4.3),(7,1,9,2.4),(5.6,.2,5.8,2.5),(5.6,5,5.8,7.8)] if kind=='home' else [(2,2,3.5,3),(5,2,6.5,3),(2,5,3.5,6),(5,5,6.5,6),(8,3.6,9.2,5.5)]
 for x0,y0,x1,y1 in rects:a[int(y0/RES):int(y1/RES),int(x0/RES):int(x1/RES)]=True
 return a
cases=[]
for kind in ['home','office']:
 grid=Grid(map_for(kind))
 for mode in ['solo','follow']:
  start=(1,1,0);goal=(8.5,6.8);nav=Navigator(grid,start);human=np.array([2.2,1.0]);human_path=grid.path(human,goal);hi=0
  if mode=='solo':nav.start_solo(goal)
  else:nav.start_follow('selected_person_1')
  rows=[];arrived=False
  for k in range(1200):
   t=k*.1;s=sensors()
   if mode=='follow':
    while hi<len(human_path) and np.linalg.norm(np.array(human_path[hi])-human)<.08:hi+=1
    if hi<len(human_path):
     vec=np.array(human_path[hi])-human;human+=vec/max(np.linalg.norm(vec),1e-9)*min(.014,np.linalg.norm(vec))
    s['target']={'id':'selected_person_1','age_s':.01,'quality_pass':True,'xy':human.tolist()}
    if 18<=t<24:s['target']=None
    if 24<=t<24.2:s['resume_follow']=True
   result=nav.step(s);assert grid.valid(nav.pose[:2]);assert abs(result['v_m_s'])<=.200001 and abs(result['w_rad_s'])<=.600001
   if result['state']=='ARRIVED':arrived=True
   rows.append({'time_s':t,**result,'person_xy':human.tolist() if mode=='follow' else None})
  cases.append({'id':kind+'_'+mode,'environment':kind,'mode':mode,'start':list(start),'goal':list(goal),'arrived':arrived,'rows':rows})
(ROOT/'results/scenarios.json').write_text(json.dumps(cases));summary=[]
for c in cases:
 states={x['state'] for x in c['rows']};r={'case':c['id'],'arrived':c['arrived'],'final_state':c['rows'][-1]['state'],'states':sorted(states),'collision_free_in_inflated_grid':True,'motor_output_enabled':False}
 if c['mode']=='solo':assert c['arrived'],r
 else:
  assert 'TARGET_LOST_WAIT'in states and 'FOLLOW_MOVING'in states
  r['final_follow_distance_m']=float(np.linalg.norm(np.array(c['rows'][-1]['person_xy'])-np.array(c['rows'][-1]['pose'][:2])))
 summary.append(r)
(ROOT/'results/summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2),flush=True)
# Four-panel 2D engineering simulation, 4x simulated time.
proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x900','-r','10','-i','-','-an','-c:v','libx264','-threads','2','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(ROOT/'videos/R4_10DOF_Navigation_Simulation.mp4')],stdin=subprocess.PIPE)
f=ImageFont.truetype(str(FONT),20);small=ImageFont.truetype(str(FONT),16)
for k in range(0,1200,4):
 im=Image.new('RGB',(1280,900),'#102536');d=ImageDraw.Draw(im);d.text((20,8),'R4 10DOF · 가정/사무실 자율주행 · 2D 시뮬레이션 (실물 주행 아님, 4배속)',font=f,fill='white')
 for ix,c in enumerate(cases):
  ox=(ix%2)*640+25;oy=(ix//2)*420+80;scale=48
  def point(p):return (ox+p[0]*scale,oy+(8-p[1])*scale)
  a=map_for(c['environment']);img=Image.fromarray(np.where(a[:,:,None],np.array([59,76,90],np.uint8),np.array([230,238,241],np.uint8)).astype('uint8'));img=img.transpose(Image.Transpose.FLIP_TOP_BOTTOM).resize((480,384),Image.Resampling.NEAREST);im.paste(img,(ox,oy));d=ImageDraw.Draw(im)
  title=('가정' if c['environment']=='home' else '사무실')+(' · 혼자 목적지 이동' if c['mode']=='solo' else ' · 선택 사용자 따라가기');d.text((ox,oy-35),title,font=f,fill='white')
  pts=[point(x['pose'][:2]) for x in c['rows'][:k+1:4]]
  if len(pts)>1:d.line(pts,fill='#3aa6cc',width=2)
  row=c['rows'][k];x,y=point(row['pose'][:2]);rr=RADIUS*scale;d.ellipse((x-rr,y-rr,x+rr,y+rr),fill='#187eb5',outline='white',width=2);theta=row['pose'][2];d.line((x,y,x+rr*math.cos(theta),y-rr*math.sin(theta)),fill='white',width=2)
  if c['mode']=='follow':
   px,py=point(row['person_xy']);d.ellipse((px-8,py-8,px+8,py+8),fill='#26a36b')
  gx,gy=point(c['goal']);d.rectangle((gx-5,gy-5,gx+5,gy+5),outline='#b63860',width=2)
  d.text((ox+490,oy+15),f'{row["time_s"]:.1f}s',font=small,fill='white');state=row['state'].replace('_','\n');d.multiline_text((ox+490,oy+55),state,font=small,fill='#f4cd72',spacing=6)
 proc.stdin.write(im.tobytes())
 if k==240:im.save(ROOT/'results/navigation_preview.png')
proc.stdin.close();assert proc.wait()==0
