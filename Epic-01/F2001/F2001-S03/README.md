# F2001-S03 온보딩 통합·성능·출력 제어 시험 소스

[Jira KR1-5](https://lumira077.atlassian.net/browse/KR1-5) · 상위 [F2001 / KR1-2](https://lumira077.atlassian.net/browse/KR1-2) · 선행 [S02 / KR1-4](https://lumira077.atlassian.net/browse/KR1-4)

S02 서비스에 출력 제어 Broker를 연결해 정상·장애·권한·출력 억제 규칙을 시험합니다. **실제 로봇·모터·스피커에는 연결하지 않습니다.** 실제 기기의 음량/관절/정지 시간/전원 차단은 미측정입니다. 소프트웨어 시험 성공과 S03 실기 인수 완료를 구분합니다.

## 실행
전체 KER-Robot 저장소를 다운로드하세요. S02 소스는 인접 폴더에 있어야 합니다. Python 3.11 이상, 외부 패키지 설치와 토큰이 필요 없습니다.

```bash
cd Epic-01/F2001/F2001-S03
python3 -m onboarding_lab.runner --mode simulated --samples 100 --out results
```
Windows PowerShell에서는 `python3` 대신 `python`을 사용합니다. 결과: results/report.json, report.md, tests.txt, http-smoke.txt. 전체 자동 시험 42개, ONB-01~16의 소프트웨어 부분, 경로별 100회 지연 측정과 S02 실제 HTTP 회귀 데모를 실행합니다.

시험만 실행:
```bash
python3 -m unittest discover -s tests -v
```

- S02 참조 커밋과 파일 SHA256을 docs/dependency.json으로 검증합니다. 파일이 달라지면 실행을 중단하고 재검토를 요구합니다.
- S03 runner는 해당 실행의 GitHub SHA(또는 local-uncommitted), Python/OS, 의존성·실기 미수행 상태를 보고합니다.
- p50/p95/max와 실패율을 기록합니다. 저장 p95 500ms, 등록→가상 ACK p95 1000ms는 제안 목표입니다.
- 서비스 호출 지연이며 브라우저·네트워크·실제 음성 시작 지연은 포함하지 않습니다. 첫 발화 목표는 미확정입니다.
- --samples는 최소100입니다. --mode hardware는 허용하지 않습니다.

## 구현 내용
- S02와 연결되는 LabService/GuardedOutputs, 적용별 모듈 ACK와 명시적 application ID로 첫 인사 분리.
- 첫 인사와 동일 출력 요청 멱등 처리, 다른 게스트 세션 간 출력 범위 구분.
- 미리보기 묶음 전체 검증 후 큐 생성, 세션 취소/만료 시 지연 출력 차단.
- 소유자·epoch·TTL 검사, 미승인 동작 및 범위 초과 출력 거절.
- 정지 latch, transport 정지 ACK 실패 시에도 소프트웨어 출력 억제, 명시적 검사 확인 후 재승인.
- 재시작 시 이전 queued/executing 출력 취소와 출력 비활성화; 자동 재실행 없음.
- DB 실패, 각 모듈 실패, 네트워크 fixture 단절·복원, 접근권한·동의·등록 무결성 회귀시험.
- 호칭/동의와 같은 핵심 인식값의 명시적 사용자 확인 gate. 실제 STT 모델은 없습니다.

## 코드와 증적
[설계](docs/design.md) · [요구사항 추적](docs/traceability.md) · [실기 시험 환경 기록 양식](docs/hardware-manifest.example.json) · [로컬 실행 결과](docs/local-report.md)

GitHub Actions에서 같은 시험을 수행하고 F2001-S03-test-evidence artifact에 JSON/Markdown/시험 로그를 보관합니다. Jira에 최종 검증 커밋과 CI run을 연결합니다. 생성되는 결과는 실제 실행 측정값이며 고정 성능 수치가 아닙니다.

## 정책·범위 제한
Policy 기본 음량20은 정규화 소프트웨어 값이며 dB 안전 상한이 아닙니다. 말속도 최대1.2, 표현/제스처 수준 최대1은 시험 fixture 정책입니다. 물리 동작은 none만 허용합니다. 제품의 안전 정책은 R3/R4/Q1 승인과 실기 측정으로 별도 확정해야 합니다.

Broker는 단일 프로세스·단일 작업자의 소프트웨어 시험 모듈입니다. 인증된 하드웨어 드라이버, 독립 안전 제어기, 제어 주기, 실제 긴급 정지·토크 차단을 구현하지 않습니다. 실행 중 물리 동작을 중단했다는 증거로 사용할 수 없습니다. 재승인의 inspection_confirmed는 가상 검사 입력이며 실기 승인 권한을 대체하지 않습니다.

S01/S02 소스는 변경하지 않습니다. S02 단독 UI는 S03 Broker를 자동으로 사용하지 않습니다. 여기서는 LabService와 시험 하네스가 Broker를 연결합니다. 이를 실제 API/로봇에 통합할 때 취소·사용자 전환·연결 단절·만료 이벤트를 Broker 정지 경로에 반드시 연결하고 운영 인증/권한도 추가해야 합니다.

**release_ready=false**, 실제 시험 not_run, Q1/R1 검토 대기 상태를 보고합니다. 실기 자료 없이 Jira S03을 Done으로 변경하지 않습니다.
