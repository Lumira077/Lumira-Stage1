# [F2025] 춤·노래 퍼포먼스

Jira: https://lumira077.atlassian.net/browse/KR1-195

권한이 확인된 노래·춤 콘텐츠를 beat/발화/표정/제스처 타임라인에 맞추고 stop/quiet/장비 제한을 우선한다.

content/asset id·hash/license/rights evidence·duration/repeats/beat cues·sound volume·joint plan·thermal/clearance·owner/epoch/turn·cancel.

사용자 시작/콘텐츠 허용 → beat cue/제스처 validation → F2023 timeline → audio/display/motion ACK. 현재 실제 음악/노래/모터 재생 없음.

## 단계별 개발
- 콘텐츠/저작권·연령/quiet·반복/총길이·beat/cue·stop·관절/전류/온도 제한 및 offline asset 계약을 설계한다.
- 현재 PerformancePlanner는 asset token·duration/repeat upper bound와 trusted rights/quiet/clearance/stop 기반 enabled proposal을 생성한다.
- 실제 beat/음성/모션 skew·장시간 부하/온도·stop/네트워크·금지/권한 만료·에셋 누락 복구를 검증한다.
- 사용자 콘텐츠 만족/과자극·볼륨·선호/정정 및 rights/version/배포 rollback을 검토한다.

## 검증·제한

beat-skew·sync/stop p95·온도/전류/부하·반복/길이 위반·무권한 콘텐츠 출력 0건·사용자 만족

실제 노래/음악/beat extraction·license 검증 서비스·trajectory/장비/thermal·player 미연결. rights는 trusted fixture이며 실제 권리 증거 검증이 아니다.

S01 계약/평가 기준 검토, S02 실제 renderer/TTS/제어 adapter 및 재현 버전, S03 실제 장비의 표현 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-04/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 7개 합성 입력 시험. 실제 TTS/디스플레이/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/clearance/rights/intent를 공급한다; 실제 인증·환경/권리/의미 검증 서비스가 아니다.

도구 참조: [ros2_control Joint Trajectory Controller](https://control.ros.org/jazzy/doc/ros2_controllers/joint_trajectory_controller/doc/userdoc.html) — 후속 후보; 미설치/미연결.
