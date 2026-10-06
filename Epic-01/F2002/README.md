# F2002 사용자 프로필 및 선호 설정

[Jira Feature KR1-7](https://lumira077.atlassian.net/browse/KR1-7) · [소스](https://github.com/retri/KER-Robot/tree/main/Epic-01/F2002)

F2001에서 등록한 프로필을 가져와 언어·호칭·이용 목적·음성·표정·제스처·선택 동의를 수정하고 로봇의 활성 프로필을 전환하는 **개발 Prototype**다. 네 단계의 실행 소스, 자동 시험, 설계·운영 문서와 CI를 포함한다.

| 패키지 | Jira | 역할 |
|---|---|---|
| F2002-S01 | KR1-8 | 엄격한 계약·입력 검증·F2001 변환·API 설계 |
| F2002-S02 | KR1-9 | SQLite 프로필 CRUD·충돌/멱등·활성 프로필·HTTP API·F2001 bridge |
| F2002-S03 | KR1-10 | 대화/인식/TTS/표현/제어 설정 수신기 모의 통합·안전 시험 |
| F2002-S04 | KR1-11 | 기간별 지표·사용자 검증 평가·정적 Dashboard·sandbox 복원·Release 차단 |

## 실행

Python 3.11 이상, 표준 라이브러리만 사용한다. 저장소를 내려받아 F2001/F2001-S02와 F2002/S01~S04의 상대 경로를 유지한다.

```sh
cd Epic-01/F2002/F2002-S04
python -m profile_ops.runner --out results --samples 100
python -m http.server 8080 --directory results --bind 127.0.0.1
```

`http://127.0.0.1:8080/dashboard.html`로 개발 지표를 확인한다. 각 패키지 README에 개별 실행 명령이 있다. `--require-release`를 추가하면 미완료 Release를 차단해 종료 코드 1을 반환한다. 기본 실행 종료 코드 0은 소프트웨어 검증 성공만 의미한다.

## 구현 범위

프로필 수정은 예상 revision과 mutation_id가 필수다. 동일 요청 재전송은 중복 저장하지 않으며, 키 내용 충돌 및 이미 더 최근 버전이 된 요청은 거부한다. 외부 인증 계층에서 확정한 actor와 authorized_subjects만 신뢰한다. HTTP는 로컬 고정 Demo 사용자에 매핑된 비밀 토큰으로 보호한다. 임의 actor 헤더나 body는 받지 않는다.

활성화마다 장치 generation을 갱신한다. 프로필 변경·전환·정지·단절·복원은 과거 ACK/적용 요청을 무효화한다. 저장 성공과 전체 모듈 적용 완료는 다르다. 프로필 설정은 모의 수신기에서만 처리되며 실제 발화·인식·동작을 실행하지 않는다. 음량 40/표현 2/제스처 1의 cap은 Demo 제안값이지 실제 dB/관절 안전 한계가 아니다.

F2001 bridge는 권한 확인된 committed 비게스트 세션을 한 번 가져오는 snapshot이다. 기존 F2001 DB/API를 수정하지 않는다. 삭제된 import의 tombstone은 재가져오기를 거부한다. F2001과의 양방향 변경/삭제/동의 동기화, 외부 캐시 제거는 추가 통합 대상이다. 오래된 F2001 데이터가 계속 사용되지 않도록 운영에서는 단일 프로필 권위 저장소와 철회 전달 경로를 먼저 확정해야 한다.

## 결과·한계

`results`에는 4개 패키지 tests.txt, report.json, performance.json, metrics.json, study.json, sandbox-restore.json, release-gate.json, dashboard.html을 생성한다. 지표 단위는 저장된 연산 이벤트이며 고유 사용자 성공률이 아니다. 실제 사용자 관찰은 0명이다. CI Artifact는 30일 보관한다. `evidence/local`은 로컬 소프트웨어 실행 증적이다.

단일 프로세스 SQLite, 개발 HTTP, 모의 장치만 지원한다. 실제 로그인·보호자 관계 검증·TLS·암호화·분산 ACK/outbox·실제 로봇 안전·운영 배포/복귀·Q1/R1 권한 승인은 연결하지 않았다. 현재 Release 평가기는 항상 blocked로 유지하며 승인 플래그만으로 배포를 허용하지 않는다. Jira 상태를 Done으로 변경하지 않는다.

[설계](F2002-S01/design.md) · [운영·배포](F2002-S04/runbook.md) · [검증 계획](F2002-S04/user-study.md) · [추적표](docs/traceability.md)
