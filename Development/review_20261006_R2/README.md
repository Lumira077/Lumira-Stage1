# Epic01~17 프로그램 통합·재검증 R2

최신 연결 상태: 2026-10-06 사용자가 https://github.com/Lumira077/Lumira-Stage1 을 지정했고 읽기·쓰기 권한 및 빈 저장소를 확인했다. 아래 접근0건 기록은 대상 지정 전의 이력이다. 원격 반영/CI 최종 결과는 후속 게시 기록과 JIRA를 따른다.

기준일 2026-10-06. 요청 GitHub 계정 Lumira077. 현재 로그인도 Lumira077으로 확인.
접근 가능한 저장소 조회(전체/owner 필터/owner affiliation)가 모두 0건으로 반환되어 대상 저장소를 확정하거나 push/PR을 수행하지 못했다. 이는 R1의 retri/KER-Robot 403과 구분되는 현재 연결 상태다. 저장소가 없다고 단정하지 않는다.
대상 저장소 URL과 해당 저장소에 대한 GitHub 앱 접근·쓰기 권한이 필요하다. 계정만으로 저장소명을 임의 생성하지 않았다.

## 적용 내용

R1 커밋1788ac0의 17 Epic 점검·3개 결함 수정·SQLite 원장·Epic17 및 보드설계/Sprint1 결과를 유지했다.
R1 목록은 17 Epic, 183 Feature+4 기타 직접 하위 작업, 732 Sub-task. 현재 17 Epic Description을 재조회하여 R1 기록 존재를 확인했다. 모든 하위 요구사항이 구현 완료된 것은 아니다.

이번 추가 코드: Development/Stage1/bringup/probe.py 및 config.example.json, UNO identity 펌웨어 초안, 테스트20건, 연결 설명서.
- Pi5 8GB/Hailo-8L13TOPS·Stage1 기준 고정, UNO R4 Minima 2대는 실물 확인 전 후보 상태.
- 네트워크 subnet/IP 중복과 안정적 serial by-id 경로 검사.
- check(설정/경로), simulate(합성), probe(실제 identity 요청) 모드 분리.
- 모델 미확인 시 probe 차단, A/B 역할·모델·nonce·프레임 길이·응답 시간 검증.
- Linux 표준 라이브러리 serial 전송/단독 점유/timeout 정리 구현. 모터 제어 명령 없음.
- UNO 스케치는 HELLO에만 응답. 모터/센서 핀을 설정하지 않는다. 실제 드라이버의 물리 차단과 같지 않다.
- GitHub Actions에 신규20개 시험 및 simulation 추가. 원격 게시되지 않아 신규 Actions 미실행.

## 실행 검증

Python 총595건 통과: Epic01~06 457 + 공통80 + Epic17 22 + Stage1 16 + 신규20.
신규20에는 실제 Linux 가상 터미널(PTY) 송수신과 timeout 후 포트 해제 시험이 포함된다. PTY는 UNO 실물이 아니다.
기존 공통 계약148 Feature/557 Sub-task 검사도 통과. simulation은 실제 장치 연결로 표시하지 않는다.

MCU 대상 compiler/Arduino CLI 부재로 UNO 펌웨어 대상 컴파일·업로드 미실행. Pi5/Hailo·카메라·음성·ROS2/DDS·모터·전원·실사용자 검증 미수행.
소스/로그는 이 폴더 validation.json과 suite별 log 참조. 새 소스 hash는 source_sha256.txt.

## Epic별 처리

| Epic | Jira | 이번 확인/적용 | 남은 핵심 작업 |
|---|---|---|---|
| Epic-01 | KR1-1 | R1 구현/계약 유지, 최신 Epic 기록 및 회귀 증거 재확인 | 프로필 스키마 확장과 기억·동의 epoch 이벤트 연결, 인증/NFC 실기, SKU 정책·사용자 평가 |
| Epic-02 | KR1-42 | R1 구현/계약 유지, 최신 Epic 기록 및 회귀 증거 재확인 | Pi5 실측 음성 파이프라인, 마이크 AEC/DOA·스피커 loopback, STT/TTS 제공자·동의·지연 평가 |
| Epic-03 | KR1-143 | R1 구현/계약 유지, 최신 Epic 기록 및 회귀 증거 재확인 | 카메라·음성 모델/가중치 선택, 동의된 평가 데이터와 calibration, 실시간 timestamp 정합 |
| Epic-04 | KR1-169 | R1 구현/계약 유지, 최신 Epic 기록 및 회귀 증거 재확인 | 표정·음성·관절의 실제 clock/취소 ACK 연결, 관절 속도·토크·음압 및 자연성 평가 |
| Epic-05 | KR1-215 | R1 구현/계약 유지, 최신 Epic 기록 및 회귀 증거 재확인 | 카메라·ToF·터치 드라이버, 식별/추적 실데이터 평가, cliff·장애물 실패 시 정지 검증 |
| Epic-06 | KR1-246 | Pi5–UNO 식별·네트워크/포트 설정 검사·시리얼 진단 추가 | Pi5/AI HAT+ 및 UNO 실기, ROS2/DDS·Hailo 실행, typed interface·watchdog·실제 stop ACK |
| Epic-07 | KR1-282 | R1 구현/계약 유지, 최신 Epic 기록 및 회귀 증거 재확인 | Stage2 범위: 실제 베이스·센서·URDF·TF·지도·Nav2 통합. Stage1에서는 공간 자율주행 미포함 |
| Epic-08 | KR1-318 | R1 구현/계약 유지, 최신 Epic 기록 및 회귀 증거 재확인 | Stage3 범위: 실제 관절/손끝·하중·힘 센서 및 조작 검증. Stage1 손가락은 비구동 플렉시블 |
| Epic-09 | KR1-374 | R1 구현/계약 유지, 최신 Epic 기록 및 회귀 증거 재확인 | 보호자 동의·알림 전달 ACK, 실제 평가 데이터와 전문가 검토. 건강 관련 실효성 검증 미완료 |
| Epic-10 | KR1-405 | R1 구현/계약 유지, 최신 Epic 기록 및 회귀 증거 재확인 | 검수·권리 확보 콘텐츠, 연령/보호자 정책, 실제 참가자와 학습·사용성 평가 |
| Epic-11 | KR1-436 | R1 구현/계약 유지, 최신 Epic 기록 및 회귀 증거 재확인 | 실제 앱/backend·pairing·인증·Push/WebRTC·원격 권한 및 통신 장애 통합시험 |
| Epic-12 | KR1-472 | R1 구현/계약 유지, 최신 Epic 기록 및 회귀 증거 재확인 | 기기 인증·DB·fleet·서명/KMS·OTA A/B bootloader·rollback의 실제 운영 증거 |
| Epic-13 | KR1-528 | R1 구현/계약 유지, 최신 Epic 기록 및 회귀 증거 재확인 | 인증·KMS·동의 철회·원본 보존정책, 독립 안전 회로와 침투/물리 고장 시험 |
| Epic-14 | KR1-584 | R1 구현/계약 유지, 최신 Epic 기록 및 회귀 증거 재확인 | 실제 provider 사용량 영수증, 계정/권한·요금 정책·가격 버전·회계 대사·Test PG 연결. SQLite는 로컬 원장 시제품 |
| Epic-15 | KR1-655 | R1 구현/계약 유지, 최신 Epic 기록 및 회귀 증거 재확인 | Stage2~4 범위: 승인 IoT/Gateway·공간 지도·권한·실제 기구/하중 검증. Stage1 실행 기능으로 활성화하지 않음 |
| Epic-16 | KR1-711 | Pi5–UNO 식별·네트워크/포트 설정 검사·시리얼 진단 추가 | UNO 정확한 모델 확정, 모터·배터리·충전기 정격 및 전원 지그, 하네스/열/하중·낙하 방지 실측, CAD 오류 수정 |
| Epic-17 | KR1-832 | 실기 연결 준비 절차를 기존 설계/시제품 결과와 연결 | 실사용자 음성·터치 평가, 실제 부품 간섭·외장 두께 검증, CAD 가져오기 오류 수정과 디자인 승인 |

## 이관 방법과 미결정

전달 패키지에 전체 소스 ZIP과 R1+R2 변경 패치를 포함한다. 기존 원격 내용이 있으면 먼저 비교한 뒤 브랜치/PR로 반영하며 덮어쓰지 않는다. 빈 새 저장소라면 전체 소스를 초기 import하는 방법을 선택할 수 있다. 실제 원격 구조 확인 전 이관은 수행하지 않았다.
R1 보고서·추적표는 Development/review_20261006/에 보존했다. KR1-416의 Jira parent(Epic16)와 기존 소스(Epic10) 불일치는 미해결이며 임의 이관하지 않았다.

UNO/액추에이터/전원 모델과 실장비 접근이 확보되면 identity 확인 → 센서 → 지그 저속 구동 → 정지/단선/재연결 → 배터리 통합 순서로 진행한다. Stage1의 공간 자율주행·구동 손가락은 제외한다.
