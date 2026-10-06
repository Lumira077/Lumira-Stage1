# 요구사항·데이터·인터페이스 설계 v1

기준은 Jira KR1-12~16의 상세 Description이다. 로컬 규칙·문자열 검색으로 수직 실행 흐름을 먼저 검증한다. 외부 LLM/프롬프트·임베딩/벡터·실제 클라우드/로봇은 후속 어댑터 대상이며 모의 성공을 해당 완료조건으로 인정하지 않는다.

## 상태·저장 정책

candidate → 사용자 확인 → confirmed → 정정/대체/삭제/만료. 모든 후보는 확인이 필요하다. candidate는 최대 7일, 확인은 기본30일·최대365일 제안. confirmed만 검색 인덱스를 갖는다. 같은 kind/topic의 새 확인은 이전 기억을 superseded로 바꾸고 content와 검색 인덱스를 제거한다. 독립 주제는 다른 topic으로 구분한다. 자동으로 F2002 선호를 덮어쓰지 않는다.

대화 원문 저장과 장기 기억 저장은 서로 다른 동의다. raw utterance는 transient 추출 입력이며 DB/로그에 남기지 않는다. 후보 내용과 source_ref만 저장한다. 민감/악성 지시 패턴은 기본 거부하고 일반 대화에서 사실·건강·관계·약속을 추측해 저장하지 않는다. fact/promise는 구조화 후보 입력만 지원하며 실행 권한이 아니다.

## 데이터

| 필드 | 계약 |
|---|---|
| memory_id/profile_id/source_ref | 무작위 32자리 hex 또는 신뢰된 서비스의 opaque 식별자 |
| owner | 인증된 상위 서비스에서 공급, HTTP body의 actor 지정 금지 |
| kind | preference/fact/promise |
| topic | 영문 소문자 시작 slug, 1~40자, kind와 함께 단일 기억 slot |
| content | 1~400자, NFKC 정규화, 제어·보이지 않는 format 문자 금지 |
| confidence | 유한 숫자 0..1, 사용자 확인/정정 후1; 모델 확률 보정값 아님 |
| state/revision | candidate/confirmed/superseded, 양의 정수 revision |
| created/updated/expires | UNIX 초, 유효기간 도달 시 읽기/검색에서 제외하고 정리 |
| ttl_seconds | 정수60..31536000, candidate는604800 이하로 제한 |

요청 fingerprint는 내부 SHA-256이며 원문 과거 응답은 보관하지 않는다. 삭제·철회·만료한 요청은 actor/profile/key 기반 해시를 retired_keys에 남겨 오래된 저장 요청 재전송을 거부한다. 삭제/정정·대체·철회 원장에는 내용 없이 sequence·operation·가명 profile/memory 또는 폐기 key token·시간을 남긴다. 메타데이터도 접근 보호·보존 정책 대상이다. SQLite 논리 삭제는 파일의 물리 완전 소거를 보장하지 않는다.

## 권한·F2002

ProfilePolicy가 실제 F2002 Service.get/device를 호출해 소유권·활성 프로필·현재 동의를 확인한다. 얼굴/STT 결과로 권한을 부여하지 않는다. 보호자는 F2002에서 소유권을 가진 대상 프로필 범위에만 접근한다. 실제 보호자 관계 증명은 F2002 운영 인증 과제다. 게스트는 유효한 지속 프로필이 없으므로 접근 불가.

삭제는 동의가 꺼지거나 프로필이 비활성인 경우에도 인증된 소유자에게 허용한다. 다른 actor의 실패는 피해자의 기억을 purge하지 않는다. 외부 프로필 삭제/철회는 synchronize 또는 다음 호출에서 정리한다. 즉시 이벤트·consent epoch·원자성은 추가 운영 연동 대상이다.

## context·검색

정규화 substring 또는 bigram Jaccard≥0.25, 최신시각/ID로 안정 정렬, 결과1..10개. 조회는 원문과 출처를 제공한다. prepare는 text 없는30초 ticket과 memory/revision 참조만 보관한다. release_context는 최신 인증 stamp와 memory revision을 재확인하고 ticket을 한 번만 소비한다. 출력 context는 reference_data와 빈 executable_actions다. Dialogue bridge는 명시적 private_output_confirmed만 받고 실제 발화/동작을 실행하지 않는다. 외부 LLM에 전달된 문자열이 지시로 해석되지 않는지는 별도 실제 모델 시험 대상이다.

## API·오류

HTTP는 token→서버 고정 actor/profile/device로 매핑하고 loopback만 사용한다. GET/POST /memories, GET/PATCH/DELETE /memories/{id}, POST /memories/{id}/confirm, POST /capture, POST /search, POST /privacy/delete-all|revoke|grant. 인증 token·권한·프로필·device provisioning은 요청 body로 받지 않는다. JSON16KiB 이하, no-store, 요청 로그 없음.

401 UNAUTHORIZED; 403 MEMORY_CONSENT_REQUIRED/SCOPE_REGRANT_REQUIRED/CLOUD_CONSENT_REQUIRED/PRIVATE_OUTPUT_CONFIRMATION_REQUIRED; 404 NOT_FOUND(미존재/외부 사용자 동일); 409 REVISION_CONFLICT/IDEMPOTENCY_CONFLICT/IDEMPOTENCY_SUPERSEDED/PROFILE_NOT_ACTIVE/STALE_CONTEXT; 410 RETIRED_REQUEST; 422 INVALID_INPUT/SENSITIVE_MEMORY_FORBIDDEN/INSTRUCTION_MEMORY_FORBIDDEN; 500 INTERNAL_ERROR. 저장/인덱스 같은 트랜잭션, 실패 rollback; 기억 장애 fallback은 빈 기억과 오류 코드.

## 검증

S01 입력/필터/추출, S02 CRUD/권한/동의/멱등/HTTP/인덱스 원자성, S03 실제 F2002·대화 context/실패/유출·지시 차단 fixture, S04 원장·복원·운영/Release. 소형 fixture 품질100%는 해당 사례에 한정된다. 경로별100회 p95≤500ms는 로컬 개발 초기 제안이며 실제 장치/모델의 수용 기준이 아니다.
