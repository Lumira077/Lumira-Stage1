# F2003-S01 계약·설계

[Jira KR1-13](https://lumira077.atlassian.net/browse/KR1-13)

```sh
python -m memory_contract examples/memory.json
python -c "import memory_contract; import unittest; unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'))"
```

memory_contract는 엄격한 데이터 검증, 민감·지시 패턴 필터, 명시적 선호 발화 규칙 추출, 정규화 문자열 검색 점수를 제공한다. 데이터·API·상태·권한·오류는 design.md/openapi.json에 정의했다. 계약 시험 19개. 실제 LLM·운영 설계 승인과 포괄적인 민감정보 탐지는 미완료다.
