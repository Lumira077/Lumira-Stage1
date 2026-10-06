# [F2060] 모바일 앱 계정 및 로봇 연결

Jira: https://lumira077.atlassian.net/browse/KR1-437

계정 인증·일회 pairing·기기 소유권·가족 초대/해제를 구성

입력/출력: account·robot id·pair token ref·owner epoch

경계시험: 토큰 재사용·소유권 변경·분실·권한 상승

지표: pairing 성공률·cross-owner 차단·해제 반영

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-11/F2060/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

계정/pairing → versioned 설정/상태/알림 → 동의 통화 → 공간 onboarding/부분reset. Epic-01/09/10 서비스·Epic-07/15 공간·Epic-12 lifecycle·Epic-13 권한/회수 연결.

필요 입력/연동: iOS/Android 대상·앱/backend 환경·identity provider·Push/APNs/FCM·TURN/signaling·기기 pairing·동의/권한·설치/공간 환경

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
