# EPIC-13 보안·개인정보·제품 안전

https://lumira077.atlassian.net/browse/KR1-528

11 Features, 44 existing Sub-tasks.

목적별 동의/epoch·최소metadata → 인증/암호화/Secret/감사 → local E-stop/MCU·기구/torque 보호. Epic-01~16 전체 서비스/제어의 공통 gate. ASVS는 앱 보안 검토 참조이며 물리 안전/법규 인증 증거를 대체하지 않는다.

현재 명세/검토 도구·일부 로컬 utility입니다. 실제 HW·production서비스·Pilot·법률/재무 승인·외부 실행은 미완료입니다.

- [[F2071] 사용자 동의 및 개인정보 설정](F2071/README.md): 목적별 consent version·철회·보유·삭제 전파를 구성
- [[F2072] 전송·저장 데이터 암호화](F2072/README.md): TLS/mTLS·저장 암호화·key lifecycle·rotation/복구를 설계
- [[F2073] 인증·권한·기기 신뢰](F2073/README.md): 사용자/기기 인증·tenant/owner scope·RBAC·세션 revoke를 구성
- [[F2074] API 키 및 비밀정보 중앙 관리](F2074/README.md): Secret 참조만 배포하고 최소권한·rotate·유출 대응을 설계
- [[F2075] 감사 로그 및 이상 접근 탐지](F2075/README.md): 최소 감사 event·무결성/시간·보존·접근 이상 경보를 구성
- [[F2076] 관절·주행 비상 정지](F2076/README.md): 관절/주행 stop latch·local 우선순위·물리 ACK·검토 reset을 연결
- [[F2139] 경량 Arm·연질 외장·라운드 Mechanical Safety](F2139/README.md): 경량 팔·연질 외장·라운드·끼임 간격·낙하 구조를 기구로 설계
- [[F2140] Torque·Current 충돌 감지 및 가변 제한](F2140/README.md): torque/current·근접·속도에 따른 충돌 후보 및 제한도를 구성
- [[F2141] Safety MCU 독립 Torque 차단·검증](F2141/README.md): Safety MCU의 독립 watchdog·torque disable·feedback·reset을 검증
- [[F2150] 민감 IoT 기기 권한·재확인·감사](F2150/README.md): 도어/락 등 민감 IoT의 user/device scope·재확인·감사·취소를 구성
- [[F2164] Fleet 최소 Metadata·Privacy·Security Policy](F2164/README.md): fleet 최소 metadata와 목적/보유/접근·raw 비전송을 구성
