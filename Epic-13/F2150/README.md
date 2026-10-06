# [F2150] 민감 IoT 기기 권한·재확인·감사

Jira: https://lumira077.atlassian.net/browse/KR1-574

도어/락 등 민감 IoT의 user/device scope·재확인·감사·취소를 구성

입력/출력: device·action·one-time confirmation·scope·expiry

경계시험: 낯선명령·replay·권한변경·원격취소

지표: 미승인 실행 0건·결과 감사·취소반영

구현 범위: partial_offline_utility; 공통 utility: scene_proposal. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-13/F2150/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

목적별 동의/epoch·최소metadata → 인증/암호화/Secret/감사 → local E-stop/MCU·기구/torque 보호. Epic-01~16 전체 서비스/제어의 공통 gate. ASVS는 앱 보안 검토 참조이며 물리 안전/법규 인증 증거를 대체하지 않는다.

필요 입력/연동: 제품 threat/hazard model·전문 보안/개인정보 검토·KMS/PKI·인증 서버·독립 safety HW·실제 정지feedback·시험/승인 기준

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
