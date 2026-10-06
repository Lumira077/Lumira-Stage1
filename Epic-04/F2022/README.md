# [F2022] 목·팔·허리 제스처 라이브러리

Jira: https://lumira077.atlassian.net/browse/KR1-180

목·팔·허리의 인사·끄덕임·위로 제스처를 버전 관리하고 관절/속도/충돌/접촉 제한 안에서 계획한다.

gesture id/version·joint names/radian waypoints·timestamp·measured start pose·joint position/velocity/acceleration/jerk·collision/clearance·current/temp·stop state.

GestureProposal → 실제 measured-state bridge·safety controller → FollowJointTrajectory goal/feedback/result. 현 로컬 plan은 executable=false이고 ROS/모터 명령을 전송하지 않는다.

## 단계별 개발
- 실제 URDF/관절 mapping·home/calibration·가동/속도/가감속/jerk·충돌/끼임/thermal·stop 경로·gesture version 계약을 정의한다.
- 현재 GestureLibrary는 nod/wave/still fixture·position/segment velocity·time order·joint schema·start pose 일치와 clearance flag를 검증한다.
- 실제 관절 feedback/충돌/접촉·가감속/jerk·전류/온도·watchdog/stop/통신 장애·기본자세 복귀를 검증한다.
- 사용자 거리/놀람/불편·접촉 허용·gesture 선호와 calibration/asset rollback을 확인한다.

## 검증·제한

tracking error·position/velocity/acceleration/jerk limits·실제 clearance/접촉·stop latency·전류/온도·failure recovery

provisional limits이며 실제 URDF/모터/feedback/충돌·끼임 감지·가감속/jerk/watchdog/E-stop controller 미연결. start pose 불일치는 거절하며 실제 복귀 trajectory를 계산하지 않는다.

S01 계약/평가 기준 검토, S02 실제 renderer/TTS/제어 adapter 및 재현 버전, S03 실제 장비의 표현 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-04/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 9개 합성 입력 시험. 실제 TTS/디스플레이/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/clearance/rights/intent를 공급한다; 실제 인증·환경/권리/의미 검증 서비스가 아니다.

도구 참조: [ros2_control Joint Trajectory Controller](https://control.ros.org/jazzy/doc/ros2_controllers/joint_trajectory_controller/doc/userdoc.html) — 후속 후보; 미설치/미연결.
