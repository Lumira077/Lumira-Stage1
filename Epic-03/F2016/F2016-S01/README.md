# F2016-S01

Jira: https://lumira077.atlassian.net/browse/KR1-150

마이크·sample rate·window/VAD·잡음/echo·언어/화자별 특징/평가 입력 계약을 정의한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 모델/서비스 및 재현 버전, S03 동의된 subject-separated 평가·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: 조건별 UAR/macro-F1·ECE·SNR/음성 coverage·silence/echo 오탐·unknown·p50/p95 end-to-end 지연

제한: 실제 마이크/VAD/pitch/rate/echo·감정 모델 및 consented 평가 음성 미연결. RMS·zero crossing만으로 감정 label을 판정하지 않는다.

증적: source/model/config/policy version, label/calibration dataset, subject split, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
