# F2017-S04

Jira: https://lumira077.atlassian.net/browse/KR1-158

원문 비저장·동의/기억 접근 제한·모델/prompt 변경 회귀와 사용자 정정 흐름을 검증한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 모델/서비스 및 재현 버전, S03 동의된 subject-separated 평가·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: 문맥별 macro-F1·ECE·self-report/추론 구분률·부정/타인 오탐·unknown·위기 경로 false positive/negative(별도 검증)

제한: 실제 sentiment/context/위기 의미 분류기·LLM·동의된 대화 dataset·사용자 연구 미연결. exact-match의 unknown은 실제 위기 감지 실패를 해결한 것으로 간주하지 않는다.

증적: source/model/config/policy version, label/calibration dataset, subject split, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
