# KR1-1104 하드웨어 요구·COTS 비교 BOM v0.1

작성일: 2026-10-06 KST | Lumira KR1 Sprint1 | 수행: AI 설계·개발 초안

## 수행 결과
10개 품목군 각각 2개 후보와 인터페이스/선정 방향/보류 사유를 BOM_v0.1.csv에 작성했다. 메인 보드는 사용자 보유 Pi5+13TOPS 기준이며 대안을 구매하라는 뜻이 아니다. 공식 문서에 근거한 비교와 실물 검증 필요사항을 분리했다. 가격/재고 견적은 이번 Sprint 산출물 범위에서 확정하지 않았다.

### 메인 컴퓨터
필수: 보유 8GB·USB/HDMI/CSI·Hailo

후보 A: Pi 5 8GB + AI HAT+13 TOPS / 후보 B: Jetson Orin Nano Super 개발키트

판단: 보유 Pi 기준 개발; Jetson은 CUDA/오프라인 AI 대안

보류: 실측 대화지연·열·소비전력·OS 호환 미확정

공식 자료: https://www.raspberrypi.com/products/raspberry-pi-5/ ; https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/

### 얼굴 LCD
필수: HDMI·얼굴 개구부 적합·독립 전원

후보 A: Waveshare 5inch HDMI LCD (H), 800×480 / 후보 B: Waveshare 5DP-CAPLCD-H, 1024×600

판단: 전자는 단순/저해상도, 후자는 표현 해상도 증가

보류: 얼굴 CAD 개구부/PCB·소비전력 미확인

공식 자료: https://www.waveshare.com/5inch-HDMI-LCD-H.htm ; https://www.waveshare.com/5dp-caplcd.htm

### 가슴 터치
필수: 7인치급·HDMI+USB HID

후보 A: Waveshare 7inch HDMI LCD (H) / 후보 B: 동 제품군 5DP-CAPLCD-H 축소 대안

판단: 7인치 UI 우선; 5인치는 체적 절감 대신 터치 면적 감소

보류: 몸통 개구부·배선/터치OS·역급전 시험

공식 자료: https://www.waveshare.com/7inch-hdmi-lcd-h.htm ; https://www.waveshare.com/5dp-caplcd.htm

### 마이크/오디오
필수: 4mic·USB·AEC 재생 경로

후보 A: Seeed reSpeaker XVF3800 USB 4-Mic / 후보 B: Seeed ReSpeaker Mic Array v2.0 XVF3000

판단: XVF3800 우선, 구형 비교는 지원/공급 재확인

보류: 실물 USB/I2S 버전·AEC·팬/모터 소음

공식 자료: https://wiki.seeedstudio.com/respeaker_xvf3800_introduction/ ; https://wiki.seeedstudio.com/ReSpeaker_Mic_Array_v2.0/

### 카메라
필수: 머리 장착·영상 AI·케이블

후보 A: Camera Module 3 Standard / 후보 B: Raspberry Pi AI Camera IMX500

판단: AF+기존 Hailo 사용 우선; AI Camera는 센서 내 추론 모델 별도

보류: 목 FFC 수명·FOV·노출/모델 검증; Hailo와 중복 가속 비용

공식 자료: https://www.raspberrypi.com/products/camera-module-3/ ; https://www.raspberrypi.com/products/ai-camera/

### 목 구동
필수: TTL·위치/전류 feedback·실하중

후보 A: XM430-W350-T / 후보 B: XM430-W210-T

판단: 감속비/속도/토크 선택은 머리 질량·중심으로 결정

보류: stall 토크를 연속 정격으로 사용 금지

공식 자료: https://emanual.robotis.com/docs/en/dxl/x/xm430-w350/ ; https://emanual.robotis.com/docs/en/dxl/x/xm430-w210/

### 어깨 lift
필수: 팔 질량·모멘트·열·끼임 제한

후보 A: XM540-W270-T / 후보 B: XM540-W150-T

판단: lift는 손목보다 고부하; 감속비 대안 비교

보류: 관절 길이/질량/속도 없으므로 최종 선정 보류

공식 자료: https://emanual.robotis.com/docs/en/dxl/x/xm540-w270/ ; https://emanual.robotis.com/docs/en/dxl/x/xm540-w150/

### 손목
필수: 경량·TTL·허용 전압

후보 A: XC330-T288-T / 후보 B: XC330-T181-T

판단: 손목 전용 경량 후보, T/M 전압 혼동 금지

보류: payload/기구 검증; 3S12.6V 직결 금지

공식 자료: https://emanual.robotis.com/docs/en/dxl/x/xc330-t288/ ; https://emanual.robotis.com/docs/en/dxl/x/xc330-t181/

### 관절 제어
필수: USB host+TTL half duplex

후보 A: UNO R4 Minima + DXL Shield / 후보 B: OpenRB-150

판단: UNO 요청에 따라 R4 우선; OpenRB는 DXL 통합 대안

보류: R4 library/Serial1/DE·단일모터 검증 필요

공식 자료: https://docs.arduino.cc/hardware/uno-r4-minima/ ; https://emanual.robotis.com/docs/en/parts/controller/openrb-150/

### Pi DC-DC
필수: 5V/5A급·USB-C 공급 인터페이스 별도

후보 A: Pololu D24V50F5 / 후보 B: Pololu D36V50F5

판단: 둘 다 DC-DC 후보이며 USB-C PD 완제품 아님

보류: Vin·열 derating·순간전류·케이블/전원 인식 확인 전 보류

공식 자료: https://www.pololu.com/product/2851 ; https://www.pololu.com/product/4091

## R1/R3 호환성 쟁점 및 확인 시험
R1 제품 범위: 소구역 이동은 개발 포함, 공간 자율주행 제외, 탁상 이동 허용은 실물 정지거리 합격 후. R3 제어: 9축 motor ID·soft limit·profile와 UNO 통신 검증. R4 전원/기구: 질량·순간전류·배터리 화학계·11.1V 안정화·회생 대응. R1/R3 확인 완료 서명은 아직 없다.
Pi·HAT·냉각 적층과 두 HDMI·USB·CSI 동시 부하, XVF3800 AEC 출력 경로, R4 Shield 단일축, 8ToF I2C stale 처리, 5mm 플라스틱 관절부 지지 프레임을 검증해야 한다. 전력 합계/전선/퓨즈/배터리 용량은 모델 정격과 duty가 확인된 뒤 확정한다.
이번 문서는 이전 전장 연결서·이미지를 대체하지 않고 후보 근거를 추가한다. 실물 제품 suffix와 PCB revision이 불일치하면 해당 후보 행을 재검토한다.
