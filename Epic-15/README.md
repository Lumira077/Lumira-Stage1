# EPIC-15 Stage 2~4 스마트 공간·가사·생활 보조

https://lumira077.atlassian.net/browse/KR1-655

11 Features, 44 existing Sub-tasks.

Stage2 공간/IoT onboarding → 승인 intent/Scene → Stage3 이동조작 → Stage4 높이/전도/접근성/장기 임무. Epic-07 지도·Epic-08 조작·Epic-11 앱·Epic-13 안전·Epic-16 HW 연결.

현재 명세/검토 도구·일부 로컬 utility입니다. 실제 HW·production서비스·Pilot·법률/재무 승인·외부 실행은 미완료입니다.

- [[F2082] 높이 조절 본체](F2082/README.md): Stage4 높이 조절 actuator·absolute position·limit·과부하·끼임 구조를 설계
- [[F2083] 생활 공간 의미 지도](F2083/README.md): 방/가구/물체/보관장소/금지구역의 의미지도와 revision을 구성
- [[F2084] 가사 작업 계획](F2084/README.md): 가사 요청을 자원/안전 precondition·navigation/manipulation 단계로 분해
- [[F2085] 스마트홈 기기 연동](F2085/README.md): 승인 기기 목록의 상태조회·제어·결과확인을 Stage2부터 구성
- [[F2086] 장애인·고령자 접근성 보조](F2086/README.md): 시각/청각/운동 접근성 모드·지원 요청·비상 중단 UX를 구성
- [[F2087] 장기 자율 생활 서비스](F2087/README.md): 장기 임무·충전/점검·장애 복구·서비스 중단을 운영계획과 연결
- [[F2137] Stage4 가변 높이 범위·승강 Mechanism](F2137/README.md): 700~1200mm 구상 목표의 승강·limit·position·구조를 설계 검증
- [[F2138] 높이별 무게중심·전도·작업영역 안전](F2138/README.md): 높이/하중/팔 자세별 CoM·support polygon·속도제한을 구성
- [[F2147] Matter·Wi-Fi Device Discovery·Gateway](F2147/README.md): Matter/Wi-Fi commissioning·discovery·capability·gateway를 설계
- [[F2148] 자연어 IoT 제어·실행 확인](F2148/README.md): 자연어를 allowlisted IoT intent로 변환하고 민감명령 확인·receipt를 구성
- [[F2149] Scene 자동화·공간 위치 기반 제어](F2149/README.md): Scene의 시간/방/사용자/권한 조건·순차 실행·partial failure를 구성
