# EPIC-05 사용자·환경 인지

Jira: https://lumira077.atlassian.net/browse/KR1-215

6개 Feature(F2026~F2029/F2127/F2133), 24개 Sub-task. 첨부 상세 6 Feature/55 SP 및 AI로봇사업.docx를 기준으로 한다.

실행: `python Epic-05/runtime/run.py` / `python Epic-05/runtime/demo.py` (Python 3.11+, stdlib).

현재: 8차원 합성 vector 메모리 등록/유사도 후보·철회 epoch, supplied gesture tag 안정화/3-point angle, touch down/up seq/debounce/long/stuck 처리, supplied person score hysteresis, given DOA/visual bearing 후보 결합, supplied yaw/face offset의 bounded head proposal.

실제 detector/embedding/liveness·pose/hand·person/scene/위험 classifier·DOA/VAD/AEC·camera tracker·센서/ROS/head motor 없음. 인증/동의/quality/live/VAD/echo/clearance는 신뢰된 호출자 fixture로 실제 분류/서비스와 구분한다. 후보는 authenticated=false, 제스처/헤드 계획은 executable=false, 물리 정지는 확인하지 않는다.

원본 영상/얼굴/대화·집 내부 가구 배치/지도는 저장하지 않는다. 개발용 fixture template는 메모리만 사용한다. 실제 생체 template의 암호화/권한/보존/철회·삭제 및 backup purge는 production adapter와 검토가 필요하다. 후보 ID를 인증으로 간주하거나 다른 사용자 profile/memory를 공개하지 않는다.

통합 계약: Epic-01 F2001 등록/F2002 동의/F2004 활성 사용자 → camera/sensors → F2026/F2027/F2028/F2029 → F2127 audio-vision → F2133 head alignment → Epic-02 turn/대화 및 Epic-03 감정/Epic-04 시선/표현/Epic-06 제어. 자동 event bus/epoch 전파·실제 controller는 추가 개발이다. unknown/센서 장애/다중 후보/가림은 재확인·게스트·움직임 보류로 처리한다.

F2127/F2133 현 due 2027-09-30은 Epic due 2027-06-30보다 늦다. Stage1 핵심/추적 확장·OTA 일정을 분리 검토하고 Jira 상태·담당자·날짜를 변경하지 않는다. 초기 이미지의 object/scene/위험/Stage2 navigation은 확장 구상이며 현재 person gate의 구현 범위를 넘는다.

Release: 실제 consented 평가(FAR/FRR, precision/recall, gesture macro-F1, ID switch, sensor failure, tracking error/latency)·camera/mic/touch/head·production privacy/auth·watchdog/물리 stop·실사용/Q1/R1/rollback 증거 확보 전 release_ready=false. 개발 예시 threshold/FOV/joint limits를 실제 안전 기준으로 쓰지 않는다.
