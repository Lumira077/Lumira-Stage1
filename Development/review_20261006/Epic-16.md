# EPIC-16 로봇 하드웨어 시스템 구축 — 개발 점검 R1

기준: 2026-10-06 / Jira KR1-711 / 원격 기준 96c6285.

직접 하위 작업 27건, Sub-task 100건. 요구사항·소스 매핑 점검이며 모든 하위 작업의 인수시험 완료를 뜻하지 않습니다.

## 이번 수행

기존 Pi5·UNO 결선 문서·7개 이미지와 Sprint1 BOM·위험목록·전송 계약을 저장소에 통합.

## 검증

공통 유틸리티 시험 80건·계약 검사 공유; 해당 Epic 전체 기능시험 수가 아님.
전체 실행 명령·로그는 `validation.json` 및 같은 폴더의 `.log` 파일에 있습니다. 실제 하드웨어·외부 제공자·실사용자 시험은 수행하지 않았습니다.

## 남은 개발·입력

UNO 정확한 모델 확정, 모터·배터리·충전기 정격 및 전원 지그, 하네스/열/하중·낙하 방지 실측, CAD 오류 수정

## 작업별 소스 위치

| Jira | 개발 항목 | 소스/계약 경로 |
|---|---|---|
| KR1-416 | [F2056] 동화 스토리텔링 | Epic-10/F2056 |
| KR1-712 | [F2090] Stage1 HW 요구사양 및 시스템 Architecture | Epic-16/F2090 |
| KR1-717 | [F2091] Main Computing HW 선정 및 인터페이스 설계 | Epic-16/F2091 |
| KR1-722 | [F2092] Safety MCU·Motor Interface·I/O 제어 Architecture | Epic-16/F2092 |
| KR1-727 | [F2093] 목·팔·허리·손 구동 HW 및 Actuator 선정 | Epic-16/F2093 |
| KR1-732 | [F2094] Camera·Mic·IMU·Touch·근접 Sensor HW 구성 | Epic-16/F2094 |
| KR1-737 | [F2095] 얼굴 Display·Touch LCD·Audio HW 구축 | Epic-16/F2095 |
| KR1-742 | [F2096] Battery·BMS·전용 전원·안전 Board 설계 | Epic-16/F2096 |
| KR1-747 | [F2097] 내부 Frame 및 기구 Architecture 설계 | Epic-16/F2097 |
| KR1-752 | [F2098] 내부 배치·배선·Connector·Harness 설계 | Epic-16/F2098 |
| KR1-757 | [F2099] 열·소음·진동·EMI 대응 설계 | Epic-16/F2099 |
| KR1-762 | [F2100] HW Prototype #1 제작 | Epic-16/F2100 |
| KR1-767 | [F2101] ROS2/HW 통합 및 Bring-up 시험 | Epic-16/F2101 |
| KR1-772 | [F2102] HW Prototype #2 개선 및 제품화 설계 | Epic-16/F2102 |
| KR1-777 | [F2103] HW 신뢰성·안전·양산성 검증 | Epic-16/F2103 |
| KR1-782 | [F2125] 4~6채널 MEMS Mic Array HW | Epic-16/F2125 |
| KR1-787 | [F2132] Main Camera 사양·위치·시야각 검증 | Epic-16/F2132 |
| KR1-792 | [F2135] Stage 확장 Modular Interface 표준 | Epic-16/F2135 |
| KR1-797 | [F2136] 관절 Motor Bench·열·소음·수명 검증 | Epic-16/F2136 |
| KR1-802 | [F2156] NFC Fashion·Accessory 인식 HW | Epic-16/F2156 |
| KR1-807 | [F2221] Fusion·AI 기반 Mechanical CAD·BOM·도면 Workflow | Epic-16/F2221 |
| KR1-812 | [F2222] COTS 70%·Custom 30% 전자구성 및 전환 Gate | Epic-16/F2222 |
| KR1-817 | [F2223] 전용 Power·Safety Board 개발 | Epic-16/F2223 |
| KR1-822 | [F2224] STM32 Motion·I/O·Safety Controller Board | Epic-16/F2224 |
| KR1-827 | [F2225] RK3588 SoM 양산 Carrier Board 개발 | Epic-16/F2225 |
| KR1-1109 | [KR1-SP2-C02] UNO 모델·단일축 DYNAMIXEL·휠·센서 Bring-up | 별도 작업; 아래 통합자료/후속 작업 참조 |
| KR1-1110 | [KR1-SP2-C03] 전원·충전 인터록 및 탁상 이동 안전 지그 검증 | 별도 작업; 아래 통합자료/후속 작업 참조 |

Sub-task 전체 매핑은 `traceability.csv` 참조. 경로 존재는 구현·완료 판정이 아닙니다. 계약만 있는 항목과 미연동 adapter는 기존 명세의 제한을 유지합니다.

## 반영 상태

로컬 검토 브랜치에 통합. GitHub 연결의 push 권한 없음 및 브랜치 생성 403으로 원격 게시/신규 CI 미실행. Jira에는 이번 결과를 추가하고 완료 상태로 일괄 변경하지 않습니다.

## 계층 불일치 발견

KR1-416 [F2056] 동화 스토리텔링의 현재 Jira parent는 KR1-711(Epic16)이지만 저장소 계약은 Epic-10/F2056에 있습니다. traceability.csv에는 실제 소스 위치를 연결했습니다. 콘텐츠 범위상 Epic10과 관련되지만 의도된 이관 여부를 확인할 수 없어 Jira parent/기존 계약을 임의 변경하지 않았습니다. 담당자의 소속 확인 후 두 기준을 일치시켜야 합니다.
