from pathlib import Path
import numpy as np,json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
base=(ROOT/'src/render_base.py').read_text();font=ROOT/'assets/NotoSansCJKkr-Regular.otf';frames=[]
for filename,label in [('R4_13DOF_Source.glb','변경 전 R4 · 13축'),('T02_M2_R4_10DOF_Slim.glb','변경 후 R4 · 10축 / 하체 -7.5%')]:
 s=base.replace("ROOT/'assets/T02_M2_R3_Motion.glb'","Path("+repr(str(ROOT/'models'/filename))+")").replace("ROOT/'assets/NotoSansCJKkr-Regular.otf'","Path("+repr(str(font))+")")
 ns={'__file__':str(ROOT/'src/render.py')};exec(s,ns)
 ns['scene'].set_pose(ns['cam'],ns['look']([0,.52,1.8],[0,.375,0]))
 im,_=ns['r'].render(ns['scene']);canvas=Image.new('RGB',(700,650),'#102536');canvas.paste(Image.fromarray(im),(0,60));d=ImageDraw.Draw(canvas);d.text((16,15),label,font=ImageFont.truetype(str(font),25),fill='white');d.text((16,620),'외형·관절 검토용 / 정밀 간섭·실물 검증 전',font=ImageFont.truetype(str(font),18),fill='white');frames.append(canvas);ns['r'].delete()
out=Image.new('RGB',(1400,650));out.paste(frames[0],(0,0));out.paste(frames[1],(700,0));out.save(ROOT/'docs/R4_10DOF_Comparison.png')
