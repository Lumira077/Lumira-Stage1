# [F2015] 얼굴 표정 기반 감정 추정

Jira: https://lumira077.atlassian.net/browse/KR1-144

얼굴 표정·시선·눈깜박임·머리 자세를 관찰해 감정 후보와 신뢰도/관찰 근거를 제공하고 낮은 품질에서는 판단을 보류한다.

사용자/동의 epoch, frame timestamp, face_count, 조명/각도/가림 quality, 얼굴 관찰 특징, 모델/label schema 버전, 확률분포. 원본 영상·얼굴 template는 기본 비저장; 추적 identity를 사용자 인증으로 취급하지 않는다.

FaceObservation → quality/consent/active-user gate → EmotionObservation. 다른 사용자·epoch·schema 거절; 다중 얼굴·저품질·stale/미래 frame은 unknown.

## 단계별 개발
- 표정 특징과 감정 label의 차이를 정의하고 카메라 권한·사용자 결합·조명/각도/가림 조건별 데이터와 평가 계약을 설계한다.
- 현재 ObservationGate("face")는 외부 모델 fixture 확률과 quality/시간/사용자 계약을 검증한다. 실제 face detector·landmark·감정 모델 adapter를 후속 구현한다.
- 얼굴 탐지 coverage·subject-separated macro-F1/UAR·ECE·selective risk와 조명/각도/가림별 latency/abstention을 평가한다.
- 원본 비저장·동의 철회·사용자 전환·카메라 고장 복구와 배포/rollback을 사용자 검증으로 확정한다.

## 검증·제한

조명/각도/가림/연령별 coverage·macro-F1/UAR·ECE·unknown 비율·p50/p95 지연; 사용자 혼선/철회 후 처리 0건

실제 카메라/감지/추적/landmark/감정 모델·가중치/라이선스·calibration·동의된 평가 dataset·실기 시험 미연결. MediaPipe blendshape는 표정 계수이며 감정 정답이나 준비된 심리 분류기가 아니다.

S01 계약/평가 기준 검토, S02 실제 모델/서비스 및 재현 버전, S03 동의된 subject-separated 평가·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-03/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 13개 합성 입력 시험. 실제 모델/카메라/마이크/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/epoch/quality를 공급한다; 실제 인증·quality classifier가 아니다.

도구 참조: [MediaPipe Face Landmarker](https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker) — 후속 후보; 미설치/미연결.
