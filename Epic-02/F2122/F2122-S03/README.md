# F2122-S03

Jira: https://lumira077.atlassian.net/browse/KR1-131

- 미지원 runtime/NPU·과다 RAM·온도·변조 모델·비허용 Tool·데드라인 시험 설계
- 운영 품질지표: peak RAM·tokens/s·TTFT·온도/전력·fallback·Tool 거절. 장비·모델·설정·sample·기대/실제 결과·결함/재시험을 묶어 증적화한다.
- 실제 장치의 지연·정확도·안전·취소·실패 복구를 검증하고 시뮬레이션 합격과 구분한다. 개인정보 노출·금지 전송/출력은 시험 집합에서 0건이어야 한다.

산출물: 자동 시험 소스·CI report·실기 평가표·결함/재시험 증적

상위 Feature 완료조건: 선정 모델을 실제 보드에서 실행해 RAM/first token/속도/발열 목표와 승인 Tool 검증을 통과한다.

현재 제한: 현재 자원/Tool gate만 구현; 모델 다운로드·실제 추론·RK3588 NPU/Jetson 가속·실물 benchmark 미실시

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
