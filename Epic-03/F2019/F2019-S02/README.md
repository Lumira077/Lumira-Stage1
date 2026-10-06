# F2019-S02

Jira: https://lumira077.atlassian.net/browse/KR1-166

현재 TrendStore는 bounded in-memory metadata·TTL·dedup·owner/epoch·철회/삭제 purge·descriptive counts를 구현한다. 개인 baseline/장기 DB/자동 알림은 후속이다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 모델/서비스 및 재현 버전, S03 동의된 subject-separated 평가·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: window coverage·min samples·baseline drift·정정 반영·TTL/철회/삭제 처리 지연·타 사용자 정보 노출/철회 후 복원 0건

제한: 실제 인증/epoch 이벤트·암호화 DB·backup purge·장기 사용자 dataset·개인 baseline·정정 API·알림 기준/검토 미연결. summary는 기술통계이며 clinical risk/자동 신고는 생성하지 않는다.

증적: source/model/config/policy version, label/calibration dataset, subject split, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
