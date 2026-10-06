# Lumira Stage1 프로그램 운영 안내

2026-10-06 | 저장소: [Lumira077/Lumira-Stage1](https://github.com/Lumira077/Lumira-Stage1)

현재 실행 가능한 것은 **오프라인 기능 시제품·자동시험·UI 미리보기·Pi–UNO 장치 식별 진단**입니다. 전체 로봇을 구동하는 통합 서비스나 실제 모터 드라이버 펌웨어는 아직 제공되지 않습니다. Python 시험 통과와 실물 인수 완료를 구분합니다.

![네트워크와 장치 연결](images/network.svg)

## 1. PC에서 시작

Git, Python 3.11 이상을 준비합니다. 아래 시험은 외부 AI 계정·모터·배터리 없이 실행됩니다. 신규 시리얼 실기 진단은 Linux/Pi OS용이며 Windows에서는 WSL의 가상 포트 시험과 물리 USB 연결을 구분해야 합니다.

```sh
git clone https://github.com/Lumira077/Lumira-Stage1.git
cd Lumira-Stage1
python3 scripts/verify_all.py
```

정상 결과는 10개 suite PASS, 총595개 시험입니다. 로그와 `summary.json`은 `artifacts/verification/`에 생성됩니다. 실패 시 종료코드1을 반환합니다. 소스 커밋과 변경 상태도 기록하므로 수정된 작업트리의 결과를 깨끗한 커밋의 CI 결과로 오해하지 않습니다.

| 실행 대상 | 명령 | 확인할 내용 |
|---|---|---|
| 전체 오프라인 시험 | `python3 scripts/verify_all.py` | 595개, 실기 제외 |
| Pi/UNO 설정 검사 | `python3 Development/Stage1/bringup/probe.py --mode check` | 설정·장치 경로 존재; 포트 미개방 |
| UNO 응답 모의시험 | `python3 Development/Stage1/bringup/probe.py --mode simulate` | `physical_transport_exercised:false` |
| 2프로세스 전송 시제품 | `python3 Development/Stage1/mock_transport.py` | TCP 모의 전송7건; DDS 아님 |
| 설계 합성 데이터 집계 | `python3 Epic-17/runtime/run.py` | 합성 사용성 지표; 실제 참가자 아님 |

Epic01~06은 각각 `runtime/run.py`(Epic01은 `integration/run.py`)를 사용합니다. Epic07~16의 다수 항목은 계약·증적 도구이며 각 Feature README의 구현 범위를 확인합니다. Epic18~20은 원본 저장소의 참고 자료를 보존한 것으로 이번 Stage1 개발 점검 범위 밖입니다.

## 2. 화면 미리보기

프로젝트 루트에서 아래를 실행하고 로컬 브라우저로 `http://127.0.0.1:8000/Epic-17/prototype/index.html`에 접속합니다.

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

이 화면은 디자인 검토용 시제품입니다. 실제 로봇 연결·인증·카메라·모터 제어를 수행하지 않습니다. 종료는 터미널에서 Ctrl+C입니다. 기본 서버는 로컬 PC만 접근하도록 제한했습니다.

## 3. PC–Pi–NAS 네트워크

PC/Pi/NAS를 같은 공유기에 연결하고 실제 주소 대역에서 DHCP 예약을 설정합니다. 예시 대역은 192.168.10.0/24이며 실제 LAN이 다르면 설정 파일을 바꿉니다. 최초 유선 LAN으로 접속한 후 이동시험에 Wi-Fi를 사용합니다.

```sh
ssh 사용자명@Pi의_IP
cat /etc/os-release
uname -m
hostname -I
lsusb
ls -l /dev/serial/by-id/
```

SSH는 Pi OS 초기 설정에서 활성화합니다. 공개 인터넷으로 SSH·DB 포트를 직접 노출하는 대신 승인된 VPN 경로를 사용합니다. NAS는 로그·개발 DB 용도이며 장애물/추락 정지의 의존 대상이 아닙니다. 개인키·비밀번호·실제 로컬 설정은 GitHub/JIRA에 저장하지 않습니다.

Pi5 8GB + AI HAT+13 TOPS 기준을 유지합니다. 공식 Pi OS/Hailo 안내에 맞춰 드라이버·지원 모델을 설치하고 버전을 기록합니다. HAT 장착/케이블 작업은 전원 OFF에서 진행하며 초기에는 공식27W USB-C 전원과 냉각장치를 사용합니다. 지원되는 영상 추론과 대화 LLM 실행은 별도의 경로입니다.

## 4. UNO 장치 식별

[실기 연결 진단 상세 안내](../Development/Stage1/bringup/README.md)를 먼저 확인합니다.

1. R4 Minima 실물 여부를 확인하고 모터 전원을 분리합니다.
2. 기존 UNO 스케치를 보존합니다. 새 스케치 업로드는 기존 프로그램을 교체합니다.
3. Arduino IDE에서 대상 보드를 선택하고 `lumira_probe.ino`를 컴파일합니다. A와 B 각각 BOARD_ROLE을 지정해 업로드합니다.
4. 두 보드를 한 대씩 연결하여 고유 by-id 경로를 기록합니다. 역할은 응답의 A/B로 다시 확인합니다.
5. 예시 설정을 `robot.local.json`으로 복사하고 실제 IP·장치 경로를 기입합니다. 모델 확인 후에만 confirmed를 true로 변경합니다.
6. MCU 부팅 후 진단을 실행합니다.

```sh
mkdir -p artifacts
cp Development/Stage1/bringup/config.example.json robot.local.json
python3 Development/Stage1/bringup/probe.py --config robot.local.json --mode probe --output artifacts/identity.json
```

`artifacts/`가 없다면 먼저 생성합니다. 진단은 HELLO/identity 메시지만 교환합니다. 역할·nonce·모델·응답 형식이 맞아야 성공하며 실제 정지 검증은 계속 false입니다. USB 포트 개방이 보드를 리셋할 수 있습니다. UNO 대상 컴파일과 실제 보드 시험은 아직 수행하지 않았습니다.

## 5. 실제 모터 연결

[실제 모터 제어 연결·시운전 상세 설명](MOTOR_CONNECTION_KO.md)을 따릅니다. 현재 identity 펌웨어에 모터 명령을 보내도 구동되지 않습니다. 실제 제어에는 모델·전원·핀맵 확정 후 별도 펌웨어와 독립 정지 회로 검증이 필요합니다.

![휠 신호·전원 연결](images/wheel_connection.svg)

## 6. 장애 대응

| 증상 | 확인·조치 |
|---|---|
| SSH 접속 실패 | IP·LAN 대역·SSH 활성화·방화벽 확인. 모터 제어 문제와 분리 |
| by-id 경로 없음 | 데이터용 USB 케이블, 전원, 포트, 보드 장치 식별정보 확인 |
| permission denied / busy | 다른 시리얼 모니터 종료, 사용자 포트 접근 권한 확인. 전체 권한 개방으로 우회하지 않음 |
| identity timeout | 부팅/리셋·스케치·baud·케이블 확인. 자동 모터 재시작 금지 |
| identity mismatch | A/B 역할·보드 모델·펌웨어 버전 확인. 검사 완화 금지 |
| Pi 저전압/재부팅 | 공식 전원·USB 전력 예산·모터 전원 분리·배선 전압강하 점검 |
| Hailo 인식 실패 | PCIe 케이블·드라이버·OS/모델 호환 버전 확인 |
| 시험 실패 | 해당 suite.log와 소스 commit/변경 상태 기록. 실제 장비를 연결해서 우회하지 않음 |

## 7. 종료·업데이트·복구

모의시험은 프로세스 종료로 끝납니다. 실제 장비 단계에서는 먼저 승인된 정지 절차로 구동을 차단하고 팔/목을 지지한 뒤 로깅·OS 정상 종료를 수행합니다. 전원 차단 시 관절이 처질 수 있습니다.
업데이트 전 로컬 설정·시험 기록과 현재 커밋을 보관하고, 변경분을 검토한 뒤 전체 시험을 실행합니다. 현재는 OTA 배포·자동 rollback이 연결되지 않았습니다. 확인된 이전 커밋으로 소스를 복귀해도 모터를 자동 재구동하지 않습니다.

- [R1 Epic별 보고서·추적표](../Development/review_20261006/README.md)
- [R2 프로그램 보완 보고서](../Development/review_20261006_R2/README.md)
- [원격 자동시험](https://github.com/Lumira077/Lumira-Stage1/actions)
- [기존 Pi5/UNO 결선 초안](../Epic-16/board_design/Lumira_Pi5_UNO_Wiring_R1.md)
