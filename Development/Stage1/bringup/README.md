# Pi5 + UNO 실기 연결 준비 R2

기준: Pi5 8GB + AI HAT+ 13 TOPS. UNO R4 Minima A/B는 권장 후보이며 실물 확인 전 `confirmed:false` 유지.
이 패키지는 **식별·연결 진단** 단계다. 휠/관절/센서 제어 드라이버 및 물리 안전 회로는 아직 연결하지 않는다.

## 네트워크와 전기 연결

| 구간 | 연결 | 역할 |
|---|---|---|
| PC ↔ 공유기 ↔ Pi | 초기 유선 LAN | SSH 개발·진단 |
| NAS ↔ 공유기 | 유선 LAN | 개발 DB·로그; 로컬 정지 기능의 의존 대상 아님 |
| Pi ↔ UNO A/B | USB 데이터 케이블 | A 휠/센서 후보, B 관절 후보 식별 |
| Pi ↔ AI HAT+ | PCIe 케이블·GPIO 헤더 | Hailo-8L 지원 모델 추론 |
| Pi ↔ 카메라 | Pi5 규격 CSI 케이블 | 영상 |
| Pi ↔ 음성·터치 | USB, 화면 HDMI | 음성 입출력·터치 |

config.example.json의 IP는 예시다. 실제 공유기 subnet과 DHCP 예약 주소를 반영한다.
외부 접속은 VPN 등 승인된 경로를 사용한다. 비밀번호/개인키는 저장소나 JIRA에 올리지 않는다.
Pi SSH 접속 자체와 이 대화에서의 원격 실행 권한은 별개다.

초기 Pi는 공식 27W USB-C 전원과 냉각장치를 사용한다. UNO는 USB 전원으로 단독 연결한다.
모터 전원은 **분리·차단한 채** 진행한다. USB open 및 펌웨어 업로드로 MCU가 리셋될 수 있다.
UNO 5V 신호를 Pi 3.3V GPIO에 직접 입력하지 않는다. 액추에이터 정격·핀맵·드라이버·배터리/BMS·퓨즈가 확정되기 전 전력부를 결선하지 않는다.
UNO GPIO 초기 상태만으로 드라이버 차단을 보장할 수 없다. 물리 차단/enable 회로 검증 필요.

## 프로그램 사용

프로젝트 루트에서 Python 3.9 이상, Linux/Pi OS로 실행한다. 외부 Python 패키지 불필요.

```sh
python Development/Stage1/bringup/probe.py --mode check
python Development/Stage1/bringup/probe.py --mode simulate
python -m unittest discover -s Development/Stage1/bringup/tests -v
```

- check: 설정을 검증하고 경로 존재만 확인. 포트를 열지 않는다. 종료코드0은 설정 검사 성공이며 실기 준비 완료가 아니다.
- simulate: 고정 프로토콜 응답을 합성. `physical_transport_exercised:false`.
- probe: 아래 준비 후 실제 USB tty에서 identity 요청/응답만 수행. 모터 명령은 없다.
- 잘못된 설정·응답·timeout은 종료코드2. 실패 후 자동 모터 재시작 기능 없음.

### 실제 장비 준비

1. 보드 라벨로 R4 Minima 확인. R3/R4 WiFi는 이 초안의 대상이 아니므로 별도 검토한다.
2. 기존 스케치 소스를 보존한다. 제공 스케치를 올리면 기존 프로그램을 교체한다.
3. Arduino IDE에서 실물에 맞는 UNO R4 Minima 보드/포트를 선택하고 `firmware/lumira_probe/lumira_probe.ino`를 **대상 보드용으로 컴파일**한다.
4. A에는 BOARD_ROLE='A', B에는 BOARD_ROLE='B'로 각각 업로드한다. 본 작업 환경에는 Arduino CLI/toolchain이 없어 대상 MCU 컴파일·업로드는 미수행이다.
5. `ls -l /dev/serial/by-id/`로 각각의 경로를 확인한다. 식별번호가 없거나 중복이면 임의의 ttyACM 순서를 사용하지 말고 포트별 udev 규칙을 먼저 구성한다. 현재 도구는 by-id 경로만 허용한다.
6. config.example.json을 로컬 설정 파일로 복사해 실제 경로·IP를 기입하고 실물 모델 확인 후 confirmed를 true로 바꾼다. 이 설정을 공개 저장소에 올리지 않는다.
7. 다른 시리얼 모니터를 닫고 포트 접근 권한을 확인한다. root 실행이나 전체 포트 권한 개방으로 우회하지 않는다.
8. MCU 부팅이 끝난 뒤 아래를 실행한다. timeout이면 보드 리셋 여부와 케이블/역할/펌웨어를 확인하고 다시 시도한다.

```sh
python Development/Stage1/bringup/probe.py --config /path/to/local-config.json --mode probe --output /path/to/identity-result.json
```

출력 `physical_transport_exercised:true`는 USB 통신 경로 사용을 뜻한다. 보드 진품 인증·센서 동작·모터 정지·출시 승인이 아니다. nonce는 이전 응답 혼입 검출용이며 암호학적 기기 인증을 대체하지 않는다.

## 프로토콜

115200 baud, 8N1, ASCII 한 줄. 호스트가 `HELLO <16자리 소문자 hex nonce>\n`을 전송.
장치는 `LUMIRA1 <nonce> <A 또는 B> UNO_R4_MINIMA probe-1 MOTION_DISABLED\r\n`을 응답.
역할/모델/펌웨어/nonce 불일치, 128바이트 초과, 여러 줄·미완성 응답을 거부한다.
펌웨어는 31문자 수신 버퍼 초과 입력을 newline까지 버리며 알려진 HELLO만 응답한다.
실제 모터 프로토콜에 이 식별 메시지를 그대로 사용하지 않는다.

## 다음 실기 작업

UNO 확정 → 액추에이터·전원 정격/핀맵 → 독립 차단·watchdog → 센서 읽기 → 지그 저속 구동 → 정지/단선/재연결 시험.
Stage1에는 공간 자율주행과 구동 손가락을 포함하지 않는다. 어깨/팔목은 각각 하중 검토가 필요하다.

## 공식 참고자료 (2026-10-06 확인)

- https://docs.arduino.cc/hardware/uno-r4-minima/
- https://www.raspberrypi.com/documentation/accessories/ai-hat-plus.html
- https://www.raspberrypi.com/documentation/computers/remote-access.html

AI HAT+13 TOPS는 Hailo-8L 기반이며 지원 영상 모델 중심이다. 모든 대화 LLM을 자동 가속한다는 전제는 사용하지 않는다.
