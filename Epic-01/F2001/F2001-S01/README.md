# F2001-S01 초기 사용자 온보딩 설계 참조 소스

Epic-01 → F2001 → F2001-S01 요구사항·데이터·인터페이스 설계를 실행 가능한 Python 코드로 검증합니다. Python 3.11 이상, 표준 라이브러리만 사용합니다.

## 구현 내용
- 언어 → 호칭 → 사용 목적 → 음성·표현 선호 → 목적별 동의 → 최종 확인 단계.
- SQLite 임시 저장, 재시작 후 복원, revision 충돌 검출, 앞 단계 변경 시 후속 단계 무효화.
- 동일 완료 요청의 멱등 처리와 프로필·완료 기록의 원자적 저장.
- 계정별 세션 접근 제한, 사전 허용된 기기만 시작, 취소 및 24시간 만료 초안 정리.
- REST API, OpenAPI 계약, 자동 시험, 실제 HTTP 데모, GitHub Actions.

## Jira 작업
[Jira KR1-3 — F2001-S01](https://lumira077.atlassian.net/browse/KR1-3)
상위 Feature: KR1-2. 저장소 내 경로: Epic-01/F2001/F2001-S01.

## 실행
`Epic-01/F2001/F2001-S01` 디렉터리에서 실행합니다. 별도 패키지 설치가 필요 없습니다.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/smoke.py
```

수동 API 실행은 임의 토큰을 환경 변수로 설정한 뒤 두 터미널에서 같은 토큰을 사용합니다. 실제 토큰을 저장소에 커밋하지 마세요.

```bash
export KER_DEMO_TOKEN="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
python3 -m ker_onboarding.api --db data/onboarding.sqlite3 --port 8080
# 동일 KER_DEMO_TOKEN 환경을 가진 다른 터미널에서 실행
python3 scripts/demo.py
```

API 계약: http://127.0.0.1:8080/openapi.json. 데모 기기는 `demo-device-01`입니다. 기존 DB로 완료한 뒤 다시 시작하면 `DEVICE_ALREADY_REGISTERED`가 반환됩니다. 반복 데모는 임시 DB를 사용하는 `smoke.py`로 실행하세요.

## 검토 파일
- [설계 및 요구사항 추적](docs/design.md)
- [API 계약](docs/openapi.json)
- [Jira·GitHub 연결 자료](docs/jira-github.md)
- [시험 결과](docs/test-report.txt)

## 적용 범위
이 코드는 S01의 설계 검증용 참조 구현입니다. 실제 회원 인증·로봇 소유권 증명·보호자 승인·게스트 모드·화면 및 음성 UX·암호화 저장·ROS2/TTS/모터 연결은 아직 구현하지 않았습니다. 동의 값은 저장 계약 검증용이며 실제 데이터 수집 서비스를 실행하지 않습니다. 완료 응답의 `apply_status=pending`, `hardware_connected=false`는 기기에 설정을 적용하지 않았음을 의미합니다. 실제 로봇 통합 및 안전 시험은 S02/S03에서 수행합니다.

WSGI 서버는 단일 프로세스 개발 서버이며 127.0.0.1에만 바인딩됩니다. 외부 서비스 배포 전 인증·권한 철회·TLS·DB 보호·부하 시험·동의 이력 및 보존 정책을 추가해야 합니다.
