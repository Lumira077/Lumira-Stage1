# [F2033] 센서 통합 및 시간 동기화

Jira: https://lumira077.atlassian.net/browse/KR1-262

camera/audio/touch/IMU 등 센서 metadata를 공통 시간축·좌표/calibration으로 결합하고 stale/누락/clock reset을 처리한다.

source/frame id·seq/timestamp/clock domain·epoch·common-clock transform/offset/drift·sensor schema/unit·calibration/extrinsics·metadata/raw 민감도·queue/skew bounds.

actual driver/clock calibration → bounded metadata synchronizer → Epic-03 fusion/Epic-05 track/Epic-04 audio clock. 현재 already-common timestamp에 latest sample pairing만 구현한다.

## 단계별 개발
- sensor clock domain·ROS/system/steady time·offset/drift/skew·TF/unit·QoS/queue·reset/loss/privacy·Simulation Case를 설계한다.
- SensorSynchronizer의 allowlist/seq/freshness/clock reversal·latest metadata pair·50ms skew·일회 소비·reset epoch를 구현한다.
- 실제 camera/mic/touch/IMU driver·HW timestamp/offset/drift·frame loss/재연결/queue·sim time reset·노이즈/지연·민감 raw 차단을 검증한다.
- 실환경 동기성·장시간 drift·sensor/calibration/time parameter freeze·불량 격리/재연결·rollback 증적을 확정한다.

## 검증·제한

sensor skew/drift p50/p95·frame loss/stale/queue depth·재연결/reset·단위/좌표 mismatch·개인정보 비저장

actual drivers/PTP/HW clock calibration·raw buffer/message_filters/TF/offset estimation 미구현. supplied common clock을 검증하며 실제 clock synchronization을 완료한 것이 아니다.

S01 계약/평가 기준 검토, S02 실제 ROS2/HAL/센서/제어 adapter 및 재현 버전, S03 실제 장비의 제어/센서/전원 품질·통합/성능/안전 증적, S04 실환경 임무 검증·Parameter Freeze·rollback·Q1/R1 증적 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-06/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 8개 합성 입력 시험. 실제 카메라/인식 모델/센서/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/epoch/quality/live/VAD/echo를 공급한다; 실제 인증·동의·센서/분류 서비스가 아니다.

도구 참조: [ROS2 Jazzy QoS 계약](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html) — 후속 후보; 미설치/미연결.
