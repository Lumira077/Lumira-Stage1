# F2157-S02

Jira: https://lumira077.atlassian.net/browse/KR1-39

현재 수행 범위: 로컬 핵심 로직 Prototype

- NFC 이벤트 어댑터와 Registry 조회를 구현하고 태그 입력을 내부 승인 outfit_id로만 해석한다.
- 테마 패키지를 로컬에서 검증·준비하고 얼굴·음성·Motion·대화 모듈에서 준비 ACK를 수집한다.
- commit 시 theme_revision을 함께 갱신하고 하나라도 실패하면 이전 완전한 테마 또는 기본 Persona로 복귀한다.
- 제거·presence 만료·센서 고장·사용자 거부 이벤트를 처리하고 빠른 의상 교체에도 오래된 sequence가 재적용되지 않게 한다.

산출물: Theme Service, NFC 어댑터, 승인 테마 패키지, commit·복귀 Prototype, 에셋 검증기.

완료조건: 2개 이상 승인 의상과 기본 Persona 전환이 재현되고 에셋 하나가 없으면 부분 활성화가 발생하지 않는다.

역할 제안(배정 변경 없음): R2 테마, R5 패키지, R4 입력, R3 출력

자동 시험은 `Epic-01/integration/run.py`에서 수행한다. 시험 환경은 개발용·단일 프로세스이며 실제 장치의 출력 취소나 안전성 증거를 대신하지 않는다.
