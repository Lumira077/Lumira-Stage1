# [F2023] 표정·음성·동작 동기화

Jira: https://lumira077.atlassian.net/browse/KR1-185

표정·음성·동작을 동일 발화/재생 시계로 정렬하고 끼어들기·지연·실패 시 세 채널의 일관된 상태를 유지한다.

owner/epoch/turn·generation·cue id/channel/offset·audio playback clock·alignment version·queue bound·cancel generation·채널별 ACK/실제 재생 및 관절 feedback.

F2020 face/F2021 audio/F2022 motion cue → timeline proposal queue → renderer/player/controller ACK. F2012 cancel/활성 사용자 변경 시 큐 폐기·generation 무효화·세 채널 cancel ACK.

## 단계별 개발
- audio-clock 기준 cue/offset·deadline/priority·late/drop·drift/resync·pause/buffer/cancel 및 ACK timeout 계약을 설계한다.
- 현재 Timeline은 one active context·generation·bounded due cue 정렬/배출·역행 거절·cancel flush와 모든 채널 ACK 전 새 turn 차단을 구현한다.
- 실제 playback clock·display frame·joint feedback skew/drift·network/underrun·cancel residual·ACK timeout을 통합 시험한다.
- 사용자 자연성·동기 어긋남/끼어들기 평가·큐 원문 비저장·rollback·장애 후 기본표정/물리 정지 정책을 검토한다.

## 검증·제한

face/audio/motion onset/skew/drift p50/p95·late/drop·취소 요청→ACK/물리정지·잔여출력·clock reversal

actual clock/renderer/audio/motor adapter·ACK timeout/watchdog·자동 동의/사용자 전환 이벤트 전파 미구현. 가상 ACK는 물리 정지 증거가 아니다.

S01 계약/평가 기준 검토, S02 실제 renderer/TTS/제어 adapter 및 재현 버전, S03 실제 장비의 표현 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-04/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 11개 합성 입력 시험. 실제 TTS/디스플레이/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/clearance/rights/intent를 공급한다; 실제 인증·환경/권리/의미 검증 서비스가 아니다.

도구 참조: [ros2_control Joint Trajectory Controller](https://control.ros.org/jazzy/doc/ros2_controllers/joint_trajectory_controller/doc/userdoc.html) — 후속 후보; 미설치/미연결.
