# KR1-1102 시스템 경계·인터페이스 v0.1

작성일: 2026-10-06 KST | Lumira KR1 Sprint1 | 수행: AI 설계·개발 초안

## 결과와 경계
Pi 5 8GB+AI HAT+13 TOPS는 보유 기준. UNO-A 주행·센서, UNO-B 관절은 R4 Minima 권장 구성이다. 구조도는 KR1-1102_Architecture_R1.png 참조. 기능별 책임자는 역할 제안이며 실제 담당자 배정이 아니다.

|모듈|역할 소유자 제안|입력→출력|오류 시 상태|
|---|---|---|---|
|설정·가슴 UI|R5|터치·계정 설정→명시적 기능 요청|설정 보존, 구동 DISARM, 오류 안내|
|음성 I/O|R2|USB mic/재생→발화 이벤트/AEC reference|마이크 장애 표시, 터치 대체, 재생 중단|
|대화·클라우드 adapter|R2|동의된 발화→대화 이벤트/응답|망/기한 초과 응답 폐기, 로컬 오류 문구|
|시각·Hailo|R2/R4|CSI 영상→사람/물체 메타데이터|시각 기반 추종 중지; 독립 추락 센서 유지|
|표정·화면|R6/R5|대화 상태→얼굴/가슴 UI|정적인 오류 상태; 구동과 독립|
|제스처 planner|R3|allowlist 동작 이름→제한된 관절 목표|취소·범위 초과 거절; 자동 재허용 금지|
|MCU bridge|R3|명령/heartbeat↔USB 상태|기한 만료·CRC·seq 오류 거절, 세션 초기화|
|UNO-A|R3/R4|인코더/ToF/범퍼→휠/Pi 상태|로컬 정지·독립 watchdog 경로|
|UNO-B|R3/R4|제한된 관절 목표↔DXL 상태|명령 만료/버스 장애 감지; 기계 지지 조건의 안전 정지|
|전원·독립 인터록|R4|비상정지/충전/전압/watchdog→동력 허용|휠·관절 분리 차단, 로직은 종료 절차|

## ICD 초안
|ID|출발→도착|매체·데이터|주기/기한 초안|권한·실패|
|---|---|---|---|---|
|I01|앱/터치→설정|인증된 설정 요청, device/session ID|이벤트|소유권/동의 확인, 중복 요청 idempotency|
|I02|음성→대화|발화 완료·취소·원문 임시 처리|이벤트|일반 로그에는 원문 제외|
|I03|대화→표정|IDLE/LISTENING/THINKING/SPEAKING/ERROR|상태변경+5Hz|상태 timeout이면 IDLE/ERROR|
|I04|대화→planner|gesture allowlist·request ID|이벤트|LLM 각도/전압 직접 명령 불가|
|I05|planner→UNO-B|고유 세션·seq·축 ID·각도·profile·CRC|명령 최대50Hz; 목표값|수신 기준 기한·soft limit·ID 검증|
|I06|이동 요청→UNO-A|좌우 속도·가속 제한·유효기한|20~50Hz; 목표값|센서 valid+ARM+충전 아님일 때만|
|I07|Pi↔MCU|HEARTBEAT/STATUS/FAULT|HB50ms, 상실200ms 목표|추락 대응 기한과 별개; 실측 필요|
|I08|ToF→UNO-A|각 채널 거리·valid·age|추락4개 각20Hz 목표|100ms age 한계 후보, invalid는 이동 금지|
|I09|전원→MCU|ESTOP_OK/CHARGE_PRESENT|하드웨어+상태 보고|상태 보고는 실제 차단의 대체가 아님|
|I10|카메라→Hailo|CSI/rpicam 프레임|영상모델별 시험|FPC 굽힘/드라이버/모델 지원 검증|

## 데이터·좌표·OS
관절은 rad, 속도 rad/s, 휠 m/s, 거리 m, 시간 단위는 이름에 명시. ROS frame은 base_link, head_link, camera_optical_frame 제안; 실제 TF는 CAD/URDF·원점 확인 후 게시한다. 미확인 센서 값을 0이나 정상으로 대체하지 않는다.
ROS 시간은 로깅/프레임에, 로컬 monotonic clock은 수신 후 기한에 사용. 서로 다른 보드 monotonic timestamp를 직접 빼지 않는다. clock 동기 없는 이전/지연 패킷은 세션·seq와 bridge/MCU 수신 TTL을 함께 검증한다.
Pi OS·Hailo camera stack과 ROS2 지원 환경 조합 미확정. 개발 ROS2 Jazzy 참조와 Pi OS 패키지 호환을 별도로 확인하며 Ubuntu 설치만으로 Hailo 동작을 보장하지 않는다.

## 시작·오류·종료
전원 인가→MCU DISARM→장치/센서/버스 확인→사람 ARM→제한 동작. 서비스 재시작·USB reconnect는 새 세션/DISARM. 종료는 정지→지지 가능한 관절 자세→파일 동기화→Pi 종료. 급정지 시 중력 낙하/전도 대책 필요.
공간 자율주행은 제외. 인터넷이 동력 허용 판단에 직접 관여하지 않는다. 클라우드 동의/통신 실패는 구동 안전 계층에 영향을 주지 않아야 한다.

## 쟁점·리뷰
UNO 모델/수량, R4 Shield library, 모터 stall·관절 하중, battery chemistry, HDMI·USB 전류 예산, 충전 검출 단선 정책, safety 차단부·기계 지지 미확정. R1/R3/R4 검토 제안 2026-10-09. 구조도·ICD 작성 완료, 실물/인간 리뷰 미수행.
