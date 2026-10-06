# [F2073] 인증·권한·기기 신뢰

Jira: https://lumira077.atlassian.net/browse/KR1-539

사용자/기기 인증·tenant/owner scope·RBAC·세션 revoke를 구성

입력/출력: principal·role·device/tenant·token ref·epoch

경계시험: cross-tenant·replay·expired·owner 변경

지표: 권한우회 0건·revoke 지연·session 감사

구현 범위: partial_offline_utility; 공통 utility: scoped_access. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-13/F2073/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

목적별 동의/epoch·최소metadata → 인증/암호화/Secret/감사 → local E-stop/MCU·기구/torque 보호. Epic-01~16 전체 서비스/제어의 공통 gate. ASVS는 앱 보안 검토 참조이며 물리 안전/법규 인증 증거를 대체하지 않는다.

필요 입력/연동: 제품 threat/hazard model·전문 보안/개인정보 검토·KMS/PKI·인증 서버·독립 safety HW·실제 정지feedback·시험/승인 기준

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
