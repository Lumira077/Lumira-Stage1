# S03 기술 설계와 검증 한계

## 서비스 연결
의존성 검증 후 인접 S02 Service를 가져옵니다. LabService는 등록/프로필/동의/적용 저장을 재사용하며 GuardedOutputs를 통해 Broker로 context/tts/expression/motion 명령을 보냅니다. 적용 ACK의 applied_settings는 가상 설정 계약 대조용입니다. 실제 음색·관절 각도 적용 증적이 아닙니다.

greeting에는 application_id를 명시적으로 전달합니다. 프로필/호칭이 같은 여러 게스트도 서로 다른 적용 범위와 명령 UUID를 사용합니다. 최초 greeting의 logical_output_started만 true이고 반복은 최초 영수증을 사용합니다. robot_audio_played 및 physical_output은 false입니다. 실제 출력 서비스는 command_id에 대한 멱등 처리를 별도로 구현해야 합니다.

미리보기는 모든 필드/한도를 검사한 뒤 scope=preview:session_id에 출력 큐를 만듭니다. dispatch_preview는 세션 활성/만료/권한/기기 연결을 다시 확인합니다. cancel은 저장 초안 정리 후 scope를 비활성화하고 epoch를 증가시킵니다. stop_outputs는 등록 적용과 미리보기 범위를 함께 멈춥니다. 사용자 전환과 네트워크 단절의 운영 이벤트 배선은 후속 통합 항목입니다.

## 출력 Broker
scopes: id, actor, epoch, enabled, connected, stopped, context_hash. commands: UUID, scope, epoch, kind, request_key, deadline, 제한된 숫자 설정 payload, state, receipt. raw 호칭/발화 문장은 Broker에 저장하지 않습니다. 동일 scope/kind/request_key는 고유하며 다른 payload 재사용은 거절합니다.

명령마다 권한, 현재 epoch, stop latch, enabled, connected를 확인합니다. TTl 경과 queued 명령은 취소하고 실행하지 않습니다. done도 현재 권한/안전 상태 확인 후 영수증만 반환합니다. 정지는 먼저 출력 억제를 저장하고 transport.stop ACK를 확인합니다. ACK 실패는 physical_stop_verified=false로 기록하며 소프트웨어 억제를 풀지 않습니다.

Broker 새 인스턴스는 queued/executing 명령을 취소하고 모든 scope를 비활성화하며 epoch를 올립니다. 전송은 완료됐으나 영수증이 저장되지 않은 불확실한 상태에서도 자동 재실행하지 않습니다. 이는 출력 손실보다 중복/갑작스러운 재생 방지를 우선하는 시뮬레이션 정책입니다.

SQLite는 시험용 단일 작업자 구성입니다. DB 갱신과 실제 transport 호출의 원자성, 다른 스레드의 정지와 dispatch 경합, 독립 안전 경로의 지연 상한은 보장하지 않습니다. 정지 gate는 실제 E-stop 컨트롤러의 대체재가 아닙니다. hardware mode는 명시적으로 거부합니다.

## 안전 정책
volume 0~20, rate 0.7~1.2, expression 0~1, gesture_level 0~1, 물리 gesture none만 허용. 임의 joint_angle과 모터 명령은 거절합니다. 이는 실기 전 가상 fixture입니다. 음량은 소프트웨어 정규화 값이며 dBA 측정과 다릅니다. S02 입력 범위보다 엄격하므로 S02에서 허용한 높은 음량/수준은 S03 적용 실패로 반환됩니다. 묵시적 클램프를 하지 않습니다.

confirmed_input는 호칭/동의 입력의 명시적 true 확인과 타입 검사만 수행합니다. 실제 인식 정확도·소음·발음 시험은 not_run입니다.

## 결과 모델
report.json에는 환경, 고정 의존성, 실제 test id별 상태, ONB 시나리오별 software_status와 real_robot_status, 지연 측정 범위, hardware_tests not_run, software_gate, release_ready=false를 기록합니다. 실기 관련 필드는 자료 없이 null입니다. 시험 실패는 CLI exit1이며 최소100회 미달/미지원 hardware 모드는 거절합니다.

실패가 발생하면 실패 케이스와 회귀 시나리오를 고쳐 다시 실행하고 최종 커밋/CI를 Jira에 연결합니다. 초기 지연 목표를 넘으면 software_gate 실패로 보고하지만 목표 미달 원인/검토는 Q1/R1이 판단합니다. 수행되지 않은 실기 시험을 0건 실패로 집계하지 않습니다.

## 후속 실기 인수
실기 기기/펌웨어/ROS2 및 프로토콜, 소유권·보호자 권한, TTS/오디오, 표현·관절 제어, stop 전략, 센서 피드백, 물리 안전 한계를 받아 실제 드라이버를 별도로 구현해야 합니다. 실제 power-loss/파일시스템 복구, 음향 dBA/mute/onset, 관절 각도·속도·토크·끼임/낙하·정지시간을 측정해야 합니다. hardware-manifest.example.json은 수집 양식이며 내용을 채우는 것만으로 시험 완료가 되지 않습니다.
