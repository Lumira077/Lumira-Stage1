# F2001-S01 요구사항·데이터·인터페이스 설계

## 기준과 상태
상위 Feature F2001 초기 사용자 온보딩의 S01 설계 산출물입니다. 실제 Jira 이슈는 [KR1-3](https://lumira077.atlassian.net/browse/KR1-3), 상위 Feature는 KR1-2입니다. 원본 계획의 CSV ID 4001과 Jira key는 구분합니다. 아래 상세 요구사항 ID는 이번 구현의 내부 추적용이며 Jira에 새 sub-task를 생성한 것을 뜻하지 않습니다. 언어·닉네임·호칭·사용 목적·프로필 저장과 다음 부팅 활용을 기준으로 설계를 보완했습니다. 보완된 범위와 수치는 검토 전 제안입니다.

## 사용자 및 기본값
참조 사용자: 로컬 소유자(local-demo-owner). 인증 토큰에서 actor_id와 허용 device_ids를 결정하고 요청 본문에서 계정 ID를 받지 않습니다. 기기 허용 목록은 데모 설정으로 제공됩니다. 실서비스에서는 계정 인증 및 기기 소유권 검증 결과로 대체합니다. 게스트·보호자·복수 사용자 전환은 후속 설계 항목입니다.

초기 선호: device_default 음성, 말속도 1.0, 음량 20, 표정/제스처 1. 음량 0~100, 말속도 0.7~1.3, 표정/제스처 0~3은 데이터 검증 범위이며 로봇 구동 안전 한계가 아닙니다. 실제 최대 출력은 S03 안전 정책과 capability 확인으로 별도 제한합니다.

## 요구사항 추적
| ID | 요구사항 | 구현/증적 |
|---|---|---|
| S01-R01 | 최초 설정 순서 및 누락 방지 | STEPS, save_step; test_order |
| S01-R02 | 언어 ko-KR/en-US 및 호칭 1~40자 | validate; test_unknown_fields |
| S01-R03 | companion/education/care/home 목적 | validate; 정상 완료 시험 |
| S01-R04 | 음성·표현 선호 범위와 타입 검증 | validate; test_invalid_preferences |
| S01-R05 | 기억/대화저장/생체식별/클라우드 전송 각각 boolean 동의 | validate; test_complete_and_false_consents |
| S01-R06 | 변경 후 재확인 및 명시적 true | save_step; test_edit_invalidates_review, test_review_requires_boolean |
| S01-R07 | 중단 복원 및 중복 시작 재사용 | create/get; test_resume_after_reopen, test_repeat_create_resumes |
| S01-R08 | 버전 충돌 검출 | expected_revision; test_revision_conflict |
| S01-R09 | 세션 소유자/기기 권한 제한 | _get/create; test_wrong_actor_hidden, test_device_scope |
| S01-R10 | 완료 원자성·멱등성·중복 기기 금지 | complete; rollback/idempotent/registered_device 시험 |
| S01-R11 | 취소 초안 삭제 및 만료 | cancel/purge_expired; cancel/expiry 시험 |
| S01-R12 | REST 계약 및 실행 재현 | api.py, openapi.json, scripts/smoke.py, GitHub Actions |

## 데이터와 저장
sessions: session UUID, actor, device, status, revision, expires(Unix seconds), draft JSON, profile_id. profiles: profile UUID, actor, UNIQUE device, 설정 JSON. completions: UNIQUE session_id, mutation_id, 원 응답 JSON. 프로필 저장과 완료 기록은 BEGIN IMMEDIATE 트랜잭션으로 함께 커밋합니다. 실패하면 전부 롤백합니다.

상태: in_progress → committed 또는 cancelled/expired. 단계를 앞에서 다시 저장하면 그 이후의 모든 값과 동의/확인 단계를 지웁니다. complete는 전 단계 저장이 필요합니다. 같은 mutation_id 완료 재요청은 최초 응답을 반환하고 다른 ID 재요청은 충돌로 거절합니다. 기기 1대당 프로필 1개라는 제한은 참조 구현 정책이며 다중 사용자 지원 시 스키마 변경이 필요합니다.

만료 초안은 조회 시 410으로 거절하며 purge_expired 호출 시 데이터가 지워집니다. 서버 시작 시만 정리합니다. 운영 환경의 주기적 삭제 스케줄은 후속 작업입니다. SQLite 파일 및 백업에서 물리적인 복구 불가능 삭제까지 보장하지 않습니다.

## 연계 및 실패 처리
F2002 사용자 모델은 확정 프로필을, F2004 다중 사용자 모듈은 활성 사용자 지정을, F2005 제품별 정책 모듈은 모델별 설정 제한을 후속 adapter로 처리합니다. TTS·표정·Motion 모듈에는 preferences를 전달하는 계약을 추가합니다. 현재 외부 모듈 호출과 ACK는 없습니다. 등록 committed와 기기 적용 pending은 분리합니다. 다음 부팅에서 프로필을 기기에 반영하는 실제 기능은 S02 범위입니다.

HTTP 401 인증 실패, 403 기기 불허, 404 없는/타인 세션, 409 순서·revision·중복 완료 충돌, 410 만료, 422 입력 검증, 500 내부 오류입니다. 409 revision 충돌은 GET으로 최신 초안을 받은 뒤 사용자에게 차이를 확인시켜 재요청합니다. 타임아웃 시 동일 mutation_id를 재사용합니다. 실제 UI 자동 재시도는 아직 구현하지 않았습니다.

## 완료 검토
현재 자동 시험과 HTTP 스모크 통과는 코드·계약의 검증 증적입니다. S01 Jira 완료는 제품 담당자의 데이터 수집 범위, 소유권/보호자 정책, 실제 기기 capability 및 성능 목표 승인과 API 검토 후 판단합니다. S02 구현 완료나 S03 안전 통과로 해석하지 않습니다.

## Jira T01~T12 실행 체크리스트 연결
| 항목 | 현재 산출물 | 후속 검토/구현 |
|---|---|---|
| T01 사용자 시나리오 | 로컬 소유자 등록 경로 | 보호자·게스트·가족 정책 미확정 |
| T02 최초 실행 | 미등록 시작, 등록 중복 방지, 중단 복원 | 초기화·소유권 이전 정책 |
| T03 기기 연결 | 데모 허용 기기 목록 검사 | 실제 pairing·소유권 증명·재연결 |
| T04 설정 항목 | validate, OpenAPI schemas | 실제 음성 목록·기기 상한 합의 |
| T05 동의 | 목적별 boolean, 거부한 채 완료 | 동의 버전·철회 이력·문안 |
| T06 화면·음성 UX | 순서·수정·재확인 규칙 | 큰 글씨·건너뛰기·미리듣기 UI |
| T07 상태 전이 | in_progress/committed/cancelled/expired | waiting/applying/failed 적용 상태 |
| T08 임시 데이터 | SQLite draft, revision, expires | updated_at·단계 이력·주기적 삭제 |
| T09 API | 시작/조회/저장/완료/취소 구현 | 실서비스 인증·기기 권한 철회 |
| T10 서비스 연결 | 프로필 생성, apply pending | F2002 정식 모델·F2004 사용자·Context adapter |
| T11 오류 복구 | 충돌·중복·취소·만료·DB rollback | 로봇 적용 실패·네트워크 UI |
| T12 인수시험 | 19 자동 시험 및 실제 HTTP 시험 | 첫 대화 적용·실기기 안전 시험 |

현재 자료는 Jira의 전체 완료 조건 중 코드로 검증할 수 있는 부분을 충족합니다. 보호자·게스트·오프라인 사용 경로 및 화면·음성 흐름의 상세 검토는 남아 있으므로 S01 전체 완료를 선언하지 않습니다.
