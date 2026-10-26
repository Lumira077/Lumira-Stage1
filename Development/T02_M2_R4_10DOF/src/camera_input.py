"""Local prototype face-direction detection. No identity/emotion inference, no image upload."""
import math,time,json,argparse
class FaceDirection:
 def __init__(self,hfov_deg=60,sign=1):
  import cv2
  if not 1<hfov_deg<179 or sign not in [-1,1]:raise ValueError('camera calibration')
  self.cv=cv2;self.hfov=hfov_deg;self.sign=sign;self.last=None;self.stable=0
  self.detector=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
  if self.detector.empty():raise RuntimeError('cascade unavailable')
 def process(self,frame,now_ms):
  gray=self.cv.cvtColor(frame,self.cv.COLOR_BGR2GRAY);boxes=self.detector.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(40,40))
  if len(boxes)!=1:self.last=None;self.stable=0;return None
  x,y,w,h=map(int,boxes[0]);cx=x+w/2;width=frame.shape[1]
  self.stable=self.stable+1 if self.last is not None and abs(cx-self.last)<width*.1 else 1;self.last=cx
  fx=(width/2)/math.tan(math.radians(self.hfov/2));bearing=self.sign*math.degrees(math.atan2(cx-width/2,fx))
  return {'ts_ms':now_ms,'bearing_deg':bearing,'quality_pass':self.stable>=3,'bbox_xywh':[x,y,w,h],'detector':'OpenCV Haar prototype','quality_is_probability':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--camera',type=int,default=0);p.add_argument('--hfov',type=float,default=60);p.add_argument('--yaw-sign',type=int,choices=[-1,1],default=1);p.add_argument('--frames',type=int,default=300);a=p.parse_args();d=FaceDirection(a.hfov,a.yaw_sign);cap=d.cv.VideoCapture(a.camera)
 if not cap.isOpened():raise SystemExit('Camera unavailable; no motor command issued.')
 try:
  for _ in range(a.frames):
   ok,frame=cap.read()
   if not ok:break
   print(json.dumps({'camera':d.process(frame,time.monotonic()*1000)}),flush=True)
 finally:cap.release()
