# F2002-S01 요구사항·데이터·인터페이스 설계

[Jira KR1-8](https://lumira077.atlassian.net/browse/KR1-8) · 상위 F2002

`profile_contract`는 Python 실행 가능한 검증 소스다. 프로필 JSON 및 수정 요청·선택 동의·F2001 변환·모듈 context 계약을 정의한다.

```sh
python -m profile_contract examples/profile.json
python -c "import profile_contract; import unittest; unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'))"
```

`design.md`, `openapi.json` 참조. 실제 사용자/보호자 권한·기종별 제한은 승인 대상이다. 건강·감정·생체 원본·대화 기록은 이 프로필에 넣지 않는다. 입력 계약과 API 설계는 구현된 개발 범위이며 실제 운영 설계 승인은 미완료다.
