# [F2016] 음성 톤 기반 감정 추정

Jira: https://lumira077.atlassian.net/browse/KR1-149

음성의 pitch·속도·energy·침묵 등 운율 단서를 추출하고 잡음·겹말·로봇 음성 영향을 구분해 감정 후보를 제공한다.

사용자/동의 epoch, audio window timestamp, sample rate/channel, voice activity·pitch/rate/energy/silence 특징, noise/clipping/overlap/TTS echo quality, 모델/언어/label schema 버전. 원본 음성 기본 비저장.

AudioFrame/quality → prosody extractor → external emotion model → EmotionObservation; F2126 reference/AEC 및 F2009 STT 시간축 연동 계약. 실제 driver/stream 미구현.

## 단계별 개발
- 마이크·sample rate·window/VAD·잡음/echo·언어/화자별 특징/평가 입력 계약을 정의한다.
- 현재 AudioFeatures는 normalized synthetic PCM의 RMS/zero-crossing/silence/clipping만 계산하며 ObservationGate("audio")가 외부 점수의 quality/시간을 검증한다. pitch/rate·실제 감정 추론은 후속 구현한다.
- 잡음/SNR·겹말·마이크 거리·언어/연령 조건별 UAR/macro-F1·calibration·지연·silent/echo unknown을 평가한다.
- 마이크 고장/철회 복구·원본 비저장·품질 drift와 모델/장비 변경 rollback을 검증한다.

## 검증·제한

조건별 UAR/macro-F1·ECE·SNR/음성 coverage·silence/echo 오탐·unknown·p50/p95 end-to-end 지연

실제 마이크/VAD/pitch/rate/echo·감정 모델 및 consented 평가 음성 미연결. RMS·zero crossing만으로 감정 label을 판정하지 않는다.

S01 계약/평가 기준 검토, S02 실제 모델/서비스 및 재현 버전, S03 동의된 subject-separated 평가·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-03/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 12개 합성 입력 시험. 실제 모델/카메라/마이크/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/epoch/quality를 공급한다; 실제 인증·quality classifier가 아니다.

도구 참조: [SpeechBrain classifier API](https://speechbrain.readthedocs.io/en/latest/API/speechbrain.inference.classifiers.html) — 후속 후보; 미설치/미연결.
