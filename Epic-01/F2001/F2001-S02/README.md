# F2001-S02 초기 사용자 온보딩 Prototype

[Jira KR1-4](https://lumira077.atlassian.net/browse/KR1-4) · 상위 [F2001 / KR1-2](https://lumira077.atlassian.net/browse/KR1-2) · 선행 [S01 / KR1-3](https://lumira077.atlassian.net/browse/KR1-3)

로컬 설정 웹 UI → 임시 저장 → 등록 → 가상 모듈 설정 적용 → 개인화 첫 인사를 재현합니다. 기기·소유권·TTS·표정·Motion은 **가상 어댑터**입니다. 실제 로봇이나 클라우드 AI에 연결하지 않습니다.

## 빠른 실행
Python 3.11 이상(서비스 의존성 없음). 전체 저장소를 다운로드한 뒤 아래 폴더로 이동합니다.

```bash
cd Epic-01/F2001/F2001-S02
export KER_DEMO_TOKEN="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
export KER_GUARDIAN_TOKEN="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
export KER_ADAPTER_MODE=simulated
python3 -m ker_onboarding.api
```

Windows PowerShell에서는 다음 환경변수 설정을 사용합니다.

```powershell
cd Epic-01/F2001/F2001-S02
$env:KER_DEMO_TOKEN = python -c "import secrets; print(secrets.token_urlsafe(32))"
$env:KER_GUARDIAN_TOKEN = python -c "import secrets; print(secrets.token_urlsafe(32))"
$env:KER_ADAPTER_MODE = "simulated"
python -m ker_onboarding.api
```

브라우저에서 **http://127.0.0.1:8081**을 엽니다. 직접 생성한 개발용 토큰을 입력하고 연결 확인 → 기기 선택 → 설정 시작을 누릅니다. 동일 로컬 PC 터미널에서 환경변수 값을 확인하여 붙여 넣습니다. 토큰은 로그·소스·Jira에 기록하지 마세요. 브라우저에는 최근 세션 ID만 저장하고 토큰은 저장하지 않습니다.

## 화면 사용
1. 본인: KER_DEMO_TOKEN, demo-device-01, self + local-demo-owner.
2. 보호자: KER_GUARDIAN_TOKEN, demo-guardian-01, guardian + demo-child-01. 사전 승인된 가상 시험 관계입니다.
3. 게스트: KER_DEMO_TOKEN, demo-guest-01, guest + guest. 정식 프로필을 만들지 않고 동의는 모두 false입니다.
4. 언어·호칭·목적·선호·동의를 단계마다 저장합니다. 선호 단계만 기본값으로 건너뛰기가 가능합니다.
5. 최종 확인 체크 후 저장하고 최종 등록을 누릅니다. 이어 가상 설정 적용과 첫 인사를 실행합니다.
6. 중단 후 페이지 재로드 시 토큰을 다시 입력하고 연결 확인 → 세션 재개를 누릅니다.
7. 앞 단계 수정 시 후속 설정과 동의·확인을 다시 입력해야 합니다. 출력은 등록된 프로필에서 읽습니다.

음성 안내·미리듣기·첫 인사는 브라우저 speechSynthesis가 지원되면 재생하며, 선택한 가상 voice_id의 실제 음색을 보장하지 않습니다. 브라우저 재생 음량은 20% 이하로 제한합니다. 오프라인에서도 설정과 텍스트 인사는 동작하며 음성 합성은 브라우저 엔진에 따라 달라집니다.

## 시험과 Demo
```bash
python3 -m unittest discover -s tests -v
python3 scripts/smoke.py
```

smoke.py는 임시 DB와 무작위 토큰을 만들고 실제 HTTP 서버에서 본인·게스트·보호자 등록, 3회 중복 완료, TTS 실패 후 재시도, 첫 인사를 검증합니다. 서버가 실행 중이고 동일 토큰 환경인 터미널에서는 `python3 scripts/demo.py`도 가능합니다. Demo가 완료된 DB를 다시 사용하면 등록 중복 오류가 정상입니다.

선택적 브라우저 시험(Node.js 20 이상):
```bash
npm install
npx playwright install --with-deps chromium
npm run test:ui
```

설정 입력·재로드 재개·건너뛰기·동의 거부·등록·적용 실패/재시도·첫 인사를 조작합니다. 캡처는 evidence/에 저장되며 토큰 필드는 마스킹합니다. GitHub Actions도 같은 시험을 수행하고 캡처를 artifact로 보관합니다. 설치는 공식 [Playwright 안내](https://playwright.dev/docs/browsers)를 따릅니다.

## 실패 재현·초기화
TTS 1회 실패: 서버 시작 전 `KER_SIM_FAIL_ONCE=tts`를 설정합니다. UI의 가상 설정 적용을 다시 누르면 기존 프로필과 성공 ACK를 유지한 채 재시도합니다. 단절 시험/재연결 버튼은 가상 장치의 상태만 변경합니다.

서버 종료(Ctrl+C) 후 알려진 개발용 DB만 초기화합니다.
```bash
export KER_ENV=development
python3 scripts/reset_dev.py --confirm-prototype-reset
```
PowerShell: `$env:KER_ENV = "development"` 이후 `python scripts/reset_dev.py --confirm-prototype-reset`. 임의 DB 경로는 받지 않으며 data 디렉터리나 DB가 심볼릭 링크이면 거부합니다. `--db`로 별도 지정한 DB에는 적용하지 않습니다.

## 계약과 제한
[설계·T01~T12 추적](docs/design.md) · [DB 스키마](docs/schema.sql) · [OpenAPI](docs/openapi.json) · [로컬 시험](docs/test-report.txt)

API http://127.0.0.1:8081/openapi.json. v0.2.0 / 스키마2 / 동의정책 prototype-2026-10-v1. S01의 검증 규칙을 고정 복사해 독립 실행하며 S01 코드를 변경하지 않습니다. S01 DB를 재사용하지 말고 S02용 DB를 사용하세요.

운영용 로그인·보호자 승인·기기 소유권 증명·암호화 저장·실제 F2002/F2004/F2005·ROS2/TTS 연결은 미구현입니다. 상태 applied는 가상 ACK 완료이며 hardware_connected는 항상 false입니다. 실기 연결·성능·안전 시험은 S03 범위입니다. 단일 프로세스 로컬 개발 서버이고 외부 공개 서버로 배포하지 않습니다. S02 Jira 인수 승인은 R1 검토 후 판단합니다.
