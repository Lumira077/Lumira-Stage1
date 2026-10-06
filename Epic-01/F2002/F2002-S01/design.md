# 요구사항·데이터·API 설계 v1

근거: Jira KR1-7~11의 단계별 범위, 기존 F2001 계약, 첨부 AI로봇사업 문서의 사용자 인증·프로필 기반 개인화·데이터 무결성 방향. 구체적인 필드·임계치·권한 모델은 이번 개발 제안이며 기존 Jira에 없는 내용을 확정 요구로 간주하지 않는다.

## 시나리오와 완료조건

| 항목 | 입력·출력·기준 |
|---|---|
| 본인/보호자 프로필 | 신뢰된 actor·subject 권한 목록; 다른 owner 조회는 NOT_FOUND |
| 프로필 수정 | language/nickname/preferred_name/purpose/preferences/consent, revision, mutation_id; 새 revision 반환 |
| 기본 선호 복원 | 선호만 DEFAULTS로 변경, 언어·호칭·동의 보존 |
| 활성 사용자 전환 | 소유 장치·프로필·revision 확인; generation 증가; 이전 요청 무효화 |
| 선택 동의 철회 | consent 전체 객체로 변경; 이전 적용 무효화; 새 인식 permissions 전달 |
| 프로필 삭제 | 프로필·멱등 기록·ACK·적용 제거, 장치 연결 해제, import tombstone 보존 |
| F2001 가져오기 | 승인된 committed 비게스트 세션; 한 번 복사, 삭제 후 같은 source 재import 거부 |
| 단절·정지·재시도 | 이전 generation 요청 거부, 재활성화 필요; 부분 성공 ACK 재사용은 동일 프로필 버전/장치 generation 내에서만 |

## 데이터

언어 ko-KR/en-US; nickname/preferred_name 1~40자, 제어문자 금지; purpose companion/education/care/home. preferences는 voice_id(device_default/demo_voice_a), speech_rate 0.7~1.3, volume 0~100, expression_level/gesture_level 정수 0~3. 선택 동의 long_term_memory/conversation_storage/biometric_identity/cloud_transfer는 모두 bool, policy_version prototype-2026-10-v1. 기본 음량 20, 속도 1, 표현/제스처 1, 장치 기본 음성. 중첩 수정은 객체 전체 교체이며 임의 필드/생체/건강/대화 데이터 금지.

프로필 ID는 무작위 32자리 hex, revision 양의 정수다. device generation은 설정 적용의 전환 장벽이다. mutation에는 요청 SHA-256만 저장하고 원문/과거 응답 snapshot을 남기지 않는다. 현재 revision보다 오래된 멱등 응답 재전송은 IDEMPOTENCY_SUPERSEDED로 거부한다. SHA-256 digest도 접근 보호가 필요한 내부 데이터다.

## API와 오류

개발 HTTP: GET/POST /profiles; GET/PATCH/DELETE /profiles/{id}. Bearer token은 고정 로컬 Demo actor에 매핑. 요청 body에는 actor/권한/장치 provisioning을 받지 않는다. Content-Type JSON, 최대 16KiB, loopback만 허용. TLS·다중 계정은 운영 통합 대상이다. activate/apply/reset/import는 Python 서비스 API다; 현재 HTTP로 노출하지 않는다.

401 UNAUTHORIZED; 404 NOT_FOUND(미존재/다른 owner 동일); 409 REVISION_CONFLICT/IDEMPOTENCY_CONFLICT/IDEMPOTENCY_SUPERSEDED/STALE_APPLICATION/DEVICE_NOT_READY/INCOMPATIBLE_SCHEMA; 422 INVALID_INPUT/INVALID_REVISION/UNSUPPORTED_LANGUAGE/UNSUPPORTED_VOICE/POLICY_VERSION_MISMATCH; 413 BODY_TOO_LARGE. 저장 오류 시 트랜잭션 rollback. 모듈 오류 시 저장 프로필을 유지하고 적용 실패·재시도 상태 반환.

## 통합·안전

F2002 context는 버전·프로필 ID·revision·언어·호칭·목적·선호·권한을 정의한다. 각 모듈은 최소 필드만 받아야 한다. 모의 수신기는 대화에 언어/목적, 인식에 permissions, 출력에 제한된 선호만 전달한다. 실제 STT/TTS/ROS2/모터 동작 어댑터는 미구현. 실제 장치에서는 설정 적용과 현재 권한 확인을 출력 직전에 다시 검사하고 안전 정지·ACK 원장·outbox·시간초과·일관성 프로토콜을 검증해야 한다. 현재 구현은 로컬 동기 호출만 지원한다.
