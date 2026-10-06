# EPIC-04 얼굴 표정·음성·동작 표현

Jira: https://lumira077.atlassian.net/browse/KR1-169

9개 Feature(F2020~F2025/F2129~F2131), 36개 Sub-task. 첨부 상세 9 Feature/87 SP 목록과 AI로봇사업.docx 구상에 따라 보완한다. 초기 6개 Feature/58 SP 이미지는 이전 버전이다. 요약 이미지의 일부 Feature 매핑보다 현재 Jira/상세 목록을 기준으로 한다.

실행: `python Epic-04/runtime/run.py` / `python Epic-04/runtime/demo.py` (Python 3.11+, stdlib).

현재: 표정 pose/blend/SVG 생성, TTS voice/locale/동의 계획, fixture gesture의 joint position/segment velocity·시작자세 검증, playback-clock cue queue/세 채널 취소 ACK 계약, trusted intent 선택, 제한된 performance plan, SHA256/상태 검증을 통한 skin metadata 교체, supplied viseme/gaze pose, R&D metadata gate.

실제 TTS/음성 재생·모터/ROS·GPU/Qt display loop·2.5D renderer·camera tracking·forced alignment·semantic classifier·실제 사용자 없음. 모든 제스처 계획은 executable=false. clearance/rights/의미 태그·동의는 trusted fixture이며 실제 검증 서비스가 아니다. 가상 취소 ACK는 물리 정지 증거가 아니다. raw text/media를 일반 로그에 저장하지 않는다.

통합: Epic-01 프로필/개인 선호/동의 → Epic-02 F2010 대화/F2012 끼어들기/F2126 audio reference → Epic-03 감정 후보/unknown → F2024 표현 선택 → F2020·F2021·F2022 → F2023 타임라인 → F2129 skin/F2130 gaze/lip. 실제 auth/event bus/adapter는 추가 개발이다. unknown/위험/quiet/사용자 전환·철회는 보수적인 기본표정·움직임 보류와 실제 취소/정지 확인으로 연동한다.

Stage 1 기본은 캐릭터 얼굴이다. F2131은 Stage 2~3 연구 옵션이며 production_enabled=false. due 2029-06-30은 Epic due 2028-03-31보다 늦어 별도 R&D/OTA 일정 검토가 필요하다. Jira 상태·담당자·날짜를 변경하지 않았다.

Release: 실제 장비/Provider/저작권·privacy·사용자 평가·watchdog/실제 stop ACK·Q1/R1·배포/rollback 증거 확보 전 release_ready=false. provisional joint/volume/sync/research 기준을 실제 안전/품질 목표로 사용하지 않는다.
