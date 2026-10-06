# F2018-S03

Jira: https://lumira077.atlassian.net/browse/KR1-162

동기화 지연·한 modality 누락·품질 저하·모달리티 충돌·사용자 전환/동의 철회·calibration 및 실제 end-to-end 지연을 검증한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 모델/서비스 및 재현 버전, S03 동의된 subject-separated 평가·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: fusion macro-F1/UAR·ECE·coverage/selective risk·missing/conflict unknown·시간 skew·p50/p95 지연·타 사용자 결합 0건

제한: 실제 3 modality adapter/calibration·ROS/event bus/F2010 표현 연결·physical latency 미연결. example 품질/시간/confidence threshold는 운영 승인 대상.

증적: source/model/config/policy version, label/calibration dataset, subject split, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
