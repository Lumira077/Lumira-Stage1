# F2003 개인화 장기 기억

[Jira Feature KR1-12](https://lumira077.atlassian.net/browse/KR1-12) · [GitHub 소스](https://github.com/retri/KER-Robot/tree/main/Epic-01/F2003)

동의한 활성 사용자의 기억 후보를 저장하고 사용자 확인 후 검색·정정·삭제·만료·응답 context 구성을 지원하는 로컬 개발 Prototype이다. F2002의 실제 서비스 코드를 직접 호출해 소유권·활성 프로필·현재 동의를 확인한다. **외부 LLM, 벡터 DB, 클라우드 동기화 및 실제 로봇 출력은 연결하지 않았다.**

| 패키지 | Jira | 구현 |
|---|---|---|
| F2003-S01 | KR1-13 | 실행 가능한 계약·민감/지시 패턴 필터·규칙 추출·검색 점수·API 설계 |
| F2003-S02 | KR1-14 | 기억 CRUD·후보/확인·revision/멱등·F2002 동의·검색 인덱스·HTTP API·응답 ticket |
| F2003-S03 | KR1-15 | 구조화 대화 bridge·실패 fallback·권한/context 시험·합성 품질 평가 |
| F2003-S04 | KR1-16 | 전체 실행기·지표/Dashboard·사용자 관찰 평가·개발 복원·Release 차단 |

## 전체 실행

Python 3.11 이상, 외부 pip 패키지 없이 표준 라이브러리로 실행한다. 전체 저장소를 내려받아 F2001/F2002/F2003 상대 경로를 유지한다. 의존 소스 해시는 각 dependencies.json과 f2002-dependency.json으로 확인한다.

```sh
cd Epic-01/F2003/F2003-S04
python -m memory_ops.runner --out results --samples 100
python -m http.server 8080 --directory results --bind 127.0.0.1
# http://127.0.0.1:8080/dashboard.html
```

기본 종료 코드 0은 소프트웨어·합성 fixture 검증 성공만 의미한다. `--require-release`를 추가하면 Release 미완료로 종료 코드 1을 반환한다. Dashboard는 정적 개발 스냅샷이다.

## 결과

단계별 tests.txt, report.json/md, quality.json, performance.json, metrics.json, study.json, sandbox-restore.json, release-gate.json, dashboard.html을 생성한다. report에는 후보 SHA·실행 환경·시험 수·검증 범위를 기록한다. 다섯 측정 경로는 규칙 추출/후보 저장/검색/context 준비/context 반환이며 각각 100회 이상 측정한다. 실제 발화·모델 추론·네트워크·로봇 동작의 지연이 아니다.

quality는 고정 합성 18개 발화의 후보 판별·추출 내용 일치와 검색 4개 사례를 평가한다. 이 수치는 실제 사용자 대화의 추출/검색 품질·보안 성능을 나타내지 않는다. rules는 한국어 `나는 …을/를 좋아해`, 영어 `I like …`만 지원한다. 자유 대화 요약·의미 추론은 없다. 직접 구조화 입력으로 fact/promise 후보를 만들 수 있지만 약속의 일정 실행·장치 제어는 지원하지 않는다.

## 개인정보·한계

장기 기억 동의와 대화 원문 저장 동의를 구분하며 원문 대화/검색어를 저장·로그에 남기지 않는다. 기억 후보는 모든 경우 사용자가 확인해야 검색에 포함된다. 기본 후보 보존 7일 이하, 확인 기억 기본 30일·최대 365일은 제안 설정이며 운영 승인 대상이다. 프로필·기억 DB는 평문 SQLite로 암호화·키 관리·접근·보존 승인이 필요하다.

검색은 정규화 문자열과 bigram 유사도이며 임베딩/벡터 DB가 아니다. 한 kind/topic은 하나의 확인 기억 slot이므로 동시에 보존할 독립 주제는 다른 topic으로 지정한다. 민감/악성 지시 필터는 제한된 패턴만 검출하며 모든 변형을 차단한다고 주장하지 않는다. 외부 LLM 도입 시 별도 추출 품질·프롬프트 공격·누출 평가가 필요하다.

F2002 동의 철회/삭제는 다음 접근 또는 명시적 synchronize에서 확인한다. 앱은 즉시 이벤트를 전달해야 하며 서비스 비사용 중 실시간 purge가 자동 실행되지는 않는다. F2002에서 철회 후 재동의를 F2003 관측 없이 완료하면 과거 철회를 감지할 수 없으므로 실제 도입 전 승인된 consent epoch/event 연동이 필수다. 제공 revoke/grant 경로는 로컬 purge·차단을 먼저 적용하며 재동의로 옛 기억을 복원하지 않는다.

준비 ticket에는 기억 원문을 담지 않고 반환 직전에 현재 프로필 revision/generation/동의와 기억 revision을 확인한다. 이미 호출자에게 전달된 데이터의 회수·외부 캐시 제거, DB 간 동시 변경의 원자성·분산 잠금·실제 출력 시점 재검사는 미구현이다. 단일 동기 프로세스 Prototype이며 실제 로봇/운영 배포 승인은 blocked다.

[설계](F2003-S01/design.md) · [S02 실행](F2003-S02/README.md) · [시험](F2003-S03/README.md) · [운영·복귀](F2003-S04/runbook.md) · [추적표](docs/traceability.md)
