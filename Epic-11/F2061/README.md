# [F2061] 로봇 상태 및 알림 조회

Jira: https://lumira077.atlassian.net/browse/KR1-442

상태 TTL·알림 이력/확인·중복 억제와 offline 표시를 구성

입력/출력: status stamp·battery·error·alert id·receipt

경계시험: stale 상태·중복 push·offline·권한 없음

지표: 상태 freshness·알림 지연·중복률

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-11/F2061/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

계정/pairing → versioned 설정/상태/알림 → 동의 통화 → 공간 onboarding/부분reset. Epic-01/09/10 서비스·Epic-07/15 공간·Epic-12 lifecycle·Epic-13 권한/회수 연결.

필요 입력/연동: iOS/Android 대상·앱/backend 환경·identity provider·Push/APNs/FCM·TURN/signaling·기기 pairing·동의/권한·설치/공간 환경

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
