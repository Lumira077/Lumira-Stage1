# [F2029] 주변 상황 및 사람 존재 감지

Jira: https://lumira077.atlassian.net/browse/KR1-231

사람의 존재/접근/이탈과 주변 상황을 인지하여 대기/깨우기·상호작용을 전환하고 불명확/센서 장애 시 unknown으로 처리한다.

person/scene detection·track bbox·count·distance/bearing/unit/source/calibration·presence score·sensor readiness/timestamp·owner/epoch·consent·scene 민감도/원본 비저장.

person detector/proximity/depth → presence/approach metadata → Epic-01 활성 사용자/Epic-02 대기/깨우기/Epic-06 제한된 상황 입력. 존재는 사용자 identity/장애물 안전 검증과 구분한다.

## 단계별 개발
- person/scene/물체 범위·Stage1/Stage2 navigation 분리·confidence/hysteresis·거리/depth validity·unknown/stale·개인정보/보존 계약을 설계한다.
- 현재 PresenceGate는 supplied person score의 high/low hysteresis·3-frame stability·gap/센서/동의 unknown·owner/epoch·frame order 검증을 구현한다.
- 실제 person detector/센서 precision/recall·approach/leave·거리/조명/혼잡/TV 이미지·sensor outage·지연/unknown·false wake를 검증한다.
- 대기/깨우기/개인정보·집 내부 배치 비저장·scene 접근·운영 drift/재연결/rollback을 검토한다.

## 검증·제한

person precision/recall·false wake/leave·distance/bearing error·coverage/unknown·p95·센서 장애 복구·민감 scene 노출 0건

실제 detector/카메라/depth/proximity·object/scene/위험 인지·접근 방향/거리·driver/대기 mode event 미구현. 사람 score gate는 obstacle clearance나 지도/SLAM이 아니다.

S01 계약/평가 기준 검토, S02 실제 인식 모델/센서/제어 adapter 및 재현 버전, S03 실제 장비의 인지/추적 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-05/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 9개 합성 입력 시험. 실제 카메라/인식 모델/센서/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/epoch/quality/live/VAD/echo를 공급한다; 실제 인증·동의·센서/분류 서비스가 아니다.

도구 참조: [Ultralytics multi-object tracking (weight/runtime 라이선스 검토 필요)](https://docs.ultralytics.com/modes/track/) — 후속 후보; 미설치/미연결.
