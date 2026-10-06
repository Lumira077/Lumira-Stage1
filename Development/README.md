# EPIC-07~16 및 EPIC-18~20 개발 작업

현재 Jira의 13 Epics, 148 Features, 557 Sub-tasks를 기준으로 작성했다. 원본 설명/이미지와 현재 계층을 보존하며 Epic-17은 이번 변경 범위에서 제외했다.

## 실행

Python 3.11+, 표준 라이브러리만 사용한다.

```bash
python Development/runtime/run.py
python Development/runtime/review.py Epic-07/F2039/contract.json
```

61개 행동 시험은 13분야의 소규모 offline utility를 검증한다. 148개 Feature 전체를 구현/검증한 시험이 아니다. 23개 Feature에 부분 utility를 매핑했고, 나머지는 명세/작업계약/증적 검토 도구만 작성했다. contract.json은 기능별 개발 범위·데이터·경계조건·지표·필요 입력을 제공한다. task.json/README.md는 기존 Sub-task의 단계별 작업계약이며 실제 작업 완료 증적이 아니다.

## 현재 구현과 제한

| 분야 | 실행되는 부분 | 추가 필요 |
|---|---|---|
| Navigation | 작은 grid 4-neighbor A*·unknown 차단 | SLAM/AMCL/Nav2, footprint/inflation, 동적회피/속도/도킹/ROS adapter |
| Manipulation | 질량/힘/slip 기반 한손/양손/지원 제안 | 실제 perception/IK/trajectory/force loop·양팔/5-Finger HW |
| Care | timezone-aware occurrence 중복 억제·quality 값 보류 | 실제 scheduler/푸시/수신 ACK·rPPG/낙상 모델·Pilot |
| Kids | 검수/권리/연령/시간 gate | 실제 콘텐츠·학습/언어/표현·부모 인증/Pilot |
| App | allowlisted setting patch·version conflict·copy isolation | 모바일/UI·backend·pairing/auth/push/WebRTC·device ACK |
| Cloud | SHA256/board/version/expiry/power gate | 실제 signature/KMS·A/B bootloader·install/rollback·Cloud/Fleet |
| Security | trusted fixture scope/epoch/expiry·strict enum telemetry | 암호화·identity·cert/key·감사무결성·독립Safety MCU |
| Billing | 정수 quota·in-memory idempotency·refund tombstone | 동시성/영속transaction·예약/취소·PG/webhook 서명·대사 |
| Home | 허용기기/action·민감명령 fixture 확인·Scene 제안 | Matter commissioning·실제실행/receipt·승강/전도/가사 |
| Hardware | BOM 중복/전압범위/검토상태 검토 | CAD/회로/ERC/DRC·PCB/제작·bench/EVT/DVT·인증 |
| IP | counsel-verified timestamp 기한 후보 검토 | 실제 특허검색/claim chart·변리사/FTO·출원/접수증 |
| Finance | Decimal 현금흐름·단순 주식수 희석 계산 | 최신 실제 재무/세무·주주계약/optionpool·전문검토·투자 |
| Sales | 동의한 fixture event 수·dedup/conflict | 실제 consent CRM·고객/채널/캠페인/주문·분모/귀속 검증 |

모든 물리/외부 실행 0. release_ready=false. signature_verified/consent/confirmation/ratings는 trusted fixture 입력이며 실제 인증·서명·법적승인·안전검증을 뜻하지 않는다. OTA SHA256은 파일 무결성만 검증한다. 코드의 경로/파지/Scene/stop는 actuator 실행 권한이 없다. 법률기한을 자동 산출하지 않으며 변리사가 확인한 날짜만 받는다. 금액/판매/투자 가정은 illustrative이며 실적/투자확정이 아니다.

## 연결 상태

현재 사용: Jira, GitHub, Python unittest, GitHub Actions. 공식 Nav2/MoveIt/DYNAMIXEL/OpenTelemetry/Uptane/OWASP/Matter/n8n/Fusion/PATENTSCOPE/KIPRIS 링크는 참조 및 후속 연동 후보다. 실제 runtime/account/secret/장비 연결을 뜻하지 않는다. 계정키는 Jira나 소스에 직접 기록하지 않고 환경별 Secret 참조로 공급해야 한다.

## 작업 공백과 일정

Epic-19 현재 Sub-tasks 31, Epic-20 46. Feature별 missing_stages는 현재 Jira에서 S01~S04가 없는 단계이며 자동으로 신규 이슈를 만들지 않았다. 첨부에 적힌 추가 작업은 상위 설명에 남아 있어도 실제 Sub-task가 없으면 등록 완료로 계산하지 않는다.

Epic-08 F2146, Epic-11 F2153, Epic-12 F2124/F2161/F2162, Epic-14 F2214/F2219/F2220/F2158/F2163의 due date가 상위 Epic 종료일을 넘는다. 기존 날짜는 유지하고 책임자가 출시/범위/일정을 검토해야 한다. 이미지 요약의 Feature 번호/묶음 오류보다 Jira와 상세표를 식별 기준으로 사용한다.
