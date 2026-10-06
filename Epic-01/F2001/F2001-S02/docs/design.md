# F2001-S02 Prototype 기술 및 인수 검토

## 구조와 선행 계약
S01 고정 커밋 e3109197d73879d7c2952549aabc3489c5c75854의 상태·검증·SQLite 규칙을 core.py로 복사했습니다. S02는 registration 단계, 버전 동의, 적용 outbox와 가상 장치/출력 adapter, 설정 웹 UI를 추가합니다. 외부 런타임 패키지 없이 Python 표준 라이브러리로 서버가 실행됩니다. 선택적 화면 시험만 Playwright 1.51.1을 사용합니다.

API에서 인증 토큰을 actor와 허용 device 목록에 매핑합니다. UI는 actor_id 권한을 생성하지 않습니다. 본인 subject는 actor와 같아야 하며 보호자는 local-demo-guardian→demo-child-01의 명시적 fixture만 허용합니다. 실제 보호자 승인과 소유권 증명은 별도 개발이 필요합니다.

## 상태와 모델
임시 세션 in_progress → committed / cancelled / expired. 정식 등록은 committed, 게스트는 guest_ready 응답(profile_id=null). 등록 단계는 registration→language→profile→purpose→preferences→consent→review입니다. PATCH의 revision 검증과 앞 단계 변경 시 후속 무효화는 S01과 동일합니다. current_step/completed_steps는 조회 응답에서 초안으로부터 계산합니다.

정식 완료 트랜잭션은 profiles, consent_events, applications(pending), sessions, completions를 함께 저장합니다. 실패 시 부분 등록 없이 롤백합니다. mutation_id가 같으면 최초 완료 응답을 재사용합니다. 완료 응답은 최초 pending 스냅샷이며 최신 적용 상태는 GET application으로 조회합니다.

적용 서비스: pending → failed 또는 applied. context/tts/expression/motion별 ACK를 application UUID와 함께 저장합니다. 실패하면 기존 프로필과 성공 ACK는 유지합니다. 재시도는 미완료 모듈만 수행하고 동일 적용 ID를 사용합니다. applied 이후 재요청은 저장된 상태를 반환합니다. 실제 외부 모듈 도입 시 동일 적용 ID의 모듈 멱등 처리와 timeout 정책이 필수입니다. 현재 가상 호출에는 실기 네트워크 지연·모터 동작이 없습니다.

ProfileAdapter의 최소 F2002 계약은 actor/subject/type, 언어·호칭·목적, preferences, permissions, policy_version을 반환합니다. 활성 사용자와 제품 정책에 필요한 필드는 전달 계약 수준이며 실제 F2004/F2005 호출은 없습니다. 첫 인사는 applied 및 가상 연결 상태를 확인한 뒤 저장된 Context의 호칭·선호를 사용합니다.

consent_events는 최초 등록 시 목적별 granted/정책버전/시각을 기록합니다. 등록 전 선택 변경은 revision 기반 초안이며 감사 이력을 누적하지 않습니다. 등록 후 동의 철회 API/이력은 후속 작업입니다. 게스트는 모든 동의가 false이고 profiles 및 consent_events를 만들지 않습니다. 세션·Context는 24시간 TTL 임시 데이터이며 서버 반복 처리에서 만료 정리합니다. 장기 기억 저장·조회 API는 제공하지 않습니다. SQLite 및 백업의 물리 복구 불가능 삭제를 보장하지 않습니다.

## API
시작/조회/단계 저장/완료/취소는 S01 경로를 유지합니다. S02 추가:
- GET /v1/bootstrap: 계정 및 장치 fixture, 기본값, 정책 버전.
- GET /v1/devices/{device_id}, POST .../connection: 가상 상태/단절·재연결 시험.
- GET /v1/onboarding/sessions/{session_id}/application: 최신 적용 상태·ACK.
- POST .../apply: 가상 적용 또는 재시도.
- POST .../greeting: 적용 완료 후 저장 Context 기반 첫 인사.
- POST .../guide, .../preview: 안내·미리보기 payload, 실제 음성·구동 미수행.
- GET /v1/profiles/{profile_id}/context: 소유자에게만 정식 프로필 Context 반환.

문법400, 인증401, 권한403, 타인/없는 대상404, 순서/충돌/미적용409, 만료410, 입력422. 가상 모듈 실패는200 응답의 apply_status=failed로 보고하므로 클라이언트는 HTTP 상태뿐 아니라 적용 상태를 확인해야 합니다. Host/Origin 제한, Bearer token, no-store, CSP를 적용합니다. payload/token/URL을 접근 로그에 기록하지 않습니다.

## Jira 내부 체크리스트 추적
| 항목 | 구현 증적 | 제한/후속 |
|---|---|---|
| T01 환경 | README, VERSION, .env.example, CI | Python3.11+; 실기 환경 미검증 |
| T02 상태기계 | core.py, service.py | 적용 상태는 별도 저장 |
| T03 데이터 | schema.sql, SQLite, consent_events | S01→S02 운영 DB migration 없음; 신규 개발 DB |
| T04 API | api.py, OpenAPI | 로컬 전용 |
| T05 검증 | validate, 역할/기기 검사 | 실기 capability 범위 미연계 |
| T06 화면 | web/, UI test | 선호만 skip; 주요 개인정보·동의는 skip 없음 |
| T07 음성 안내 | guide/preview, browser speech | 브라우저 음성, 실제 로봇 TTS 없음 |
| T08 기기 연결 | SimulatedDevice, 단절·재연결 | 실기 adapter 미구현, hardware 모드 거부 |
| T09 프로필 | ProfileAdapter, context API | 최소 계약; 실제 F2002 서비스 호출 없음 |
| T10 완료 | DB 트랜잭션, mutation_id | 단일 로컬 프로세스 |
| T11 적용·인사 | applications, module_acks, greeting | 모두 simulated ACK, Motion 물리 동작 없음 |
| T12 재현·시험 | unittest36, HTTP smoke, CI UI | S03 실기/성능/안전 및 R1 검토 필요 |

## S03 인계 및 인수
확인된 기능은 신규 등록, 중단 복원, 반복 완료/적용, 범위 검사, 동의 거부, 타인 접근 거부, 저장 롤백, 적용 실패 후 재시도, 오프라인 로컬 인사, 개발용 reset 제한입니다. UI 캡처와 시험 결과는 CI run/artifact에서 확인합니다. API/스크립트·화면 데모에서는 가상 연결 여부를 명시합니다.

S03은 실제 pairing/소유권·보호자 권한, 기기 capability, TTS 음색·속도·음량, context epoch, 모듈 timeout/중복 ACK, 출력 취소, 장애 복구, 동의 철회, 민감정보 저장 보호, 성능 및 구동 안전 한계를 검증해야 합니다. S02 코드 게시와 시험 성공은 실기 통합 완료 또는 Jira 인수 승인을 의미하지 않습니다.
