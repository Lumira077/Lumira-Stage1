# EPIC-08 Stage 3 5-Finger 조작 및 심부름

https://lumira077.atlassian.net/browse/KR1-318

11 Features, 44 existing Sub-tasks.

팔/손 HW·물체 pose → 파지/force/slip → 한손/양손·협조 → 심부름. Epic-05 인지·Epic-06 제어·Epic-07 이동·Epic-13 안전·Epic-16 HW 연결.

현재 명세/검토 도구·일부 로컬 utility입니다. 실제 HW·production서비스·Pilot·법률/재무 승인·외부 실행은 미완료입니다.

- [[F2042] Dynamixel 기반 다관절 팔 제어](F2042/README.md): DYNAMIXEL joint mapping·profile·limits·measured feedback와 trajectory 실행을 연결
- [[F2043] 5-Finger 손가락 독립 제어](F2043/README.md): 5개 손가락의 독립 joint/synergy 명령과 force·접촉 제한을 구성
- [[F2044] 조작 대상 물체 인식 및 자세 추정](F2044/README.md): RGB-D 기반 물체 종류·6D pose·uncertainty와 파지 후보를 구성
- [[F2045] 안전 파지 및 놓기](F2045/README.md): 접근→접촉→파지→운반→지지면 확인→놓기 상태를 구성
- [[F2046] 간단 심부름 임무 실행](F2046/README.md): 심부름 요청을 탐색/이동/파지/운반/전달 단계와 취소·지원 요청으로 분해
- [[F2047] 사람 근접 조작 안전](F2047/README.md): 사람 근접 조작의 감속·정지·작업영역 제한을 독립 안전경로와 연결
- [[F2142] 손끝 Force·Tactile Sensor HW 통합](F2142/README.md): 손끝 force/tactile HW의 배선·sample·calibration·교체 가능 구조를 설계
- [[F2143] 물체 재질·취약성 추정 및 Unknown 안전정책](F2143/README.md): vision/접촉으로 재질·취약성을 추정하고 Unknown일 때 보수적인 파지 정책을 적용
- [[F2144] Force·Slip 기반 Adaptive Soft Grasp](F2144/README.md): force/slip feedback로 힘 증분·재파지·중단을 결정
- [[F2145] One-Hand·Two-Hand 조작 판단](F2145/README.md): 크기·추정 질량·취약성·작업경로로 한손/양손/지원 요청을 선택
- [[F2146] 양팔 협조 제어·재파지·지원 요청](F2146/README.md): 양팔 trajectory 동기화·하중분배·재파지와 지원 요청을 구성
