# [F2222] COTS 70%·Custom 30% 전자구성 및 전환 Gate

Jira: https://lumira077.atlassian.net/browse/KR1-812

COTS70/Custom30 구상 및make/buy·공급/원가·EVT/DVT전환 gate를 관리

입력/출력: module·make/buy·supplier·cost·lifecycle·gate

경계시험: 단종·공급부족·자체화미승인·BOM변경

지표: 대체품·configuration 추적·gate승인

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-16/F2222/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

COTS70/Custom30 구상: 전원/안전 → STM32 Motion/I/O → DVT 이후 RK3588 SoM carrier 순서. Fusion masterCAD·중립 STEP/PDF/DXF·BOM revision, Stage1 UVC1080p HDR·4채널 USB mic·DYNAMIXEL, RGB-D 옵션 및 HW benchmark 후 단일 플랫폼 gate. 명세 수치/후보는 구매승인·물리성능 검증이 아니다.

필요 입력/연동: CAD/회로/PCB master·보드/센서/actuator SKU·전기정격/chemistry·BOM/공급 견적·bench/jig·측정기·EVT/DVT·인증 검토

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
