# F2122-S01

Jira: https://lumira077.atlassian.net/browse/KR1-129

- 보드/RAM·모델/양자화/라이선스/hash·runtime·NPU 지원·전력/발열·Tool 허용표 정의
- LocalModelManifest: runtime, model_hash, quantization, ram_required_mb, supported_hardware; ToolProposal: allowed_action의 필수값·민감도·보존기간·권한·revision/epoch를 표로 정의한다.
- LocalModelGate.validate/propose; 운영 inference는 llama.cpp/보드별 runtime의 별도 adapter의 정상·오류·취소·stale 입력 계약 및 시험 데이터 분할을 명세화한다.

산출물: 요구사항·데이터/인터페이스 계약·예외표·시험 기준

상위 Feature 완료조건: 선정 모델을 실제 보드에서 실행해 RAM/first token/속도/발열 목표와 승인 Tool 검증을 통과한다.

현재 제한: 현재 자원/Tool gate만 구현; 모델 다운로드·실제 추론·RK3588 NPU/Jetson 가속·실물 benchmark 미실시

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
