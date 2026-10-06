# [F2133] 음원 유도 Face Tracking·Head 미세 정렬

Jira: https://lumira077.atlassian.net/browse/KR1-241

음원 유도 1차 방향과 얼굴 중심 오차로 헤드 yaw를 미세 정렬하고 대상 소실/위험/불확실 시 새 동작을 보류한다.

owner/epoch·track id·DOA/camera extrinsics/FOV·normalized face center·measured joint yaw/time/dt·quality·joint limits/velocity/acceleration/jerk·clearance/stop/watchdog feedback.

F2127 track/DOA → measured yaw/vision geometry → bounded target proposal → Epic-06 ROS safety controller/FollowJointTrajectory feedback; Epic-04 gaze와 시선 계약. 현재 executable=false.

## 단계별 개발
- 마이크/camera/head frame·pixel/FOV/extrinsics·coarse/fine phase·deadband/gain·yaw/pitch·velocity/가감속/jerk·lost/stop/clearance/watchdog 계약을 설계한다.
- 현재 HeadAligner는 supplied DOA 또는 normalized face_x의 pinhole/FOV yaw 오차·proportional gain/deadband·±60도 clamp·30도/초 step bound를 구현한다. stale/lost/low quality/stop/clearance 불명확 시 현재 yaw proposal을 반환한다.
- 실제 모터/URDF/encoder·FOV/extrinsics calibration·pixel/angle error·추적 jitter/가림/이동/다중 사용자·limit/가감속/jerk/stop/watchdog·부하를 검증한다.
- 응시/머리 움직임 불편·안전 거리·접촉·추적 해제 UX·실제 실패 복구/기본자세·config rollback을 검토한다.

## 검증·제한

face center/angle tracking error·jitter/settling/획득 p95·joint limit/velocity/가감속/jerk·lost/stop/clearance·전류/온도

실제 head motor/controller/feedback·yaw/pitch calibration·track identity/자동 epoch event·가감속/jerk/collision/watchdog·물리 정지 ACK 미연결. 예시 FOV/gain/limits는 승인 필요이며 hold proposal이 실제 물리 정지를 뜻하지 않는다.

S01 계약/평가 기준 검토, S02 실제 인식 모델/센서/제어 adapter 및 재현 버전, S03 실제 장비의 인지/추적 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-05/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 11개 합성 입력 시험. 실제 카메라/인식 모델/센서/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/epoch/quality/live/VAD/echo를 공급한다; 실제 인증·동의·센서/분류 서비스가 아니다.

도구 참조: [ros2_control Joint Trajectory Controller](https://control.ros.org/jazzy/doc/ros2_controllers/joint_trajectory_controller/doc/userdoc.html) — 후속 후보; 미설치/미연결.
