# [F2048] 복약 및 일정 알림

Jira: https://lumira077.atlassian.net/browse/KR1-375

사용자 승인 복약/일정의 timezone 반복·snooze·확인·재알림을 구현

입력/출력: schedule id·local time·timezone·occurrence·ack

경계시험: DST·시계변경·중복전달·연결 단절

지표: 중복 알림 0건·누락률·도달시간

구현 범위: partial_offline_utility; 공통 utility: Reminder. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-09/F2048/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

일정/정서 지원 → 후보 이벤트/측정 품질 → 보호자 전달/ACK → 동의한 리포트. Epic-02 대화·Epic-03/05 인지·Epic-11 앱·Epic-12 관제·Epic-13 개인정보 연결. rPPG/정서/낙상은 미검증 후보/참고정보이며 진단/처방/응급대응 보장을 주장하지 않는다.

필요 입력/연동: 동의한 사용자/보호자·알림 채널 계정/수신ACK·camera/참조측정기·검증dataset·전문가 검토·운영 escalation

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
