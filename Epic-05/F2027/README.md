# [F2027] 손짓·포즈 인식

Jira: https://lumira077.atlassian.net/browse/KR1-221

손짓/상체 포즈를 인사·호출·가리키기·정지 후보로 분류하고 흔들림/중복을 억제하여 상호작용에 전달한다.

owner/epoch·track id·hand/pose landmarks·confidence/visibility·gesture label·frame timestamp·stable window/gap·event id·모델/hash/언어 아닌 gesture ontology·consent.

camera/landmark/gesture adapter → scoped stable gate → InteractionCandidate → Epic-02 대화/Epic-04 표현. gesture stop 후보는 실제 E-stop hardware와 구분한다.

## 단계별 개발
- hand/pose label·landmark 좌표계/visibility·거리/조명·stable window·반복 억제·사용자 track/epoch·stop/cancel event 계약을 설계한다.
- 현재 GestureGate는 supplied wave/point/open_palm/stop tag의 3-frame stability·gap/중복/low confidence·owner/epoch·철회 gate와 2D 3-point angle 계산을 구현한다.
- 실제 gesture/pose 모델 macro-F1·오탐/누락·움직임/거리/조명/가림·다중 사용자·event latency·stop 후보/실제 안전 경로 분리를 검증한다.
- 사용자/문화/연령별 제스처 이해·오작동·접근성·대체 터치/음성 입력과 모델/정책 rollback을 확인한다.

## 검증·제한

gesture macro-F1/confusion matrix·pose angle error·거리/조명/가림 coverage·중복 이벤트·FAR/누락·p95 latency

실제 MediaPipe/카메라/landmark/gesture classifier·track/자동 epoch event·stop controller·사용자 평가 없음. supplied stop tag는 safety_estop=false/executable=false이다.

S01 계약/평가 기준 검토, S02 실제 인식 모델/센서/제어 adapter 및 재현 버전, S03 실제 장비의 인지/추적 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-05/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 10개 합성 입력 시험. 실제 카메라/인식 모델/센서/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/epoch/quality/live/VAD/echo를 공급한다; 실제 인증·동의·센서/분류 서비스가 아니다.

도구 참조: [MediaPipe Gesture Recognizer](https://developers.google.com/edge/mediapipe/solutions/vision/gesture_recognizer) — 후속 후보; 미설치/미연결.
