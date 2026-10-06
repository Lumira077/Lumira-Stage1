# [F2048-S04] 복약 및 일정 알림 운영·지표·Release 전환

Jira: https://lumira077.atlassian.net/browse/KR1-379

콘텐츠갱신/상담/신고·보유/삭제·KPI·Release/중단: 사용자 승인 복약/일정의 timezone 반복·snooze·확인·재알림을 구현

데이터: schedule id·local time·timezone·occurrence·ack

검증: DST·시계변경·중복전달·연결 단절

지표: 중복 알림 0건·누락률·도달시간

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
