# [F2028] 터치 상호작용

Jira: https://lumira077.atlassian.net/browse/KR1-226

머리·몸체·화면의 터치와 길게 누름을 안정된 상호작용 이벤트로 제공하고 중복/노이즈/고착을 억제한다.

touch sensor/region/contact id·pressed/released·seq·monotonic timestamp·debounce/long/stuck bounds·owner/epoch·sensor health·driver/version/calibration.

실제 capacitive/pressure/touchscreen driver → TouchFSM event → interaction/표현/대화. 안전 긴급 정지는 별도 hardware 경로로 유지한다.

## 단계별 개발
- 센서 region/전기 입력·단위/calibration·tap/long/double·debounce/stuck·동시 입력/순서/복구·사용자/epoch 계약을 설계한다.
- 현재 TouchFSM은 head/body/screen down/up·seq/time order·50ms bounce 제외·1초 long 분류·10초 초과 고착 제외·철회 pending purge를 구현한다. 이벤트는 release 시점에만 생성한다.
- 실제 센서 잡음/연속 접촉/습기/동시입력·고착/driver 재연결·중복·release latency·사용자 전환/철회와 안전 경로를 시험한다.
- 대상 사용자 압력/터치/장갑·접근성·오작동/피드백·운영 calibration/교체/rollback을 검토한다.

## 검증·제한

tap/long 오탐/누락·중복 이벤트·debounce/release p95·고착/재연결·region 혼선·사용자 접근성

실제 touch driver/sensor calibration·double-tap/pressure·contact watchdog/즉시 long 이벤트·자동 사용자/철회 event 미연결. release 기반 Prototype은 고착 중 자동 알림/정지를 구현하지 않는다.

S01 계약/평가 기준 검토, S02 실제 인식 모델/센서/제어 adapter 및 재현 버전, S03 실제 장비의 인지/추적 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-05/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 10개 합성 입력 시험. 실제 카메라/인식 모델/센서/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/epoch/quality/live/VAD/echo를 공급한다; 실제 인증·동의·센서/분류 서비스가 아니다.

도구 참조: [Linux input event API (후속 driver 참조)](https://www.kernel.org/doc/html/latest/input/input.html) — 후속 후보; 미설치/미연결.
