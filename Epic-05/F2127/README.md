# [F2127] Audio-Vision 능동 화자 추적

Jira: https://lumira077.atlassian.net/browse/KR1-236

음원 방향·발화 활동·얼굴/사람 위치를 결합해 능동 화자 후보를 추적하고 TV·겹말·다중 사용자 혼선을 줄인다.

DOA angle/unit/confidence·audio timestamp/VAD/echo·visual track id/bearing/quality/timestamp·session epoch·association/ambiguity·head acquisition phase·동의/실제 화자 ground truth.

F2126 AEC/DOA/VAD → coarse acquire proposal → camera/person/face track → audio-vision association → F2004/F2011 활성 화자 확인·F2133 미세 정렬. track id는 인증 identity가 아니다.

## 단계별 개발
- audio→vision→track 상태·DOA/camera/head 좌표 calibration·time skew·candidate/ambiguity·target switch/lost/reacquire·TV/echo/겹말·privacy 계약을 설계한다.
- 현재 SpeakerAssociator는 supplied DOA와 visual bearing의 circular angle·freshness/skew/quality/epoch·20도 후보 cone·10도 ambiguity margin 및 VAD/echo gate를 구현한다.
- 실제 다중 화자/TV/반사/겹말·audio→head→vision 획득·switch/ID switch·occlusion/reacquire·time skew·latency/부하를 검증한다.
- 후보 확인/사용자 정정·추적 불편·원본 비저장·운영 기준/다중 사용자 복구/rollback을 검토한다.

## 검증·제한

active speaker precision/recall·ID switch·TV/echo 오탐·획득/전환/재획득 p95·DOA/vision angular error·time skew/unknown

실제 DOA/VAD/AEC·head 획득·camera tracker/립 활동·지속 추적 상태/전환 hysteresis·auth/epoch event 미연결. 방향 일치는 실제 화자 확정/사용자 인증이 아니며 TV source를 자동 검출하지 않는다.

S01 계약/평가 기준 검토, S02 실제 인식 모델/센서/제어 adapter 및 재현 버전, S03 실제 장비의 인지/추적 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-05/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 10개 합성 입력 시험. 실제 카메라/인식 모델/센서/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/epoch/quality/live/VAD/echo를 공급한다; 실제 인증·동의·센서/분류 서비스가 아니다.

도구 참조: [Ultralytics multi-object tracking (weight/runtime 라이선스 검토 필요)](https://docs.ultralytics.com/modes/track/) — 후속 후보; 미설치/미연결.
