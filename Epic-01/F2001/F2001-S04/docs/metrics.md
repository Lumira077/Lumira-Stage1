# 운영지표·로그 계약

집계 코호트는 [start,end)에 시작한 고유 세션이다. as_of까지 후속 이벤트를 관찰하되 시작 이벤트의 버전·mode를 유지한다. start < end <= as_of, UNIX 초, 경로 self/guardian/guest/unknown 및 버전·mode 필터를 사용한다. 운영 일별 보고서는 하루 단위 구간마다 aggregate를 호출한다. 예시는 고정 시간의 합성 데이터다.

| 지표 | 분자 / 분모 |
|---|---|
| 등록 완료 | 등록 committed 고유 self/guardian / 시작 self/guardian |
| 이용 준비 | 첫 greeting ready 고유 세션 / 전체 시작 세션(게스트 포함) |
| 완료 시간 | 첫 ready - 시작, 초, median p50 / nearest-rank p95; 미완료 제외 |
| 단계 이탈 | 최신 단계 진입 후 미진행 / 관찰창 1800초 이상 확보한 진입 세션; 정상 취소 제외 |
| 재개 성공 | 성공 응답 attempt_id / 재개 요청 attempt_id |
| 모듈 적용 실패 | 실패 attempt_id / 실제 적용 시도 attempt_id; 중복 ACK 조회 제외 |
| 중복 등록 | duplicate_registration 고유 세션 수 |
| 도움 요청 | support_requested 고유 세션 / 전체 시작 세션 |

분모가 0이면 값은 null이며 Dashboard는 N/A로 표시한다. 중복된 start/complete/ready/support는 안정 키로 한 번만 저장한다. unknown은 등록 분모에서 제외하고 별도로 조사한다. 동의 거부는 오류가 아니다. 정상 취소는 따로 집계한다. 오류 횟수와 세션 이탈 수는 서로 다른 단위다. 모듈 적용 시도 20건 이상 중 실패율 10% 이상은 제안 경보, 중복 등록은 blocker 경보이며 운영 임계치는 미승인이다.

로그: HMAC 가명 세션·이벤트 ID, 시간, 코드 버전, mode, 경로, 허용된 이벤트·단계·모듈·오류 코드·지연·시도 ID만 저장한다. 이름/선호 호칭/대화 원문/Wi-Fi 정보/토큰/동의 전문 및 임의 필드는 거부한다. SQLite 로그는 암호화 저장소가 아니며 파일 접근권한과 저장 암호화는 운영 구성 책임이다. 키는 외부 공급한 32바이트 이상 비밀이며 저장하지 않는다. 키 교체 시 동일 세션 코호트의 단절을 검토해야 한다. 보존 기간 승인 후 `purge_before(timestamp)`를 호출하고 감사 증적을 보관한다. 실제 개인정보 삭제 요청의 매핑과 서비스 저장소까지의 삭제는 별도 운영 통합 대상이다.
