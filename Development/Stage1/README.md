# Lumira Sprint1 개발·검토 패키지 R1

대상: KR1-1101~1106. 문서6건, BOM, 위험 목록, 구조도, 모의 통신 소스/ROS2 adapter, 신규 실행 로그 포함.
- reports/: 이슈별 보고서
- BOM_v0.1.csv: 품목별 2후보
- risk_register.csv: 위험12건
- KR1-1102_Architecture_R1.png: 시스템 경계 구조도
- contract_core.py, contract.json, fixtures.jsonl: 모의 계약
- mock_transport.py: 두 프로세스 localhost TCP 시험 (DDS 아님)
- tests/: 경계/실패조건 계약 시험
- ros2_ws/: ROS2 Jazzy adapter 개발안, DDS 실행 미검증
- evidence/: 실제 신규 실행 원시로그, SHA256SUMS.txt

재현: 패키지 루트에서 `python3 mock_transport.py`, `python3 -m unittest discover -s tests -v`.
센서·관절·전원·사용자 평가 및 사람의 R1/R3 승인 미완료. production 배포/실기 사용을 위한 firmware가 아니다. 실물 실행은 0건.

## R2 실기 연결 진단

[Pi5·UNO 네트워크/연결·identity 프로그램](bringup/README.md). MCU용 펌웨어 초안은 대상 toolchain 컴파일·실물 시험 전 단계이며 모터 제어를 포함하지 않습니다.
