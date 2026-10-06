# EPIC-03 멀티모달 감정 인식

Jira: https://lumira077.atlassian.net/browse/KR1-143

5개 Feature(F2015~F2019), 20개 Sub-task. 첨부 상세 목록과 AI로봇사업.docx 구상을 기준으로 보완한다.

`python Epic-03/runtime/run.py` / `python Epic-03/runtime/demo.py` (Python 3.11+, stdlib).

현재: 외부 모델 점수 계약/quality gate, synthetic PCM RMS/zero crossing, 8개 명시 자기보고 exact-match, 확률 fusion/abstention, in-memory 추세/동의 철회/삭제. owner/consent/quality는 신뢰된 caller의 fixture다. 실제 모델·카메라/마이크·로봇·사용자·장기 DB·운영 인증/epoch event 없음.

emotion-v1 label/probabilities와 confidence/quality는 개발 예시이며 실제 감정 ground truth 또는 진단을 뜻하지 않는다. conflict/missing/low-quality는 unknown; 실행 명령/진단/자동 알림은 생성하지 않는다. 원본 영상·음성·문장은 저장하지 않는다. 개인 baseline/정정/위기 semantic classifier는 미구현이다.

통합 계약: Epic-01 프로필/동의/활성 사용자 → Epic-02 STT/turn/취소 → EPIC-03 face/audio/text → fusion → 개인 추세 → 확인 질문/표현. 실제 서비스 event bus 연결은 후속 작업이다. F2014/KR1-118 안전 정책과 별도의 위기 대응 검증이 필요하다.

평가: consented subject-separated dataset, train/calibration/test 분리, 모델/hash/라이선스, confusion matrix/macro-F1/UAR/ECE/coverage/selective risk와 age/language/lighting/noise별 지연·오탐·철회/삭제 검증. 합성 테스트를 실제 모델 정확도로 보고하지 않는다.

Release: 실제 모델/실기/사용자·운영 rollback/Q1/R1 승인 전 release_ready=false. 현재 Jira due date를 유지하고 첨부 초기 일정과 버전 차이는 검토 필요로 기록한다.
