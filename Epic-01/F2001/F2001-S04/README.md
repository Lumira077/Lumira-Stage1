# F2001-S04 초기 사용자 온보딩 사용자 검증·운영지표·Release

[Jira KR1-6](https://lumira077.atlassian.net/browse/KR1-6) · [GitHub 소스](https://github.com/retri/KER-Robot/tree/main/Epic-01/F2001/F2001-S04)

가명 이벤트 수집, 세션·재시도별 지표 집계, 정적 Dashboard, 사용자 검증 평가, 증적에 결합된 Release 판정, 개발용 백업·복원 시험을 제공한다. **개발 검증 소스이며 실제 사용자/로봇/운영 배포 및 Release 완료 증적이 아니다.**

## 실행

Python 3.11 이상, 표준 라이브러리만 사용한다. 저장소에서 S02/S03/S04를 함께 내려받고 이 디렉터리에서 실행한다.

```sh
python -m unittest discover -s tests -v
python -m onboarding_ops.runner --out results
python -m http.server 8080 --directory results --bind 127.0.0.1
# http://127.0.0.1:8080/dashboard.html
```

`python -m onboarding_ops.runner --out results --require-release`는 동일한 개발 검증 후 Release 차단 시 종료 코드 1을 반환한다. 기본 실행의 종료 코드 0은 소프트웨어 시험 성공만 뜻한다. HTTP 서버는 정적 결과를 열람하는 개발용이며 원격에 공개하지 않는다.

## 결과

- `report.json`, `tests.txt`: 실행 환경의 실제 소프트웨어 시험 결과
- `events.jsonl`, `metrics.json`, `metrics-by-route.json`: 합성 서비스 시나리오에서 수집된 가명 이벤트와 기간·버전·경로별 집계
- `dashboard.html`: 오프라인 정적 검토 화면; 실시간 운영 모니터링 서버가 아님
- `study-simulated.json`, `study-evaluation.json`: 양식 예시 60건; 실제 참가자 인정 수 0
- `sandbox-restore.json`: 삭제·철회 재적용과 진행 중 세션 보존 시험; 운영 복원 승인 아님
- `release-evidence.json`, `release-gate.json`: 실사용·실기·운영 복귀·결함·Q1/R1 승인 미확보로 blocked

S02/S03의 고정 의존성은 `docs/dependency.json`의 SHA-256으로 확인한다. CI는 S03 회귀 시험과 S04 실행 결과를 Artifact로 보관한다. 저장소의 `evidence/local/`은 이번 로컬 실행의 개발 증적이다. 합성 가명 ID는 실행마다 달라지며 식별 키와 원본 서비스 DB는 결과에 포함하지 않는다.

## 통합 범위와 제한

`ObservedService`는 S03 `LabService`의 저장 완료·재시도·취소 전이를 계측한다. 기존 S02 웹 서버는 자동으로 이 클래스에 교체되지 않는다. 운영 도입 시 API 서비스 팩토리·인증·권한·실제 장치 어댑터를 연결하고 지표 이벤트 계약을 검토해야 한다. SQLite 단일 프로세스 Prototype이며 분산 내구성, 원격 모니터링, 키 관리, 실제 배포를 구현하지 않는다. 이벤트 수집 실패는 등록 트랜잭션을 취소하지 않고 `dropped_events`로 노출하므로 운영 경보 연결이 필요하다.

HMAC 가명은 익명화를 보장하지 않는다. 키 공급·교체·동의·접근·보존·삭제 정책은 운영 승인 대상이다. Release 검토 키를 스스로 만들어도 Q1/R1 권한 증명이 되지 않는다. 유닛 시험의 정상 승인 사례는 알고리즘 검증용 합성 데이터다.

[사용자 검증 계획](docs/user-study.md) · [지표 계약](docs/metrics.md) · [운영 절차](docs/runbook.md) · [배포·복귀](docs/deployment.md) · [사용 안내](docs/user-guide.md) · [추적표](docs/traceability.md) · [Release 기록](docs/release-notes.md)
