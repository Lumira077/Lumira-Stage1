# F2006-S02

Jira: https://lumira077.atlassian.net/browse/KR1-29

현재 수행 범위: 로컬 핵심 로직 Prototype

- 동반자 상태기계와 Context Composer를 구현하고 로컬·클라우드 대화 어댑터에 동일 계약을 적용한다.
- 사용자 선호에 따라 호칭·길이·말투를 조정하고 기억 source_ref를 응답 생성 근거로 전달한다.
- 응답을 발화·표정·제스처 계획으로 분리하고 임의 관절 값 대신 승인된 동작 ID만 출력하게 한다.
- turn_id별 한 backend의 결과만 확정하고 끼어들기 시 TTS 취소·동작 취소를 실행한다.

산출물: Companion Orchestrator, 대화 샘플, 응답 계획 검증기, fallback·cancel Prototype.

완료조건: 정상 대화·끼어들기·timeout 경로가 재현되고 하나의 turn_id에 두 개의 최종 응답이 실행되지 않는다.

역할 제안(배정 변경 없음): R2 주도, R5 backend 연결, R3 출력 취소

자동 시험은 `Epic-01/integration/run.py`에서 수행한다. 시험 환경은 개발용·단일 프로세스이며 실제 장치의 출력 취소나 안전성 증거를 대신하지 않는다.
