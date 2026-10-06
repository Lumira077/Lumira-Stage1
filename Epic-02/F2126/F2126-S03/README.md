# F2126-S03

Jira: https://lumira077.atlassian.net/browse/KR1-141

- 무음·길이 불일치·NaN·채널 오류·물리 불가능 지연·double talk·실물 에코/소음 시험 설계
- 운영 품질지표: ERLE·double-talk 왜곡·DOA MAE·STT CER/WER 개선·frame loss. 장비·모델·설정·sample·기대/실제 결과·결함/재시험을 묶어 증적화한다.
- 실제 장치의 지연·정확도·안전·취소·실패 복구를 검증하고 시뮬레이션 합격과 구분한다. 개인정보 노출·금지 전송/출력은 시험 집합에서 0건이어야 한다.

산출물: 자동 시험 소스·CI report·실기 평가표·결함/재시험 증적

상위 Feature 완료조건: 실제 TTS 재생·잡음·거리/방향 조건에서 AEC/DOA/STT 품질 목표를 충족하며 DOA를 사용자 인증으로 사용하지 않는다.

현재 제한: 현재 기초 DSP 계산·계약 시험. adaptive AEC·실제 beamformer·TDOA 추정·마이크 배열·실물 성능 미구현

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
