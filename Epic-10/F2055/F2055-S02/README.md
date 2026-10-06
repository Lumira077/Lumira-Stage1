# [F2055-S02] 퀴즈·학습 대화 기능·콘텐츠 Package 구현

Jira: https://lumira077.atlassian.net/browse/KR1-413

서비스 로직·콘텐츠/화면·대화/연동 Package 구현: 검수 문제은행의 난이도·힌트·정답 feedback·중단을 구성

데이터: question id·difficulty·answer·attempt·hint

검증: 오답 연속·ASR 불확실·금지내용·시간초과

지표: 정답처리 정확성·학습흐름·피로/중단

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
