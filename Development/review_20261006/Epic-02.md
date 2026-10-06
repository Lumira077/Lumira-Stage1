# EPIC-02 AI 대화 및 음성 인터랙션 — 개발 점검 R1

기준: 2026-10-06 / Jira KR1-42 / 원격 기준 96c6285.

직접 하위 작업 20건, Sub-task 80건. 요구사항·소스 매핑 점검이며 모든 하위 작업의 인수시험 완료를 뜻하지 않습니다.

## 이번 수행

기존 요구사항·하위 작업과 소스 위치를 대조하고 회귀/계약 증거 및 남은 작업을 정리. 신규 제품 기능 완료를 주장하지 않음.

## 검증

해당 Epic Python 회귀시험 132건 통과.
전체 실행 명령·로그는 `validation.json` 및 같은 폴더의 `.log` 파일에 있습니다. 실제 하드웨어·외부 제공자·실사용자 시험은 수행하지 않았습니다.

## 남은 개발·입력

Pi5 실측 음성 파이프라인, 마이크 AEC/DOA·스피커 loopback, STT/TTS 제공자·동의·지연 평가

## 작업별 소스 위치

| Jira | 개발 항목 | 소스/계약 경로 |
|---|---|---|
| KR1-43 | [F2205] Hybrid AI Policy Engine | Epic-02/F2205 |
| KR1-48 | [F2206] Multi-Cloud LLM Gateway | Epic-02/F2206 |
| KR1-53 | [F2207] Real-time Multimodal Cloud Session | Epic-02/F2207 |
| KR1-58 | [F2208] Local Conversation Context 및 RAG | Epic-02/F2208 |
| KR1-63 | [F2209] AI Cost 및 Quota Awareness | Epic-02/F2209 |
| KR1-68 | [F2210] Network Quality Adaptive Routing | Epic-02/F2210 |
| KR1-73 | [F2211] Privacy 및 Safety Routing | Epic-02/F2211 |
| KR1-78 | [F2212] LLM Failover 및 Session Recovery | Epic-02/F2212 |
| KR1-83 | [F2213] AI Quality Telemetry | Epic-02/F2213 |
| KR1-88 | [F2008] 호출어 및 대화 시작 | Epic-02/F2008 |
| KR1-93 | [F2009] 실시간 음성 인식(STT) | Epic-02/F2009 |
| KR1-98 | [F2010] Multi-LLM 자연어 대화 | Epic-02/F2010 |
| KR1-103 | [F2011] 대화 세션 문맥 관리 | Epic-02/F2011 |
| KR1-108 | [F2012] 대화 중 끼어들기와 중단 | Epic-02/F2012 |
| KR1-113 | [F2013] 다국어 대화 | Epic-02/F2013 |
| KR1-118 | [F2014] 연령·상황별 안전 대화 정책 | Epic-02/F2014 |
| KR1-123 | [F2121] Stage1 오프라인 기본 명령·Local 안전 응답 | Epic-02/F2121 |
| KR1-128 | [F2122] Stage2 Small Local LLM·RAG·NPU 실행 | Epic-02/F2122 |
| KR1-133 | [F2123] Stage3 Hybrid AI Router 및 개인화 | Epic-02/F2123 |
| KR1-138 | [F2126] AEC·Beamforming·음원 방향 추정 | Epic-02/F2126 |

Sub-task 전체 매핑은 `traceability.csv` 참조. 경로 존재는 구현·완료 판정이 아닙니다. 계약만 있는 항목과 미연동 adapter는 기존 명세의 제한을 유지합니다.

## 반영 상태

로컬 검토 브랜치에 통합. GitHub 연결의 push 권한 없음 및 브랜치 생성 403으로 원격 게시/신규 CI 미실행. Jira에는 이번 결과를 추가하고 완료 상태로 일괄 변경하지 않습니다.
