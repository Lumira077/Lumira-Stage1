# [F2130] Eye Gaze·Lip Sync·표정 동기화 고도화

Jira: https://lumira077.atlassian.net/browse/KR1-205

사용자 방향과 실제 발화 재생 시각에 맞춰 시선·입 모양·눈깜박임·표정 합성을 동기화하고 끼어들기 시 중단한다.

normalized gaze target/quality·owner/epoch·word/phoneme/viseme start/end·audio playback time·blink schedule·face mask/blend priority·cancel.

F2021 alignment/playback + 사용자 방향 → gaze/viseme pose → F2020 renderer/F2023 clock. 현재 supplied cues 기반 pose이며 actual camera/forced aligner 없음.

## 단계별 개발
- 사용자 방향/좌표계·gaze limit·viseme schema/언어·실제 playback clock·blink·표정 mask/priority·missing alignment fallback 계약을 설계한다.
- 현재 GazeLip은 normalized gaze bound·supplied closed/small/open cue 타이밍/겹침 검증과 mouth pose/취소 reset을 구현한다. blink는 false 기본값이다.
- 실제 TTS 음소/립싱크·gaze target·blink·frame clock·취소/late cue/skew·연령/언어 자연성을 검증한다.
- 과도한 응시/입모양 불편·눈 피로·접근성·camera 동의 및 alignment/asset rollback을 검토한다.

## 검증·제한

lip/audio skew p95·gaze error·blink 자연성·missing cue fallback·취소 residual·사용자 불편

actual tracking/TTS alignment·한국어 viseme mapping·blink generator·mask compositor·실제 display timing 미구현. Rhubarb는 후속 오프라인 후보로 live 한국어 품질 검증이 필요하다.

S01 계약/평가 기준 검토, S02 실제 renderer/TTS/제어 adapter 및 재현 버전, S03 실제 장비의 표현 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-04/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 9개 합성 입력 시험. 실제 TTS/디스플레이/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/clearance/rights/intent를 공급한다; 실제 인증·환경/권리/의미 검증 서비스가 아니다.

도구 참조: [Rhubarb Lip Sync 후속 offline 후보](https://github.com/DanielSWolf/rhubarb-lip-sync) — 후속 후보; 미설치/미연결.
