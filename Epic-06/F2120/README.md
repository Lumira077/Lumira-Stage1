# [F2120] Edge-Cloud AI Orchestrator

Jira: https://lumira077.atlassian.net/browse/KR1-277

Edge·Local·Cloud 실행 위치와 자원 우선순위를 결정하고 generation/취소·장애 fallback으로 대화/인지 결과를 통합한다.

task id/owner/epoch/generation·function/privacy/consent·runtime/resource/latency deadline·network/budget·placement/provider/model/policy version·bounded result/cancel/usage.

Epic-02 policy/F2123 route·Epic-01 동의 → orchestrator scheduling → local/edge/cloud adapters → scoped result integration. 실시간 제어/정지 경로는 Cloud에 배치하지 않는다.

## 단계별 개발
- 제어/인지/대화 기능별 placement·privacy·deadline/resource·우선순위/queue/admission·network/cost·취소/결과 scope·fallback 계약을 설계한다.
- Orchestrator는 trusted kind/privacy/consent/network/resource budget으로 local/edge/cloud/blocked placement·bounded task registry·generation cancel·중복/늦은/다른 placement 결과 거절을 구현한다.
- 실제 local/NPU/GPU/Cloud 실행·resource saturation/deadline·provider 장애·fallback/retry/idempotency·취소/usage·원문 미전송을 통합 시험한다.
- 실환경 임무/장시간·placement/resource/비용/동의 policy freeze·운영 지표·failover/rollback 및 검토 증적을 확정한다.

## 검증·제한

queue/end-to-end deadline·CPU/RAM/GPU/NPU·route/fallback latency·cost/usage·취소/stale result·제어 Cloud placement 0건·민감 전송 0건

actual Provider/NPU/resource probe·latency/cost model·우선순위/timeout/retry/fallback adapter·owner/auth/자동동의 event 미구현. 실제 호출 0이며 budget은 fixture다.

S01 계약/평가 기준 검토, S02 실제 ROS2/HAL/센서/제어 adapter 및 재현 버전, S03 실제 장비의 제어/센서/전원 품질·통합/성능/안전 증적, S04 실환경 임무 검증·Parameter Freeze·rollback·Q1/R1 증적 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-06/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 10개 합성 입력 시험. 실제 카메라/인식 모델/센서/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/epoch/quality/live/VAD/echo를 공급한다; 실제 인증·동의·센서/분류 서비스가 아니다.

도구 참조: [ONNX Runtime](https://onnxruntime.ai/docs/) — 후속 후보; 미설치/미연결.
