# F2002-S02 핵심 프로필 서비스

[Jira KR1-9](https://lumira077.atlassian.net/browse/KR1-9)

SQLite 프로필 CRUD·목록·선호 초기화·revision·멱등 요청·활성 사용자 전환·적용 ACK 재시도·F2001 import bridge를 구현한다. 데이터 스키마 1. 부모 S01의 소스 SHA-256을 dependencies.json으로 확인한다.

```sh
python -c "import profile_service; import unittest; unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'))"
# 개발 토큰은 터미널에서 생성해 환경에만 공급한다. 출력하거나 저장소에 올리지 않는다.
export KER_PROFILE_DEV_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
python -m profile_service.api --db profiles.sqlite3 --port 8082
```

HTTP는 127.0.0.1:8082에 바인딩한다. Authorization: Bearer 환경 토큰, Content-Type: application/json. POST는 data/mutation_id, PATCH는 changes/revision/mutation_id, DELETE는 revision을 받는다. api.py의 실제 소켓 시험은 인증 실패·생성·수정·조회·삭제를 검증한다. 외부 사용자 인증 서버가 아니다.

Python 호출: Service(path).create(actor,data,key); get/list/update/reset/delete; provision_device는 신뢰된 개발 구성만; activate(pid,actor,device,revision); apply(application_id,actor,outputs). identity와 authorized_subjects는 인증된 상위 서비스에서만 공급해야 한다.

bridge.import_onboarding(target,source,sid,actor,authorized_subjects)에서 source는 F2001 Service 인스턴스다. 세션·프로필 소유권과 committed 상태를 확인한 후 snapshot을 복사한다. 자동 동기화가 아니며 import의 DB 간 원자성·여러 프로세스 경쟁은 운영 통합 과제다. SQLite DB는 평문이므로 운영 암호화·보존·키 관리가 필요하다.
