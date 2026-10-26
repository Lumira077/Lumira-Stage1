# T02 M2 R4 작업 정리 — 2026-10-27
[Jira 통합 작업 KR1-1159](https://lumira077.atlassian.net/browse/KR1-1159)

## 현재 기준
R4 외형 유지, 상체 10DOF(팔당 4, 목 yaw 1, 허리 yaw 1), 구동 바퀴 2모터 별도. 하체 폭 7.5% 축소. 실물 배포 미실시, motor_output_enabled=false.
[모델·교감 상세](README_KO.md) / [자율주행 상세](navigation/README_KO.md)

## 작업 이력과 검증 범위
|구분|결과/현황|
|---|---|
|B15 초기 기획|5개 사용자군·60상황·12몸짓, MuJoCo+Gymnasium+SB3 PPO, 버전/승인 배포, NVIDIA AI Agent 검토가 요청된 범위. 이번 동기화에서 초기 Excel/문서 원본과 전체60상황 학습 완료는 검증하지 않음|
|R3 → R4 13축|어깨 배치·몸통·목/상박 구조 변경 후 12사례 PPO 타이밍 학습. 수동 사례 목표 기반 contextual bandit이며 영상 직접 모방/토크 정책이 아님|
|R4 13축 평가|기존 보고서: 3시드×3072 선택, 108조건 평가, seed11 선택. 평균 시간3.581초, 추종RMSE0.797도, 근사형상 접촉조건0. 실물 안전/사용자 자연성 입증 아님|
|R5 얼굴·음성/ChatGPT|13축 영상에서 기존 R5 88프레임 해시 확인, 한국어 합성음성. 대화 어댑터 로컬/모의9시험, 실제 API 미검증. 신규10축에 자동 이식되지 않음|
|최신 R4 10축|GLB3개 수동 미리보기, 하체353.9→327.4mm. 제조 CAD 아님. 13축 정책 및 과거R3 정책 직접 적용 불가; 신규 재학습 필요|
|교감|접촉확인·해제·정지래치·카메라 방향 로직. 실제 센서·순응제어·표시/TTS 미연결|
|자율주행|명시적 단일목표/선택ID 따라가기, A*, 대상분실/접촉/센서장애 정지. 4개 합성 시나리오, 실제 SLAM/사람추적/모터 미연결|
|이번 재검증|Python 자동시험 10+12+2=24개 통과. 기존 동영상/물리학습을 이번에 재실행한 것은 아님|

## 실행
이 폴더에서 실행:
```text
python -m pip install -r requirements.txt
python src/test_interaction.py
python navigation/src/test_navigation.py
python navigation/src/test_coordinator.py
```
모델 검증/재생성/렌더링에는 아래 전체 패키지의 models, assets, 대형 결과 JSON이 필요합니다. 전체 ZIP의 T02_M2_R4_10DOF 폴더 내용을 이 폴더에 합치십시오. 영상 생성에는 ffmpeg, 모델 렌더링에는 EGL/OpenGL이 필요합니다. 카메라 코드는 명시 실행 시 실제 카메라를 엽니다.

## 원본 산출물
아래 링크는 기존 접근 권한이 필요하며 공개 권한을 새로 부여하지 않습니다. 저장소에는 소스/설정/문서/검증요약을 보관하고, 바이너리·대형 궤적은 원본 패키지에서 제공합니다. ARTIFACT_MANIFEST.json은 원본 파일 SHA256 목록입니다.
- [최신 전체 ZIP](https://chatgpt.com/library?file_id=libfile_c2d9959164048191a04a787d842aa904&account_id=personal)
- [최신 GLB](https://chatgpt.com/library?file_id=libfile_ea13203320408191b08687fda69a15ca&account_id=personal)
- [하체/모터 비교 그림](https://chatgpt.com/library?file_id=libfile_5a26c20080388191b39d8e88a5f1500e&account_id=personal)
- [자율주행 30초 영상](https://chatgpt.com/library?file_id=libfile_d9ef3b4d5d64819184a4f11cf6541718&account_id=personal)
- [이전 R4 13축 학습 패키지](https://chatgpt.com/library?file_id=libfile_91df92f1e4d88191968a3de7c0e70f02&account_id=personal)
- [이전 R4 13축 영상](https://chatgpt.com/library?file_id=libfile_4d6a016891248191aae4c1aa9b490b0a&account_id=personal)
- [이전 R4 13축 학습 보고서](https://chatgpt.com/library?file_id=libfile_b86f8c4a8320819181795b578440f6fd&account_id=personal)

## 후속 작업
|Jira|범위|
|---|---|
|[KR1-1160](https://lumira077.atlassian.net/browse/KR1-1160)|시제품 디지털 증적 정리|
|[KR1-1161](https://lumira077.atlassian.net/browse/KR1-1161)|새10DOF MuJoCo/PPO 재학습|
|[KR1-1162](https://lumira077.atlassian.net/browse/KR1-1162)|제조CAD/내부배치/안정성|
|[KR1-1163](https://lumira077.atlassian.net/browse/KR1-1163)|교감센서/순응제어/표정음성 실기|
|[KR1-1164](https://lumira077.atlassian.net/browse/KR1-1164)|주행센서/SLAM/대상추적/실기|

실물 승인에는 모델/정책/설정 해시, 장비/펌웨어/캘리브레이션, 시험 결과, 검토자 승인과 롤백 버전을 함께 기록합니다. 현재 시뮬레이션 승인은 실물 배포 승인이 아닙니다.
