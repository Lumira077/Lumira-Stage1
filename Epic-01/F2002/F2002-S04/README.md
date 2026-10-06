# F2002-S04 사용자 검증·운영지표·Release

[Jira KR1-11](https://lumira077.atlassian.net/browse/KR1-11)

```sh
python -m profile_ops.runner --out results --samples 100
python -m profile_ops.runner --out results --require-release
```

첫 명령은 소프트웨어 시험 성공 시 0, 두 번째는 Release 미완료이므로 1을 반환한다. `results/dashboard.html`은 정적 개발 검토 화면이다. 운영지표는 기간별 생성·수정·활성화·적용 시도·실패·삭제 이벤트 횟수와 적용 실패율이다. 프로필 이름·ID·대화 원문은 이벤트에 남기지 않는다. 고유 사용자·세션 성공률, 운영 SLA/경보 수집은 추가 구현 대상이다.

`user-study.md`, `runbook.md`, `manifest.json` 참조. 실제 참가자 0명, 실제 로봇/운영 복귀 미수행. Release 평가기에는 승인 권한 시스템이 연결되지 않아 항상 blocked를 유지한다. 테스트 데이터와 observed 라벨만으로 승인하지 않는다.
