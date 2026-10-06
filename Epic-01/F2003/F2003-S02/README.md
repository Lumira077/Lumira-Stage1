# F2003-S02 로컬 기억 서비스

[Jira KR1-14](https://lumira077.atlassian.net/browse/KR1-14)

F2002를 직접 호출하는 동의·소유권/활성 프로필 검사, candidate/confirmed CRUD, 단일 slot 대체, 정정·삭제·만료, 검색 인덱스, 멱등/retired 요청, context ticket, 명시적 revoke/grant를 구현했다. 모듈은 표준 라이브러리만 사용하며 f2002-dependency.json이 승인된 F2002 코드의 해시를 확인한다.

```sh
python -c "import memory_service; import unittest; unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'))"
export KER_MEMORY_DEV_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
python -m memory_service --demo-dir demo-data --port 8083
```

CLI는 새 디렉터리에 합성 계정/프로필/장치와 장기 기억 동의를 생성한다. 실제 사용자 동의를 받는 절차가 아니므로 운영에 사용하지 않는다. API 127.0.0.1:8083은 Bearer token 필수. body/profile/actor를 임의로 지정하지 못한다. POST /memories는 data와 mutation_id, 확인은 revision/mutation_id, 수정은 content/revision/mutation_id, 삭제는 revision, capture는 utterance/source_ref/mutation_id, search는 query, privacy는 confirmed:true를 사용한다.

Python: Service(path,ProfilePolicy(profiles)); create/capture/get/list/confirm/correct/delete/delete_all/search/prepare/release_context/revoke/grant/synchronize/sync_status. 평문 SQLite, 단일 동기 프로세스·개발 인증 전용이다. sync_status는 클라우드 동의를 확인해도 status:not_connected/payload_exported:false만 반환하며 내용을 전송하지 않는다.

F2002 외부 변경은 synchronize를 호출하고 운영에서는 즉시 철회 이벤트·epoch를 연결해야 한다. F2002와 F2003의 두 DB 변경은 분산 트랜잭션이 아니다. 제공 revoke는 먼저 기억 purge/영구 차단, 다음 F2002 갱신; 실패 시 차단 유지. 명시적 grant만 차단을 해제하며 옛 기억/옛 요청을 복원하지 않는다.
