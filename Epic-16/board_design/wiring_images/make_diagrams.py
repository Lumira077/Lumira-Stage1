from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json, zipfile
P=Path(__file__).parent
FONT=str(P/'NotoSansKR.ttf')
C={'signal':'#2563eb','power':'#dc2626','ground':'#475569','safety':'#b45309'}
S=[]
def page(n,title,subtitle,rows,notes,issue):
 im=Image.new('RGB',(2000,1500),'#f5f7fb');d=ImageDraw.Draw(im)
 def txt(x,y,s,size=25,color='#172b4d'):
  f=ImageFont.truetype(FONT,size);f.set_variation_by_axes([450]);d.text((x,y),s,font=f,fill=color)
 def box(x,y,w,h,s):
  d.rounded_rectangle((x,y,x+w,y+h),12,fill='white',outline='#cbd5e1',width=2)
  for i,line in enumerate(s.split('\n')):txt(x+18,y+12+i*30,line,24)
 d.rectangle((0,0,2000,160),fill='#132c46');txt(55,25,f'LUMIRA  /  {n:02d}  {title}',40,'white');txt(57,91,subtitle,24,'#cbd5e1')
 txt(60,180,'출발 보드 · 핀 / 단자',25);txt(810,180,'연결 신호 / 케이블',25);txt(1390,180,'도착 보드 · 핀 / 단자',25)
 for i,(a,b,label,kind) in enumerate(rows):
  y=235+i*91;box(55,y,575,77,a);box(1370,y,575,77,b)
  col=C[kind];d.line((640,y+53,1360,y+53),fill=col,width=4);d.polygon([(1360,y+53),(1347,y+45),(1347,y+61)],fill=col)
  txt(665,y+12,label,23,col)
 y=235+len(rows)*91+15
 d.rounded_rectangle((55,y,1945,1375),12,fill='#e8eef5')
 for i,t in enumerate(notes):txt(75,y+14+i*36,t,24)
 for i,(k,t) in enumerate([('signal','신호 / 데이터'),('power','전력 공급'),('ground','기준 접지'),('safety','안전 / 조건부')]):
  x=60+i*350;d.line((x,1410,x+45,1410),fill=C[k],width=5);txt(x+58,1391,t,22)
 txt(1500,1391,'R1 · 2026-10-06',22)
 txt(60,1445,'논리 결선 초안 | 화살표는 연결 경로 표시(USB/I2C 등은 양방향) | 실제 배선·정격·보호회로 검증 전',20,'#596579')
 name=f'Lumira_Wiring_{n:02d}_R1.png';im.save(P/name);S.append({'file':name,'title':title,'issue':issue,'notes':notes})
page(1,'메인 컴퓨터 · 보드 연결','기준: 보유 Pi 5 8GB + AI HAT+ 13 TOPS / UNO R4 Minima 2장 권장',[
('Pi 5 / PCIe','AI HAT+ 13 TOPS / PCIe','전용 PCIe FFC','signal'),
('Pi 5 / 40핀 헤더','AI HAT+ / 적층 헤더','전용 stacking header','power'),
('Pi 5 / USB3 포트 1','전원형 USB 허브 / upstream','USB 데이터 · 역급전 방지 허브','signal'),
('USB 허브 / H1','UNO-A / USB','주행 명령 · 센서 상태','signal'),
('USB 허브 / H2','UNO-B / USB','관절 명령 · 모터 상태','signal'),
('USB 허브 / H3, H4','가슴 터치 / XVF3800','H3: 터치 / H4: USB 오디오','signal'),
('Pi 전용 DC-DC / USB-C 공급부','Pi 5 / USB-C 전원','5V / 5A급 · 전원 인식 검증','power'),
('보조 5V 전원 / 분기 퓨즈','전원형 허브 / 전원 입력','허브 전류 예산 확인','power'),
('Pi 5 / FAN 커넥터','Pi Active Cooler','전용 팬 케이블','signal')],['• Pi GPIO 3.3V와 UNO 5V UART를 직접 연결하지 않음. USB는 절연 회로가 아님.', '• UNO는 허브 USB로 공급. 외부 5V 핀과 USB VBUS의 무검토 병렬 연결 금지.', '• USB3 포트 2는 선택형 SSD, USB2는 예비/오디오 직결. OS 장치 경로 고정.', '• 본 보드 배치는 개발 권장안. UNO 정확한 모델·수량 확인 필요.'],'KR1-718')
page(2,'2륜 구동 · 인코더','UNO-A ↔ MDD10A 후보 ↔ DC 기어모터 2개',[
('UNO-A / D5 (PWM), D8 (DIR)','MDD10A / PWM1, DIR1','왼쪽 속도 · 방향 (각각 연결)','signal'),
('UNO-A / D6 (PWM), D9 (DIR)','MDD10A / PWM2, DIR2','오른쪽 속도 · 방향 (각각 연결)','signal'),
('왼쪽 인코더 / A, B','UNO-A / D2, D4','A → D2 / B → D4','signal'),
('오른쪽 인코더 / A, B','UNO-A / D3, D7','A → D3 / B → D7','signal'),
('동력 차단 후 WHEEL 레일','MDD10A / 모터 전원 입력','모터 정격 전압 · 분기 퓨즈','power'),
('MDD10A / M1 출력 2선','왼쪽 DC 모터 / 2선','H-bridge 출력: 두 선 모두 구동선','power'),
('MDD10A / M2 출력 2선','오른쪽 DC 모터 / 2선','모터 극성은 저속 지그 시험으로 확인','power'),
('UNO-A / GND','MDD10A 신호 GND · 인코더 GND','저전류 기준 접지','ground')],['• PWM1/2 외부 pull-down 10kΩ은 후보값. 리셋·부팅 시 0 출력 검증.', '• 인코더 VCC/출력 전압 미확정: 정격 전원과 필요 시 레벨 변환 적용. 12V 입력 금지.', '• MDD10A 전류 용량은 실제 모터 stall 전류·냉각 조건 확인 후 확정.', '• 모터 출력선을 GND로 묶지 않음. 고전류 return은 UNO 배선을 통과하지 않음.', '• 충돌·추락·통신 상실은 UNO-A 로컬 정지 + 독립 동력 차단 회로로 처리.'],'KR1-723')
page(3,'추락 · 장애물 센서','TCA9548A 8채널 mux + Pololu VL53L1X carrier #3415 × 8',[
('UNO-A / A4 SDA, A5 SCL','TCA9548A / SDA, SCL','I2C 100kHz 시작 · 0x70','signal'),
('UNO-A / A3','TCA9548A / RESET','정상 HIGH / bus 복구용 LOW','signal'),
('TCA9548A / CH0, CH1','추락 FL, FR / SDA·SCL','앞왼쪽 · 앞오른쪽 (각 채널 2선)','signal'),
('TCA9548A / CH2, CH3','추락 RL, RR / SDA·SCL','뒤왼쪽 · 뒤오른쪽','signal'),
('TCA9548A / CH4, CH5','장애물 F, B / SDA·SCL','전방 · 후방','signal'),
('TCA9548A / CH6, CH7','장애물 L, R / SDA·SCL','좌측 · 우측','signal'),
('보조 5V 레일 / 퓨즈','5V 호환 mux · ToF carrier VIN','센서 전원은 UNO 핀에서 공급하지 않음','power'),
('공통 기준 GND','UNO-A · mux · ToF GND','mux A0/A1/A2도 LOW → 주소 0x70','ground'),
('전면 / 후면 NC 범퍼 접점','UNO-A / A0, A1 (pull-up)','각 접점의 반대쪽은 GND','safety')],['• 각 ToF 주소 0x29 유지, mux는 한 번에 1채널 선택. XSHUT은 보드 pull-up 유지.', '• VL53L1X bare IC에 5V 금지. 위 결선은 전압변환 포함 지정 carrier 기준.', '• 센서 invalid·timeout·오래된 값은 이동 금지. 추락 센서 우선, 비차단 측정.', '• 범퍼 정상 LOW / 충돌·단선 HIGH. I2C 하네스는 하단에 짧게 배치.'],'KR1-733')
page(4,'목 · 어깨 · 손목 관절','UNO-B R4 Minima + TTL 반이중 인터페이스 / DYNAMIXEL -T 모델',[
('Pi / USB 허브 H2','UNO-B / USB Serial','호스트 명령 · 상태 통신','signal'),
('UNO-B / D1 TX (Serial1)','Shield / DXL_TX 입력','UART 송신','signal'),
('Shield / DXL_RX 출력','UNO-B / D0 RX (Serial1)','UART 수신','signal'),
('UNO-B / D2','Shield / DXL_DIR','TTL 반이중 방향 전환','signal'),
('TTL 인터페이스 / DATA','DYNAMIXEL / DATA 버스','Protocol 2.0 / 초기 1Mbps 후보','signal'),
('차단 후 11.1V 안정화 레일','퓨즈 분배판 → 각 관절 V+','목 / 좌팔 / 우팔 / 허리 전력 분기','power'),
('전력 분배판 / 기준 GND','서보 GND · Shield GND · UNO GND','모터 전류는 UNO 경유 금지','ground'),
('서보 ID 1~9 / 고유 주소','목2 · 어깨4 · 손목2 · 허리1','하단 ID 매핑표 참조','signal')],['• ID: 1 목yaw / 2 목pitch / 3 좌어깨lift / 4 좌어깨swing / 5 좌손목', '          6 우어깨lift / 7 우어깨swing / 8 우손목 / 9 허리yaw', '• R4 + Shield 라이브러리 호환은 단일 모터 ping·read/write·timeout 시험 후 확정.', '• -T: GND/V+/DATA 논리망. 물리 핀 순서·VIN 점퍼는 실제 공식 도면으로 확인.', '• 서보 전력을 Shield 얇은 패턴으로 모두 전달하지 않음. 손가락 비구동.'],'KR1-728')
page(5,'배터리 · 충전 · 전원 분배','기능 블록 결선 / 배터리 화학계·셀수·정격·전선 굵기 미확정',[
('배터리 팩 + 적합한 BMS','주퓨즈 · 주스위치 → 전원 분배부','팩 보호 · 역극성/과전류 보호','power'),
('배터리 전용 충전기 / 충전 소켓','적합한 충전·power-path 회로','BMS만으로 충전 기능 완성되지 않음','power'),
('로직 전원 분기','Pi용 DC-DC → USB-C 공급부','5V / 5A급 · 케이블 전압강하 검증','power'),
('보조 전원 분기','5V DC-DC → 허브 · UNO · 센서','각 부하 전류 합산 · 역급전 방지','power'),
('화면·음향 전원 분기','LCD 2개 · 오디오 · 앰프','실제 제품 정격 전압별 공급','power'),
('WHEEL 분기 / 퓨즈 · 차단부','MDD10A / 모터 전원 입력','모터 정격 · stall · 제동 검증','power'),
('JOINT 분기 / 안정화 · 차단부','퓨즈 분배판 → DYNAMIXEL V+','11.1V 후보 · 회생 에너지 처리','power'),
('설계된 전력 return / 기준 접지','DC-DC · driver · logic 기준 GND','분기 return 집결 · 신호선 우회 금지','ground')],['• XC330-T288-T는 최대 12.0V: 3S 완충 12.6V를 직접 인가하지 않음.', '• 11.1V buck-boost 용량·과도응답·회생 clamp/흡수 경로는 상세 설계 필요.', '• 충전기 연결 상태는 별도 접점/절연 입력으로 전달. 충전 전압을 UNO에 직접 입력 금지.', '• 동력 차단과 로직 전원은 분리. 종료 시 Pi 정상 종료 후 로직 전원 차단.', '• 이 그림은 제작용 전원 회로도가 아님: 보호소자·핀·정격 확정 후 회로 검토.'],'KR1-743')
page(6,'카메라 · 화면 · 대화 음향','머리 / 가슴 / 몸통 연결 + 가동부 하네스 조건',[
('Pi / CAM-DISP 0','Camera Module 3 / 15핀','Pi5 22핀 ↔ 15핀 카메라 전용 FFC','signal'),
('Pi / micro-HDMI 0','얼굴 LCD / HDMI 입력','목 가동부 통과 · 굽힘 수명 검증','signal'),
('Pi / micro-HDMI 1','가슴 LCD / HDMI 입력','영상 데이터','signal'),
('USB 허브 / H3','가슴 LCD / USB touch','USB HID 터치 데이터','signal'),
('USB 허브 H4 또는 Pi USB 직결','XVF3800 / USB','마이크 capture + 음성 playback','signal'),
('XVF3800 / 실제 오디오 출력','적합한 앰프·스피커 계통','line-out / 증폭 출력 확인 후 연결','signal'),
('전원 분배판 / 정격별 분기','얼굴 LCD · 가슴 LCD · 외부 앰프','USB touch와 외부 전원 역급전 확인','power'),
('가동 목 · 어깨 하네스','service loop + 양끝 clamp','기구 가동범위 · 케이블 최소 굽힘반경','safety')],['• 재생 음성도 XVF3800 경로로 보내 AEC reference 확보. HDMI 음향 우회 지양.', '• 증폭 출력을 앰프 line 입력에 직접 연결하지 않음. 스피커 임피던스 미확정.', '• CSI FFC 반복 굽힘 불안정 시 UVC 카메라 대안 검증. 임의 케이블 연장 금지.', '• 고전류 모터선과 카메라·마이크선을 분리. 목 무한회전 금지.', '• 카메라 영상은 추락 방지의 유일 입력으로 사용하지 않음.'],'KR1-738')
page(7,'비상정지 · 충전 인터록','독립 하드웨어 차단 + MCU 로컬 감시 / 안전 인증 회로 아님',[
('NC 비상정지 접점','독립 하드웨어 허용 회로','접점 개방 시 동력 허용 해제','safety'),
('충전 연결 검출 / 보호된 신호','독립 주행 허용 회로','충전 연결 → WHEEL 동력 억제','safety'),
('UNO-A / D12 WHEEL_ALIVE','외부 주행 watchdog','정상 제어 주기 펄스 / 고정 HIGH 불가','safety'),
('UNO-B / D5 JOINT_ALIVE','외부 관절 watchdog','정상 통신·제어 주기 펄스','safety'),
('허용 회로 + watchdog + 전압정상','WHEEL / JOINT 별도 동력 차단부','수동 재허용 · 자동 재가동 금지','safety'),
('인터록 보드 / ESTOP_OK','UNO-A D10 / UNO-B D3','정상 HIGH · 외부 pull-down','safety'),
('전원보드 / CHARGE_PRESENT','UNO-A D11 / UNO-B D4','접점/레벨 변환된 신호만 입력','safety'),
('수동 ARM 회로 / LOCAL_ENABLE','UNO-B D6 / 호스트 ARM 절차','리셋·통신 재접속 후 기본 DISARM','safety')],['• 상태 입력만으로 정지하지 않음: 비상정지 접점은 UNO와 독립된 동력 차단 경로에 연결.', '• ESTOP_OK 단선·전원 상실은 LOW. 충전 검출 극성·단선 대응은 회로 확정 시 정의.', '• 차단 시 팔·머리가 중력으로 떨어질 수 있음: 받침·counterbalance·brake 검토.', '• 추락 정지는 UNO-A 로컬 우선. 최악 센서 age와 실제 정지거리로 허용 속도 결정.', '• 하드웨어 watchdog·접점 단락 검출·차단 소자 회로와 정격은 후속 설계·시험.'],'KR1-753')
(P/'manifest.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
with zipfile.ZipFile(P/'Lumira_Wiring_Images_R1.zip','w',zipfile.ZIP_DEFLATED) as z:
 for s in S:z.write(P/s['file'],s['file'])
 z.write(P/'manifest.json','manifest.json')
print(json.dumps(S,ensure_ascii=False))
