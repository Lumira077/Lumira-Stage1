# F2208-S01

Jira: https://lumira077.atlassian.net/browse/KR1-59

- F2002 권위 프로필·F2003 확인 기억·F2004 활성 사용자의 권한 경계와 동의 epoch 계약 정의
- ContextItem: owner, id, text, confirmed, expires, cloud_share; ContextPacket: epoch, refs, scope, policy_revision의 필수값·민감도·보존기간·권한·revision/epoch를 표로 정의한다.
- LocalContext.search(actor,query,cloud=False) → bounded references; F2003 release ticket 재검증 후 운영 출력의 정상·오류·취소·stale 입력 계약 및 시험 데이터 분할을 명세화한다.

산출물: 요구사항·데이터/인터페이스 계약·예외표·시험 기준

상위 Feature 완료조건: 권한별 조회가 분리되고 미승인 기억이 Cloud로 전달되지 않으며 로컬 평가셋 검색 목표를 충족한다.

현재 제한: 현재 합성 fixture lexical 검색. 실제 F2003 ticket·동의 epoch·벡터/임베딩·운영 암호화/삭제 연동은 추가 구현

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
