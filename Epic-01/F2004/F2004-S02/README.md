# F2004-S02

Jira: https://lumira077.atlassian.net/browse/KR1-19

현재 수행 범위: 로컬 핵심 로직 Prototype

- 사용자 선택 UI, 확인 대화, 게스트 모드, 자동 로그아웃 및 가족 구성원 관리 서비스를 구현한다.
- ActiveSession의 epoch를 단조 증가시키고 대화·TTS·표정·Motion 메시지에 같은 epoch를 붙인다.
- 식별 후보 어댑터를 구현하고 원본 영상·음성 대신 필요한 후보 ID·점수만 활성 사용자 서비스에 전달한다.
- 전환 과정에서 새 Context의 적용 ACK를 모은 뒤 재개하며 실패 시 개인화 없는 게스트 Context를 적용한다.

산출물: Active User Service, 가족 관리 UI, 후보 어댑터, epoch 처리 및 게스트 복귀 Prototype.

완료조건: 수동 전환·시간 초과·인식 불확실 경로가 재현되고 이전 epoch의 지연 출력은 소비자가 폐기한다.

역할 제안(배정 변경 없음): R5 세션·UI, R2 확인 대화, R3 큐 처리

자동 시험은 `Epic-01/integration/run.py`에서 수행한다. 시험 환경은 개발용·단일 프로세스이며 실제 장치의 출력 취소나 안전성 증거를 대신하지 않는다.
