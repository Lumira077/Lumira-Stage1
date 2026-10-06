# KR1-1106 Sprint1 통합 검토·다음 우선순위 R1

작성일 2026-10-06 KST. 이 문서는 AI 비동기 문서·소스 검토 기록이다. 실제 회의 개최, 참석자 발언, R1/R3 승인 또는 실기 시험을 수행한 것으로 기록하지 않는다.

## 검토 근거와 총괄 판정
Jira KR1-1101~1106의 목적/완료기준을 읽고 산출물 5건을 작성·검토했다. 사용자 최신 보유 Pi5 8GB+AI HAT+13TOPS와 UNO 연결 초안을 우선 적용했다. 원래 board 9의 Sprint API 목록은 0건이었으나, Sprint1 텍스트가 있는 6개 Story는 실제 존재한다. 이번에는 Sprint 객체 생성·시작·종료를 하지 않고 이슈별로 수행/저장한다.

총괄 판정: **보완 필요 / 사람 검토 대기**. 문서·모의 SW 수행은 완료했으나 정의된 사람 검토·실물 확인은 미완료이므로 Done으로 전환하지 않는다. AI 검토는 최종 승인 서명을 대신하지 않는다.

|작업|이번 산출물|수행 증거|남은 완료 조건|판정|
|---|---|---|---|---|
|KR1-1101|사용자2군·시나리오3건·입력/반응/실패/범위외|Report_R1.md|R1/R6 검토, 실제 관찰|초안 작성 완료·검토 대기|
|KR1-1102|모듈 책임·ICD10개·구조도PNG·쟁점|Report_R1.md + Architecture_R1.png|모듈 실명 소유자/OS·HW 통합 확인|초안 작성 완료·검토 대기|
|KR1-1103|노드/토픽5개·JSON계약·Python TCP·ROS2 adapter|unit_tests.log, mock_transport.jsonl, mock_summary.json|신규 DDS 실행·R3 검토|모의 검증 완료·DDS 미실행|
|KR1-1104|10개품목군×2후보·필수사양/보류사유|BOM_v0.1.csv·Report_R1.md|R1/R3/R4 호환성 검토/정격 확인|비교표 완료·선정 미확정|
|KR1-1105|위험12건·원인/검출/안전상태/확인시험|risk_register.csv·Report_R1.md|담당 검토·물리 대책 시험|위험 검토 초안·잔여위험 OPEN|

## 신규 실행 결과
Python 두 프로세스 localhost TCP: 7건 발행/수신, 6건 허용, 비상정지 후 gesture 1건 예상 거절, 예상 밖 결과 0건. 서로 다른 PID를 원시로그에 기록. 계약 시험 16개 통과. Python/ROS2 adapter 구문 검사 통과.
실행환경 Ubuntu24.04 x86_64, Python3.12.14. ros2/rclpy/docker 없음. 신규 ROS2 DDS 실행, Hailo inference, UNO firmware, motor/sensor/power 실기, 사용자 조사, 외부 연락 발송은 수행하지 않음. hardware_execution=false, release_ready=false.
기존 KR1-248의 과거 CI 기록은 참고 증거이며 이번 결과와 별도 버전이다. 신규 기준은 /ker/sim/sprint1의 sprint1-v0.1; 기존 joint-v1의 timeout·한계값을 덮어쓰지 않았다.

## 검토 의견과 조치
- RV01 제품 범위 충돌: 과거 ‘주행 후속’ 표현과 최신 ‘제한 이동 개발’ 구분. 이번 문서에 후자를 반영하되 공간 자율주행/무검증 탁상 이동 제외.
- RV02 메인 보드: Pi+13TOPS 보유 확정, UNO 모델/수량·Shield 호환·battery/motor 정격 미확정. 구매·전원 핀 최종결선 전 확인.
- RV03 OS: Pi Hailo camera stack과 ROS2 배포 조합은 별도 통합 gate. 단순 OS 선택으로 양쪽 호환을 확정하지 않음.
- RV04 안전: MCU 로컬 감시와 독립 하드웨어 차단, 중력 낙하·회생·추락 정지거리 대책이 실물 미검증.
- RV05 ROS QoS: safety retained sample도 age 검사, command volatile. cross-topic 수신 순서 보장하지 않으므로 safe state 없으면 gesture 거절.
- RV06 도움 요청: 실제 전달 확인 전 ‘전송됨’ 표시 금지. 이번 시험은 외부 전송 0건.

## 결정·담당·기한 제안
기존 KR1-1101 담당 aijei IJ 유지. 나머지 기존 미배정 유지. R1=범위/결정, R2=대화, R3=제어, R4=전장, R5=앱/UI, R6=사용성 역할은 기존 문서 제안이며 실명 승인 관계를 추정하지 않는다.

|미결정|담당 역할 제안|검토 목표일(미확정)|선행조건|
|---|---|---|---|
|범위·시나리오 승인|R1/R6|2026-10-08|보고서1·2 검토|
|UNO·모터·배터리·LCD 실물 모델|R4/R3|2026-10-08|제품명/사진·정격|
|OS/ROS/Hailo·통신 계약|R3/R4|2026-10-09|동시 구동 개발환경|
|안전 회로·지그 계획|R4/R3|2026-10-09|위험 목록·정격|
|담당 실명·일정·Sprint 운영|R1|2026-10-08|등록 후보4건 검토|

## Sprint2 후보 백로그 — 실제 등록됨
|이슈|우선순위 제안|작업|완료 증거|
|---|---|---|---|
|[KR1-1108](https://lumira077.atlassian.net/browse/KR1-1108)|P0|Pi5/Hailo/ROS2·DDS 통합|버전·QoS·재시작·stale 원시로그|
|[KR1-1109](https://lumira077.atlassian.net/browse/KR1-1109)|P0|UNO·DXL·휠·8ToF bring-up|실물SKU·단일장치·고장주입 계측|
|[KR1-1110](https://lumira077.atlassian.net/browse/KR1-1110)|P0|전원·충전 인터록·이동 지그|승인회로·회생/낙하/정지거리 증거|
|[KR1-1111](https://lumira077.atlassian.net/browse/KR1-1111)|P1|사용자2군·음향·터치 평가|승인계획·실제관찰·실패대응|

후보는 각각 EPIC-06/16/17에 연결했으며 실제 Sprint 배정·개시나 담당자 약속은 확정하지 않았다. P0/P1는 보고서의 상대적 우선순위 제안이다.

## 검토서 기입란
R1 검토자/일자/범위 판정: 미기입. R3 계약·통신 검토: 미기입. R4 전원·기구 안전 검토: 미기입. R6 사용자 시나리오 검토: 미기입.
기록 시 승인/보완 항목, 근거 파일 버전·hash, 담당·기한을 함께 남긴다. 보완 후 같은 이슈에 새 revision으로 결과물을 저장한다.
