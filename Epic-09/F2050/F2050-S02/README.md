# [F2050-S02] 낙상 및 이상행동 감지 기능·콘텐츠 Package 구현

Jira: https://lumira077.atlassian.net/browse/KR1-387

서비스 로직·콘텐츠/화면·대화/연동 Package 구현: pose/time context 기반 낙상 후보와 사용자 확인·오탐 억제를 구성

데이터: event id·pose sequence·confidence·confirm state

검증: 앉기/눕기·가림·무반응·sensor offline

지표: 오탐/미탐·검출 지연·개인정보 노출

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
