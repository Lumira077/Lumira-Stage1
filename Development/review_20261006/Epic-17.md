# EPIC-17 제품 기능·디자인·사용성 설계 — 개발 점검 R1

기준: 2026-10-06 / Jira KR1-832 / 원격 기준 96c6285.

직접 하위 작업 21건, Sub-task 80건. 요구사항·소스 매핑 점검이며 모든 하위 작업의 인수시험 완료를 뜻하지 않습니다.

## 이번 수행

기존 20 Feature/80 Sub-task의 설계·UI 시제품·합성 사용자평가·22개 시험을 저장소에 통합.

## 검증

설계 시제품 시험 22건 및 합성 평가 실행 통과.
전체 실행 명령·로그는 `validation.json` 및 같은 폴더의 `.log` 파일에 있습니다. 실제 하드웨어·외부 제공자·실사용자 시험은 수행하지 않았습니다.

## 남은 개발·입력

실사용자 음성·터치 평가, 실제 부품 간섭·외장 두께 검증, CAD 가져오기 오류 수정과 디자인 승인

## 작업별 소스 위치

| Jira | 개발 항목 | 소스/계약 경로 |
|---|---|---|
| KR1-833 | [F2104] 제품 Concept 및 Target User 정의 | Epic-17/F2104 |
| KR1-838 | [F2105] Stage1 제품 기능 Requirement 정의 | Epic-17/F2105 |
| KR1-843 | [F2106] 사용자 Scenario·Journey·Use Case 설계 | Epic-17/F2106 |
| KR1-848 | [F2107] Human-Robot Interaction 기본 원칙 설계 | Epic-17/F2107 |
| KR1-853 | [F2108] 로봇 Size·비례·자세·동작 영역 설계 | Epic-17/F2108 |
| KR1-858 | [F2109] 외관 Industrial Design Concept | Epic-17/F2109 |
| KR1-863 | [F2110] 얼굴 Display·표정 UX Design | Epic-17/F2110 |
| KR1-868 | [F2111] 가슴 Touch LCD UI/UX | Epic-17/F2111 |
| KR1-873 | [F2112] 음성·표정·Gesture Interaction UX | Epic-17/F2112 |
| KR1-878 | [F2113] 버튼·터치·충전·전원 등 Physical UX | Epic-17/F2113 |
| KR1-883 | [F2114] CMF(Material/Color/Finish) 설계 | Epic-17/F2114 |
| KR1-888 | [F2115] 3D CAD Exterior 및 Packaging 설계 | Epic-17/F2115 |
| KR1-893 | [F2116] Design Mock-up 제작 | Epic-17/F2116 |
| KR1-898 | [F2117] 사용자 사용성 Test 및 UX 평가 | Epic-17/F2117 |
| KR1-903 | [F2118] 디자인 개선 및 최종 Design Freeze | Epic-17/F2118 |
| KR1-908 | [F2119] 양산 Design/DFM 및 외장 구조 확정 | Epic-17/F2119 |
| KR1-913 | [F2128] 캐릭터형·리얼형 Face UI 사용자 평가 | Epic-17/F2128 |
| KR1-918 | [F2134] Stage1~4 공통 Body Size·Work Envelope 규격 | Epic-17/F2134 |
| KR1-923 | [F2154] Robot Fashion 기계 Interface·안전 표준 | Epic-17/F2154 |
| KR1-928 | [F2155] 고객군별 Robot Fashion·CMF·Accessory Design | Epic-17/F2155 |
| KR1-1111 | [KR1-SP2-C04] 사용자 2군 시나리오·음향·터치 사용성 검증 | 별도 작업; 아래 통합자료/후속 작업 참조 |

Sub-task 전체 매핑은 `traceability.csv` 참조. 경로 존재는 구현·완료 판정이 아닙니다. 계약만 있는 항목과 미연동 adapter는 기존 명세의 제한을 유지합니다.

## 반영 상태

로컬 검토 브랜치에 통합. GitHub 연결의 push 권한 없음 및 브랜치 생성 403으로 원격 게시/신규 CI 미실행. Jira에는 이번 결과를 추가하고 완료 상태로 일괄 변경하지 않습니다.
