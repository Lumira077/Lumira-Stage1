# [F2151] Stage2 User & Space Onboarding App

Jira: https://lumira077.atlassian.net/browse/KR1-462

Stage2 계정/로봇/네트워크/공간/사용자/IoT 온보딩 재개 흐름을 구성

입력/출력: wizard version·step·map ref·owner epoch

경계시험: 중단·재개·기기 복구·로봇과 상태 불일치

지표: 필수 설정 완료율·복구 일치·동의 보존

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-11/F2151/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

계정/pairing → versioned 설정/상태/알림 → 동의 통화 → 공간 onboarding/부분reset. Epic-01/09/10 서비스·Epic-07/15 공간·Epic-12 lifecycle·Epic-13 권한/회수 연결.

필요 입력/연동: iOS/Android 대상·앱/backend 환경·identity provider·Push/APNs/FCM·TURN/signaling·기기 pairing·동의/권한·설치/공간 환경

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
