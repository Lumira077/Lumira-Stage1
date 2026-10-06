# [F2049] 비접촉 rPPG 생체신호 측정

Jira: https://lumira077.atlassian.net/browse/KR1-380

rPPG capture 품질·움직임/조명 평가와 품질 미달 시 값 보류를 구성

입력/출력: ROI·signal quality·duration·estimate·timestamp

경계시험: 가림·motion·조명·피부톤·frame drop

지표: 참조센서 비교오차·측정가능률·quality reject

구현 범위: partial_offline_utility; 공통 utility: wellness_value. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-09/F2049/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

일정/정서 지원 → 후보 이벤트/측정 품질 → 보호자 전달/ACK → 동의한 리포트. Epic-02 대화·Epic-03/05 인지·Epic-11 앱·Epic-12 관제·Epic-13 개인정보 연결. rPPG/정서/낙상은 미검증 후보/참고정보이며 진단/처방/응급대응 보장을 주장하지 않는다.

필요 입력/연동: 동의한 사용자/보호자·알림 채널 계정/수신ACK·camera/참조측정기·검증dataset·전문가 검토·운영 escalation

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
