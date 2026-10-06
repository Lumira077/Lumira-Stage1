# [F2019] 감정 변화 추세 관리

Jira: https://lumira077.atlassian.net/browse/KR1-164

동의된 감정 후보의 시간 변화와 개인 기준을 요약하고 사용자 정정·삭제·철회를 반영하며 추세를 진단으로 단정하지 않는다.

owner/epoch·event id·timestamp·label의 최소 metadata, retention/window·samples/coverage·개인 baseline/정정 version 제안. 원본 음성/영상/문장/얼굴 template 제외.

F2018 후보 → retention/consent gate → owner-isolated trend summary; F2002 동의 epoch·F2004 활성 사용자·삭제 이벤트 계약. 실제 서비스 인증/이벤트·저장소 adapter 미연결.

## 단계별 개발
- 시간 window·min samples·개인 baseline·unknown/gap 제외·정정/삭제·동의 철회·보존/복구 계약을 설계한다.
- 현재 TrendStore는 bounded in-memory metadata·TTL·dedup·owner/epoch·철회/삭제 purge·descriptive counts를 구현한다. 개인 baseline/장기 DB/자동 알림은 후속이다.
- 시간 gap/만료·중복·epoch replay·사용자 격리·철회/삭제·저장 장애/backup restore 개인정보 회귀와 실제 장기 시계열 정확도를 검증한다.
- 사용자에게 추세/불확실성을 설명하고 정정·보존/삭제 UX·운영 지표·장기 데이터 복귀 정책을 검토한다.

## 검증·제한

window coverage·min samples·baseline drift·정정 반영·TTL/철회/삭제 처리 지연·타 사용자 정보 노출/철회 후 복원 0건

실제 인증/epoch 이벤트·암호화 DB·backup purge·장기 사용자 dataset·개인 baseline·정정 API·알림 기준/검토 미연결. summary는 기술통계이며 clinical risk/자동 신고는 생성하지 않는다.

S01 계약/평가 기준 검토, S02 실제 모델/서비스 및 재현 버전, S03 동의된 subject-separated 평가·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-03/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 15개 합성 입력 시험. 실제 모델/카메라/마이크/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/epoch/quality를 공급한다; 실제 인증·quality classifier가 아니다.

도구 참조: [Python datetime/time reference](https://docs.python.org/3/library/time.html) — 후속 후보; 미설치/미연결.
