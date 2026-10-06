# [F2063] 사용 시간 및 부모 통제

Jira: https://lumira077.atlassian.net/browse/KR1-452

보호자 승인 시간·콘텐츠·camera·결제 정책을 앱/로봇에 적용

입력/출력: policy version·time budget·content scope

경계시험: 시간우회·권한 철회·다중앱 충돌

지표: 제한 위반 0건·정책전파·감사추적

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-11/F2063/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

계정/pairing → versioned 설정/상태/알림 → 동의 통화 → 공간 onboarding/부분reset. Epic-01/09/10 서비스·Epic-07/15 공간·Epic-12 lifecycle·Epic-13 권한/회수 연결.

필요 입력/연동: iOS/Android 대상·앱/backend 환경·identity provider·Push/APNs/FCM·TURN/signaling·기기 pairing·동의/권한·설치/공간 환경

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
