# F2015-S02

Jira: https://lumira077.atlassian.net/browse/KR1-146

현재 ObservationGate("face")는 외부 모델 fixture 확률과 quality/시간/사용자 계약을 검증한다. 실제 face detector·landmark·감정 모델 adapter를 후속 구현한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 모델/서비스 및 재현 버전, S03 동의된 subject-separated 평가·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: 조명/각도/가림/연령별 coverage·macro-F1/UAR·ECE·unknown 비율·p50/p95 지연; 사용자 혼선/철회 후 처리 0건

제한: 실제 카메라/감지/추적/landmark/감정 모델·가중치/라이선스·calibration·동의된 평가 dataset·실기 시험 미연결. MediaPipe blendshape는 표정 계수이며 감정 정답이나 준비된 심리 분류기가 아니다.

증적: source/model/config/policy version, label/calibration dataset, subject split, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
