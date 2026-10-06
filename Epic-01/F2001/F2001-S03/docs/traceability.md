# Jira KR1-5 요구사항 추적

| 시험 | 요구사항 | 수행한 소프트웨어 범위 | 실기 상태 |
|---|---|---|---|
| ONB-01 | 신규 등록 | 가상 적용·텍스트 첫 인사 | not_run |
| ONB-02 | 보호자 지원 | 승인된 guardian fixture | not_run |
| ONB-03 | 게스트 | 프로필 없음·분리된 출력 scope | not_run |
| ONB-04 | 동의 거부 | permissions false | not_run |
| ONB-05 | 설정 정확성 | 저장 Context와 가상 ACK 설정 대조 | not_run |
| ONB-06 | 단계별 중단·복구 | 서비스 DB 재개·미커밋 rollback; 실제 전원 차단 아님 | not_run |
| ONB-07 | 연결 단절·재연결 | 가상 기기 연결 상태; 실제 네트워크 아님 | not_run |
| ONB-08 | 앱 재접속 | 권한 재확인·저장 초안 재조회 | not_run |
| ONB-09 | 반복 완료·첫 인사 | 3회 완료·논리 첫 인사 1회 | not_run |
| ONB-10 | 비인가 접근 | 조회·수정·완료 거절 | not_run |
| ONB-11 | 만료·취소 | 재사용 거절·초안 정리 | not_run |
| ONB-12 | DB 실패 | 저장 trigger 실패·부분 저장 없음 | not_run |
| ONB-13 | 모듈 실패·재시도 | 모듈별 실패·프로필 유지·재시도 | not_run |
| ONB-14 | 미리보기 취소·정지 | queued 출력 폐기; 물리 동작 중 stop 아님 | not_run |
| ONB-15 | 재부팅 후 출력 억제 | 소프트웨어 재시작 시 이전 출력 비활성화 | not_run |
| ONB-16 | 오프라인 경로 | 외부 클라우드 호출 없는 텍스트 인사 | not_run |

| Jira 작업 | 코드/결과 | 미수행 또는 검토 사항 |
|---|---|---|
| T01 환경 | dependency.json, report.environment | 실기/펌웨어/제어모델 null |
| T02 연결 | adapters.py, HTTP guarded 시험 | 실제 STT/TTS/제어 연결 |
| T03 정상 | ONB-01~04 | 실기 본인/보호자 권한 |
| T04 정확성 | ONB-05, applied_settings | 실제 음색·출력·관절 |
| T05 지연 | runner.benchmark, 3경로 각100회 | 네트워크·실제 음성 시작 |
| T06 복구 | ONB-06~08,15 | 실제 전원 저장 전/중/후·구동 중 차단 |
| T07 무결성/권한 | ONB-09~12 | 운영 인증·개인정보 보호 |
| T08 출력 제어 | Broker, test_safety | 실제 음향·관절·정지시간·센서장애 |
| T09 재시험 | tests.txt와 CI 커밋 | 결함과 수정은 Jira 검토 시 연계 |
| T10 상위 연결 | report scenarios, 이 추적표 | Q1 검증/R1 인수 승인 대기 |
