# Lumira Stage1 전체 전자보드 구성·연결 설계 초안 R1

작성: 2026-10-06. 보유 확정: Raspberry Pi 5 8GB + AI HAT+ 13 TOPS. UNO 세대·수량, LCD·카메라·배터리 실물 사양은 미확인. 이 문서는 개발 연결안이며 제작 승인 회로도나 실물 검증 결과가 아니다.

## 1. 설계 결정

- Pi: 대화 서비스, 얼굴/가슴 UI, 영상 처리, 제스처 생성, 로그·업데이트.
- AI HAT+: 지원되는 Hailo-8L 영상 모델. 한국어 LLM·AEC 처리는 담당하지 않는다.
- UNO-A: 좌/우 휠 속도 제어, 인코더, 장애물·추락 센서, 주행 인터록.
- UNO-B: 목·어깨·손목·허리 DYNAMIXEL 통신, 동작 제한과 타임아웃.
- 권장 UNO: R4 Minima 2장. R3를 이미 보유했다면 UNO-A로 우선 활용 가능하나 8개 ToF 드라이버의 SRAM·스케줄·인터럽트 부하 검증 필요. UNO-B는 R4 Minima를 기본으로 한다. R3의 USB 통신과 D0/D1 UART는 공유되므로 관절용에 동일 배선을 적용하지 않는다.
- 모터 안전 회로는 별도. MCU 출력만 믿고 동력 전원 허용을 유지하지 않도록 외부 watchdog/인터록 회로를 설계한다. 이 구성 자체를 안전 인증 회로로 간주하지 않는다.
- 기존 9축 초안 유지: 목2, 양어깨 각2, 양손목 각1, 허리1. 팔꿈치 고정은 기존 배치 초안의 가정이고 손가락은 비구동 유연 구조.

## 2. 전체 보드 목록

|ID|보드/부품|수량|배치|역할·상태|
|---|---|---:|---|---|
|P01|Pi 5 8GB|1|몸통 상/중앙|보유 메인|
|P02|AI HAT+ 13 TOPS|1|P01 위|보유, PCIe 연결|
|P03|Pi Active Cooler|1|P01|흡배기·소음 검증|
|C01|UNO-A, R4 Minima 권장|1|하단 센서/휠 근처|R3 조건부 대체|
|C02|UNO-B R4 Minima|1|몸통 관절 분배부|USB와 UART 분리|
|D01|Cytron MDD10A|1|휠 근처|2채널 DC 모터 드라이버 후보. 실제 모터 stall 전류·냉각 조건으로 재선정|
|D02|ROBOTIS DYNAMIXEL Shield 또는 동등 TTL 반이중 회로|1|C02 위/인접|D0/D1/D2. R4 및 라이브러리 조합 단일 서보 벤치 검증 선행|
|D03|퓨즈가 있는 서보 전력 분배판|1|몸통|전체 서보 전류를 UNO/Shield 얇은 패턴으로 전달하지 않음|
|S01|TCA9548A 8채널 I2C mux 모듈|1|C01 근처|동일 주소 ToF 분리, 5V 호환 모듈 선택|
|S02|Pololu VL53L1X carrier #3415|8|하단 외주|추락4 + 수평 장애물4 후보|
|S03|NC 접점 범퍼|전/후 각1|하단|배선 단절도 이상으로 검출|
|S04|좌/우 휠 quadrature encoder|2|휠 모터|전압·펄스수 확인|
|V01|Camera Module 3 Standard|1|머리|CSI 후보, 목 가동 케이블 수명 검증|
|A01|reSpeaker XVF3800 USB 4-Mic Array|1|머리/흉부 음향 위치|USB capture+playback, 기존 음향 후보|
|A02|스피커·필요 시 외부 앰프|1세트|몸통|A01 실제 출력 종류/임피던스 확인 후 선정|
|L01|얼굴 HDMI LCD|1|머리|기존 모델 입력·소비전력 미확인|
|L02|7인치 HDMI + USB HID 터치 LCD|1|가슴|기존 모델 입력·소비전력 미확인|
|H01|자체 전원 USB 허브, 상위 포트 역급전 방지|1|몸통|UNO2·터치·오디오 분배|
|E01|전원 분배·퓨즈·차단·충전 상태 보드|1세트|하단|상세 회로 후속|
|E02|Pi용 5V/5A급 DC-DC + 검증된 USB-C 공급 인터페이스|1|몸통/하단|PD/전압강하/과도부하 검증|
|E03|센서·USB 허브·화면용 5V DC-DC|1 이상|몸통/하단|별도 분기, 부하 합산 후 용량 결정|
|E04|11.1V 서보 buck-boost 전원|1|하단|서보 모델별 전압 범위 및 피크전류 검증|
|E05|배터리+BMS+전용 충전기+power-path|1세트|최하단|화학계/셀수/용량 미확정|

## 3. Pi 포트 배정

|Pi 포트|연결|케이블/조건|
|---|---|---|
|PCIe FFC|AI HAT+|동봉 호환 FFC. NVMe HAT와 직접 동시 사용하지 않음|
|40핀 헤더|AI HAT+ stacking header|전원/기구 적층 포함. 추가 GPIO 배선은 별도 확인|
|CAM/DISP 0|Camera Module 3|Pi5 22핀 ↔ 카메라 15핀 전용 cable. 디스플레이 cable과 혼용 금지|
|CAM/DISP 1|예비|현재 두 화면은 HDMI로 통일|
|micro-HDMI 0|얼굴 LCD HDMI 입력|가동 목 통과, 고굴곡/스트레인 릴리프 검증|
|micro-HDMI 1|가슴 LCD HDMI 입력|터치 데이터는 USB로 별도 연결|
|USB3 1|전원형 USB 허브 upstream|허브 H1 UNO-A / H2 UNO-B / H3 터치 / H4 오디오|
|USB3 2|USB SSD 선택|개발 시작은 microSD. SSD와 전력 예산 검토|
|USB2|예비 또는 오디오 직접 연결|허브 경유 오디오 안정성이 부족하면 전용 포트 사용|
|USB-C 전원|E02|일반 USB 데이터 케이블과 구분. 저전압/전원 인식 로그 검사|
|팬 커넥터|Active Cooler|케이스 통풍 공간 확보|

Pi USB로 두 UNO를 연결하면 Pi GPIO 3.3V와 UNO 5V UART를 직접 연결할 필요가 없다. USB는 galvanic isolation이 아니므로 전력 접지/노이즈 설계는 여전히 필요하다. Pi에 5V UART를 직접 넣지 않는다.

카메라는 초기 권장 CSI 모델이지만 몸통 Pi에서 가동 머리까지 리본 케이블을 반복 구부리는 것은 별도 수명 검증 대상이다. 길이를 임의 연장하거나 급격히 꺾지 않는다. 반복 동작에서 불안정하면 USB UVC 카메라+로봇용 유연 USB 하네스로 전환하고 프레임 전달/색형식과 Hailo 전처리를 다시 검증한다. 카메라 영상은 추락 방지의 유일 입력으로 사용하지 않는다.

## 4. UNO-A 주행·센서 핀 연결

아래는 UNO 번호 표기 기준이며 R4 Minima를 기본으로 한다. D0/D1은 예비. D5/D6 기본 PWM을 사용하고 타이머 주파수를 임의 변경하지 않는다. R3 적용 시 Timer0 시간 함수와 라이브러리 충돌까지 점검한다.

|핀|방향|대상|연결/설명|
|---|---|---|---|
|D2|IN interrupt|왼쪽 encoder A|상승 에지 계수|
|D4|IN|왼쪽 encoder B|D2 ISR에서 방향 판정|
|D3|IN interrupt|오른쪽 encoder A|상승 에지 계수|
|D7|IN|오른쪽 encoder B|D3 ISR에서 방향 판정|
|D5|PWM OUT|MDD10A PWM1|외부 pull-down 후보 10kΩ, reset 시 0 보장 검증|
|D8|OUT|MDD10A DIR1|왼쪽 방향|
|D6|PWM OUT|MDD10A PWM2|외부 pull-down 후보 10kΩ|
|D9|OUT|MDD10A DIR2|오른쪽 방향|
|D10|IN|ESTOP_OK 피드백|인터록 보드의 5V 호환 절연/접점 출력|
|D11|IN|CHARGE_PRESENT|충전 소켓/전원보드 접점. 충전 전압 직접 입력 금지|
|D12|OUT|WHEEL_ALIVE|외부 watchdog으로 주기 pulse. 고정 HIGH는 허용 신호 아님|
|D13|OUT|진단 LED|구동 허용에 사용하지 않음|
|A0|IN digital|전면 범퍼 NC|pull-up, 정상 접점 닫힘 LOW, 충돌/단선 HIGH|
|A1|IN digital|후면 범퍼 NC|동일|
|A2|IN analog|배터리 전압|보호된 분압 출력. 원전압 직접 연결 금지|
|A3|OUT|TCA9548A RESET|정상 HIGH, bus stuck 시 reset. 부품 모듈 논리전압 확인|
|A4/SDA|I2C|mux SDA|A4와 별도 SDA 표기는 같은 bus|
|A5/SCL|I2C|mux SCL|100kHz로 시작, 파형 확인 후 변경|
|USB|양방향|Pi|C01 식별 고정, 통신 속도 115200 수준부터 검증|

Encoder는 x1 계수부터 시작한다. pulses/revolution이 출력축/모터축 기준인지 구분하여 기어비를 적용한다. 최대 에지율 = 계수/rev × 최대 rpm / 60. ISR에는 카운터 증가와 B 읽기만 수행한다. 3.3V push-pull, 5V open-collector 등 실제 출력 형식에 맞게 Schmitt buffer/pull-up을 선정한다. 12V encoder 출력 직접 연결 금지.

MDD10A의 PWM/DIR는 제어 입력이며 모터 공급이 아니다. D01 M1 출력 두 선은 왼쪽 모터, M2는 오른쪽 모터, 전원단은 차단된 휠 전원 레일로 연결한다. 제어 GND는 저전류 기준 접지로 연결하고 모터 전류가 UNO GND 배선을 거쳐 흐르지 않게 한다. 정상 제동/관성과 전원 차단 시의 자유 회전은 실측한다.

## 5. ToF 8개 연결 및 배치

|mux 채널|센서|설치 위치|용도|
|---|---|---|---|
|CH0|CLIFF_FL|바닥 앞-왼쪽|전진/회전 추락|
|CH1|CLIFF_FR|바닥 앞-오른쪽|전진/회전 추락|
|CH2|CLIFF_RL|바닥 뒤-왼쪽|후진/회전 추락|
|CH3|CLIFF_RR|바닥 뒤-오른쪽|후진/회전 추락|
|CH4|OBS_F|전방 수평|전방 장애물|
|CH5|OBS_B|후방 수평|후방 장애물|
|CH6|OBS_L|좌측 수평|회전 측면 장애물|
|CH7|OBS_R|우측 수평|회전 측면 장애물|

연결: UNO SDA/SCL → mux SDA/SCL; mux 채널 SDn/SCn → 해당 센서 SDA/SCL. 5V 호환 Pololu carrier의 VIN은 센서 5V 레일, GND는 센서 GND로 연결한다. VL53L1X bare IC는 5V 부품이 아니다. 보드명이 같아도 전압변환 없는 저가 모듈에 이 배선을 적용하지 않는다.

mux A0/A1/A2=LOW로 7-bit 주소 0x70. 각 ToF는 기본 0x29 유지, 한 번에 한 mux 채널만 선택한다. XSHUT은 채널 분리로 주소 변경이 필요 없어 보드 pull-up 상태로 둔다. 해당 pin은 5V tolerant가 아니므로 UNO HIGH를 직접 연결하지 않는다. pull-up 저항은 모듈 내장값 합성 후 결정하고 무조건 각 위치에 추가하지 않는다.

8개 센서를 blocking delay로 순차 측정하면 주행 정지가 늦어진다. 연속 측정/비동기 ready polling으로 구현하고, 추락 4개 우선 처리. 센서별 값·유효 상태·timestamp를 관리한다. timeout, out-of-range, 통신 실패, 오래된 데이터는 안전하다는 뜻이 아니라 이동 금지 조건이다. 검은 바닥, 반사/유리, 햇빛, 센서간 광간섭, 바닥 높이 변화에 대해 실측한다.

초기 목표: 각 추락 센서 20Hz 이상 유효 갱신, age 제한 100ms 이하를 시험 목표로 설정. 달성 보장값이 아니며 측정 budget/간섭 조건에 따라 조정한다. 속도 허용 조건은 d_detect > v×T_total + v²/(2a_brake) + margin. T_total에는 센서 최악 age·통신·제어·드라이버 지연을 포함한다. 센서 배치 지점과 바퀴 접촉점 사이 거리 및 모든 회전 방향을 확인해야 한다. 검증 전 책상 가장자리 자유 이동 금지, 고정 지그/낙하 방지 줄을 사용한 시험만 수행.

I2C는 몸통 전체 장거리 네트워크로 쓰지 않는다. UNO-A와 mux를 하단에 모으고 각 분기를 짧게 배치한다. 수십 cm 이상의 길이는 용량·파형·모터 잡음을 측정하고 필요 시 I2C buffer 또는 지역 MCU/차동 통신으로 변경한다.

## 6. UNO-B 관절 연결

|핀|대상|설명|
|---|---|---|
|USB|Pi/HUB H2|호스트 명령/상태, R4 USB Serial|
|D0 RX|Shield DXL_RX|Serial1 RX|
|D1 TX|Shield DXL_TX|Serial1 TX|
|D2 OUT|Shield DXL_DIR|반이중 TX/RX 전환|
|D3 IN|ESTOP_OK|안전 보드 피드백|
|D4 IN|CHARGE_PRESENT|충전 중 gesture 정책 입력|
|D5 OUT|JOINT_ALIVE|외부 watchdog pulse|
|D6 IN|LOCAL_ENABLE|수동 재허용 버튼/회로 피드백|
|A0 IN|관절 전원 monitor|보호된 분압 출력|
|나머지|예비|리미트·온도 확장, Shield 점유와 확인|

DYNAMIXEL은 RC PWM 서보가 아니다. PCA9685 및 UNO Servo 라이브러리를 기본 구동부로 쓰지 않는다. TTL -T 모델 기준 3핀 GND/V+/DATA이며 RS-485 -R은 다른 4핀 인터페이스다. 커넥터 방향/번호는 실제 모터와 케이블 공식 도면으로 확인하며 색만으로 결선하지 않는다.

R4의 USB Serial과 Serial1을 구분해 설정한다. 기존 AVR UNO용 예제의 Serial 정의를 그대로 사용하지 않는다. Shield 공식 문서에 R4 검증이 명시되지 않은 조합이므로 Dynamixel2Arduino 빌드·방향 전환·ping·read/write·timeout을 1개 모터에서 확인한 후 확대한다. 실패 시 UNO-B용 검증된 TTL 반이중 인터페이스/라이브러리 이식 또는 기존 OpenRB-150 관절 전용 보드로 대체한다. U2D2를 Pi에 직접 연결하는 방법은 별도 대안이며 이 기본안에는 중복 설치하지 않는다.

|ID 제안|축|이전 모터 후보|비고|
|---:|---|---|---|
|1|목 yaw|XM430-W350-T|원점·회전 제한 실측|
|2|목 pitch|XM430-W350-T|머리 질량/중심 검증|
|3|왼쪽 어깨 lift|XM540-W270-T|중량·링크 하중 계산 후 확정|
|4|왼쪽 어깨 swing|XM430-W350-T|동일|
|5|왼쪽 손목|XC330-T288-T|T와 M 모델 전압 혼동 금지|
|6|오른쪽 어깨 lift|XM540-W270-T|좌우 원점/방향 별도|
|7|오른쪽 어깨 swing|XM430-W350-T|동일|
|8|오른쪽 손목|XC330-T288-T|동일|
|9|허리 yaw|XM540-W270-T|현재 9축 초안 유지|

버스는 Protocol 2.0, 초기 1Mbps 후보. 각 모터를 하나씩 연결해 고유 ID와 baud를 설정한다. baud·제어모드·레지스터/펌웨어 차이를 확인한다. 위치는 기구별 각도→encoder 값 변환, soft limit·전류/속도/가속 제한 후 전송한다. Goal Position과 profile을 묶어 동기 전송하고 응답 누락·전압·온도·전류·hardware error를 감시한다. 50Hz 명령/10~20Hz 피드백은 초기 목표이며 9축 패킷 길이·반환 지연 실측 후 결정한다.

전원은 목/좌팔/우팔/허리로 퓨즈 분기하여 전력 분배판에서 주입한다. TTL 데이터는 짧은 간선과 검증된 짧은 분기를 사용한다. 긴 star 분배와 전체 전류의 서보 한 개 커넥터 경유를 피한다. 전원 주입 지점에서 V+ 레일을 중복 연결해 역류하지 않도록 분배 회로를 작성한다. Shield VIN 연결 jumper는 외부 전원 사용 조건에 맞춰 분리하며 11.1V가 UNO 5V/USB로 넘어가지 않게 확인한다.

## 7. 전원·충전 구성

배터리 → 주퓨즈/주스위치 → power-path/분배판에서 로직·화면·오디오·휠·관절 레일을 분리한다. BMS만으로 충전/power-path 기능이 완성되는 것은 아니다.

|레일|부하|설계 조건|
|---|---|---|
|LOGIC_PI|Pi+HAT+쿨러|5V/5A급 공급, USB-C 전원 식별/케이블/과도부하 시험|
|LOGIC_AUX|허브·UNO2·센서8|별도 5V 공급, 허브 역급전 방지 및 USB 전류 예산|
|DISPLAY/AUDIO|LCD2·오디오·앰프|실제 LCD/앰프 정격으로 분기·퓨즈 선정|
|WHEEL|MDD10A·DC 모터2|모터 정격에 맞는 전압. stall 합계/제동·회생 조건으로 설계|
|JOINT|DYNAMIXEL9|정전압 11.1V 후보, 피크·연속 전류 및 회생 에너지 처리 검증|

중요: XC330-T288-T 공식 입력은 6.5~12.0V, 권장 11.1V. 3S 리튬이온 배터리가 최대 12.6V라면 직접 연결하면 안 된다. 11.1V buck-boost 또는 동등 안정화·과전압 보호가 필요하다. 모터 회생 시 일반 DC-DC가 전류를 흡수하지 못할 수 있으므로 clamp/덤프/양방향 경로 등을 전원 설계에서 검토한다. 3S를 확정한 것은 아니며 실제 배터리 화학계·셀수와 BMS가 우선이다.

개발 초기에는 배터리 대신 전류 제한 벤치 전원을 분기별 사용하고 공통 기준 접지를 검증한다. UNO는 검증된 전원형 USB 허브에서 공급하며 외부 5V pin과 USB VBUS를 무검토 병렬 연결하지 않는다. 센서8·모터·화면 전류를 UNO 5V pin에서 공급하지 않는다.

ESTOP_OK 피드백은 외부 pull-down을 두고 정상일 때만 HIGH가 되도록 구성한다. 단선·전원 상실은 LOW로 인식한다. 이는 상태 표시이며 비상정지의 실제 동력 차단은 UNO 소프트웨어와 독립된 회로가 수행한다. 접점 단락까지 검출하는 이중화 회로는 별도 상세 설계 대상이다.

차단 회로: NC 비상정지 접점 + charge 상태 + 전압 정상 + 외부 watchdog + 수동 ARM 조건을 하드웨어 허용 회로로 결합한다. WHEEL과 JOINT 동력 차단을 분리한다. 충전 연결은 휠 동력을 하드웨어로 억제하고 사용자 앞 관절 동작은 초기 정책상 정지. 비상정지는 동력을 차단하지만 팔/머리가 중력으로 떨어질 수 있으므로 기계식 받침·counterbalance·brake 필요성을 검토한다. 동력 차단이 기계적 정지거리 0을 뜻하지 않는다.

## 8. 음향·화면·하네스

- USB 오디오 출력도 가능한 한 XVF3800 경로로 보내 AEC가 재생 reference를 받을 수 있게 한다. HDMI/다른 USB 오디오로 우회하면 reference 경로를 재설계해야 한다.
- XVF3800의 실제 connector가 line-out인지 amplified speaker out인지 확인 후 스피커/앰프를 연결한다. 증폭 출력을 일반 앰프 line 입력에 연결하지 않는다. 스피커 임피던스·허용 출력·커넥터 모델은 미확정 항목.
- 마이크 구멍을 외장/패션 액세서리로 가리지 않고 팬·스피커·모터 구조 전달 진동과 분리한다. 외부 앰프를 쓰면 AEC·최대 볼륨 clipping을 재검증한다.
- 얼굴 HDMI video + 별도 정격 전원. 가슴 HDMI video + USB touch + 정격 전원. 터치 USB와 LCD 외부 전원 사이 역급전 여부 확인. 화면 전원은 GPIO가 아니라 전원 분배판에서 공급.
- 목 하네스는 카메라 cable·얼굴 HDMI·오디오 USB·필요한 전원·서보 bus를 실제 통과 구조에 맞춰 분리한다. mic FPC는 헤드 내부 고정, 가동부는 USB 등 적합한 cable 사용.
- 목 pitch/yaw·어깨 회전축 밖에 service loop와 양끝 clamp. 무한회전 금지. 굽힘 반경은 cable 공급사 규격으로 결정하고 임의 수치를 최종치로 사용하지 않음.
- 고전류 휠/서보 전원과 카메라·마이크·센서 배선을 분리. 전원 return과 signal reference를 설계된 스타 접지 지점에 연결. 배터리·모터 전류가 USB shield/센서 GND를 return으로 쓰지 않게 한다.

## 9. 통신 규약·실행 순서

Pi↔UNO-A/B는 독립 USB device path로 고정한다. 포트 열기/업데이트/reset 후 자동 동작하지 않는다. /dev/ttyACM 번호만 하드코딩하지 않고 serial number 또는 USB 물리 경로를 사용한다.

|메시지|내용|초기 주기|
|---|---|---|
|HELLO/CAPS|보드 ID·FW·protocol·boot ID|연결 시|
|HEARTBEAT|session·seq|50ms 목표|
|ARM/DISARM|명시적 동작 허용·해제|필요 시, 자동 복구 금지|
|WHEEL_CMD|좌우 속도 mm/s·가속도 제한·유효기간|20~50Hz|
|JOINT_CMD|축 ID·목표 각도·속도/가속 제한·유효기간|최대50Hz 목표|
|STATUS|센서별 age/valid·encoder·fault·전압|10~20Hz|
|FAULT|코드·timestamp·원인|발생 즉시, latch|

전송 frame 초안: magic/version/type/length/sequence/payload/CRC16. 고정 최대 길이와 timeout을 두고 버퍼 넘침·중복·과거 session·잘못된 CRC·범위 초과 명령을 거절한다. MCU 수신 시각 기준 deadline 사용. 200ms heartbeat 상실 정지는 초기 목표이며 책상 추락 대응 기준이 아니다. 추락/장애물 정지는 UNO-A가 Pi 명령과 독립적으로 즉시 우선 처리하고 정지거리 시험으로 더 엄격한 기한을 정한다.

Pi 프로세스: audio, cloud dialogue, vision/Hailo, UI, motion planner, MCU bridge, logger. Linux 프로세스가 PWM을 직접 시간 제어하지 않는다. UNO-A는 비차단 sensor state machine+wheel controller, UNO-B는 trajectory limits+DXL bus state machine. 외부 watchdog은 관련 제어 cycle/센서 유효 검사까지 통과한 경우에만 갱신한다.

시작: 로직 전원 → MCU DISARM → Pi/HAT/USB 확인 → 센서 valid/전원/서보 ID 확인 → 사람의 ARM → 저속 동작. 종료: DISARM/주행 정지 → 관절 안전 자세(가능할 때) → Pi 파일 동기화/종료 → 전원 차단. 강제 정지에서는 파일 보호보다 구동 안전 우선.

## 10. 시험·완료 조건

1. 무부하 결선: 역극성·short·전압·USB 역급전·reset 기본 출력 검사.
2. 단일 wheel: 공중 지그에서 방향·encoder·PWM zero·단절·watchdog 확인.
3. 센서: 8개 주소/채널·max age·유효성, 각 센서 unplug 및 I2C stuck 주입. 어느 방향도 stale 값으로 이동 허용하지 않음.
4. 단일 DXL: R4+Shield FW 호환, ID·limit·전류·bus timeout 확인. 이후 9축 확대.
5. 음향/UI: 동시 대화·두 화면·영상·USB SSD 부하, fan/motor noise 및 AEC double-talk 측정.
6. 동력/열: peak current·전압강하·온도·throttling·회생·충전 삽입 검사.
7. 통합: Pi kill·USB disconnect·MCU hang·비상정지·센서 failure에 대한 정지거리와 수동 복구 시험.
8. 책상: 고정 지그·낙하 방지 장치 하에서 바닥 재질/가장자리/회전 방향별 시험. 합격 전 자유 이동 허용하지 않음.

## 11. 확정에 필요한 실물 정보

필수 입력은 UNO 정확한 모델·수량/사진, DC 모터 정격전압·stall current·encoder 사양, DYNAMIXEL의 정확한 -T/-R 및 XC330-T/M 구분, LCD 두 개 제품명/전원/connector, 배터리 셀수·최대전압·BMS, XVF3800/스피커 실물 형식이다. 이 정보가 확인되면 전원 용량·퓨즈·전선 굵기·connector pin 번호·정확한 shield jumper 설정을 최종 회로도로 고정할 수 있다.

## 12. 공식 자료

- Pi AI HAT: https://www.raspberrypi.com/documentation/accessories/ai-hat-plus.html
- Pi 5: https://www.raspberrypi.com/products/raspberry-pi-5/
- UNO R3: https://docs.arduino.cc/hardware/uno-rev3/
- UNO R3/R4 차이: https://support.arduino.cc/hc/en-us/articles/9350551575964-What-s-the-difference-between-UNO-R3-and-UNO-R4-boards
- UNO R4 Minima USB/UART: https://docs.arduino.cc/tutorials/uno-r4-minima/cheat-sheet/
- DYNAMIXEL Shield: https://emanual.robotis.com/docs/en/parts/interface/dynamixel_shield/
- XC330-T288: https://emanual.robotis.com/docs/en/dxl/x/xc330-t288/
- MDD10A/UNO: https://www.cytron.io/tutorial/using-mdd10a-arduino-uno
- VL53L1X carrier: https://www.pololu.com/product/3415
- TCA9548A: https://www.ti.com/product/TCA9548A
- Camera 3: https://www.raspberrypi.com/products/camera-module-3/
- Pi camera cable: https://www.raspberrypi.com/products/camera-cable/
- XVF3800: https://wiki.seeedstudio.com/respeaker_xvf3800_introduction/

제조사 사실과 본 설계의 핀 할당·ID·주기·아키텍처 제안을 구분한다. 본 문서의 수치 목표와 제안 회로는 실물 검증 전이다.
