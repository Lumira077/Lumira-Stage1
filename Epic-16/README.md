# EPIC-16 로봇 하드웨어 시스템 구축

https://lumira077.atlassian.net/browse/KR1-711

24 Features, 96 existing Sub-tasks.

COTS70/Custom30 구상: 전원/안전 → STM32 Motion/I/O → DVT 이후 RK3588 SoM carrier 순서. Fusion masterCAD·중립 STEP/PDF/DXF·BOM revision, Stage1 UVC1080p HDR·4채널 USB mic·DYNAMIXEL, RGB-D 옵션 및 HW benchmark 후 단일 플랫폼 gate. 명세 수치/후보는 구매승인·물리성능 검증이 아니다.

현재 명세/검토 도구·일부 로컬 utility입니다. 실제 HW·production서비스·Pilot·법률/재무 승인·외부 실행은 미완료입니다.

- [[F2090] Stage1 HW 요구사양 및 시스템 Architecture](F2090/README.md): Stage1 HW block/전원domain/AI와Safety MCU·인터페이스 baseline을 확정
- [[F2091] Main Computing HW 선정 및 인터페이스 설계](F2091/README.md): RK3588 기준 후보와 Jetson 비교·CPU/GPU/NPU·열/전력 benchmark 및 interface를 설계
- [[F2092] Safety MCU·Motor Interface·I/O 제어 Architecture](F2092/README.md): Linux AI와 Safety MCU의 CAN-FD/RS485·enable/watchdog·I/O 책임을 분리
- [[F2093] 목·팔·허리·손 구동 HW 및 Actuator 선정](F2093/README.md): DYNAMIXEL 후보의 torque/speed/current/heat/size와 BLDC 전환 gate를 검증
- [[F2094] Camera·Mic·IMU·Touch·근접 Sensor HW 구성](F2094/README.md): UVC/RGB-D·mic/IMU/touch/proximity의 위치/전원/USB/시각을 설계
- [[F2095] 얼굴 Display·Touch LCD·Audio HW 구축](F2095/README.md): Face/Touch display·Class-D/speaker chamber·AEC reference 경로를 설계
- [[F2096] Battery·BMS·전용 전원·안전 Board 설계](F2096/README.md): Battery/BMS·24/12/5/3.3V 예시 rail·e-fuse·역극성·종료 sequencing을 설계
- [[F2097] 내부 Frame 및 기구 Architecture 설계](F2097/README.md): Fusion master frame·joint 지지·board/battery/sensor 배치를 parametric CAD로 설계
- [[F2098] 내부 배치·배선·Connector·Harness 설계](F2098/README.md): 전원/모터/고속data harness·keying·strain relief·service loop를 설계
- [[F2099] 열·소음·진동·EMI 대응 설계](F2099/README.md): 열원·fan/motor/speaker진동·EMI/ESD 대책을 설계/측정
- [[F2100] HW Prototype #1 제작](F2100/README.md): COTS와전용보드 hybrid Prototype#1 조립·부품/firmware baseline을 구성
- [[F2101] ROS2/HW 통합 및 Bring-up 시험](F2101/README.md): ROS2 Driver/topic/diagnostics·HW bring-up·통합 기능을 확인
- [[F2102] HW Prototype #2 개선 및 제품화 설계](F2102/README.md): EVT결함→Rev.B 보드/배선/열/정비 개선→제품화 gate를 관리
- [[F2103] HW 신뢰성·안전·양산성 검증](F2103/README.md): DVT신뢰성·안전·EMI/ESD·제조 jig 및 수리/검사 기준을 구성
- [[F2125] 4~6채널 MEMS Mic Array HW](F2125/README.md): 4~6채널 MEMS Mic Array의 동기/beamforming/AEC/AGC/DOA 경로를 검증
- [[F2132] Main Camera 사양·위치·시야각 검증](F2132/README.md): 1080pHDR UVC 기본/RGB-D 옵션의 FOV·설치거리·calibration을 검증
- [[F2135] Stage 확장 Modular Interface 표준](F2135/README.md): Stage확장 모듈의 기계/전원/통신/하중 interface를 표준화
- [[F2136] 관절 Motor Bench·열·소음·수명 검증](F2136/README.md): motor bench의 torque/speed/heat/noise/lifetime 근거와전환 gate를 구성
- [[F2156] NFC Fashion·Accessory 인식 HW](F2156/README.md): NFC tag 인식·장착/교체·duplicate/위조·테마 안전모드를 구성
- [[F2221] Fusion·AI 기반 Mechanical CAD·BOM·도면 Workflow](F2221/README.md): Fusion masterCAD와Python parameter/BOM/drawing 검토 workflow를 구성
- [[F2222] COTS 70%·Custom 30% 전자구성 및 전환 Gate](F2222/README.md): COTS70/Custom30 구상 및make/buy·공급/원가·EVT/DVT전환 gate를 관리
- [[F2223] 전용 Power·Safety Board 개발](F2223/README.md): Power/Safety PCB의 DC/DC·e-fuse·watchdog·전원분리/종료를 설계
- [[F2224] STM32 Motion·I/O·Safety Controller Board](F2224/README.md): STM32G4/H7 Motion/I/O/Safety 보드의CAN-FD/RS485·timer·enable·fault를 설계
- [[F2225] RK3588 SoM 양산 Carrier Board 개발](F2225/README.md): DVT 이후 RK3588 SoM Carrier의USB/MIPI/HDMI/DDR관련SI·Ethernet/M.2·전원/boot를 설계
