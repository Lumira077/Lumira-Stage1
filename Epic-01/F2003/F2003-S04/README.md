# F2003-S04 운영·사용자 검증·복원·Release

[Jira KR1-16](https://lumira077.atlassian.net/browse/KR1-16)

```sh
python -m memory_ops.runner --out results --samples 100
python -m memory_ops.runner --out results --require-release
```

첫 명령은 개발 소프트웨어/fixture gate 성공 시0, 두 번째는 Release 미완료로1이다. 결과는 표준 라이브러리로 재현할 수 있다. 실제 연구/모델/로봇/클라우드/운영복귀/승인이 없으므로 release_ready:false를 강제 유지한다.

metrics는 기간별 committed 연산 이벤트 수이며 전체 요청 실패·유실·고유 참가자 성공률을 나타내지 않는다. 실제 운영 모니터링 연결·버전/mode/장치별 수집·삭제/철회 지연·경보/SLO는 승인·추가 구현 대상이다. Dashboard는 정적 스냅샷이다.

RestoreLab은 개발 표식 디렉터리·고정 파일명·symlink 거부·스키마1을 사용한다. 최신 외부 원장의 prefix가 snapshot 원장과 일치해야 하고 이후 삭제/철회/폐기 요청/정정 기록을 재적용한다. 정정 이후의 오래된 기억은 제거하며 backup 이후 신규·정정 내용 전체를 재구성하지 않는다. 모든 준비 ticket을 제거한다. 실제 최신 원장 진위/완전성·외부 F2002/클라우드/벡터·물리 소거·운영 DB복귀는 승인 대상이다.

[user-study.md](user-study.md) · [운영·배포·복귀](runbook.md) · [manifest](manifest.json)
