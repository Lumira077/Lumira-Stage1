# [F2018] 멀티모달 감정 융합

Jira: https://lumira077.atlassian.net/browse/KR1-159

얼굴·음성·텍스트의 시간/사용자/신뢰도 계약을 맞추고 누락·충돌을 처리해 설명 가능한 감정 후보를 통합한다.

EmotionObservation(owner,epoch,modality,timestamp,scores,quality,model_version,origin,schema), modality coverage·합의/충돌·후보/unknown·evidence; 원본 media/text 제외.

시간 정렬·owner/epoch 검증 → reliability-weighted score fusion → inferred_not_confirmed result. F2010 대화/표현에는 감정 후보와 확인 질문만 전달하며 실행 명령을 생성하지 않는다.

## 단계별 개발
- label ontology·개인 기준·모달리티별 calibration/품질·시간 허용오차·누락/충돌/보류 정책을 정의한다.
- 현재 Fusion은 2개 이상 유효 modality의 가중평균·0.3초 skew 예시 기준·conflict unknown과 evidence projection을 구현한다. cross-user/epoch/duplicate는 거절한다.
- 동기화 지연·한 modality 누락·품질 저하·모달리티 충돌·사용자 전환/동의 철회·calibration 및 실제 end-to-end 지연을 검증한다.
- 확인 질문/사용자 정정·unknown 기본 상호작용·개인화 편향·설명 수용성과 rollback 정책을 검증한다.

## 검증·제한

fusion macro-F1/UAR·ECE·coverage/selective risk·missing/conflict unknown·시간 skew·p50/p95 지연·타 사용자 결합 0건

실제 3 modality adapter/calibration·ROS/event bus/F2010 표현 연결·physical latency 미연결. example 품질/시간/confidence threshold는 운영 승인 대상.

S01 계약/평가 기준 검토, S02 실제 모델/서비스 및 재현 버전, S03 동의된 subject-separated 평가·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-03/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 12개 합성 입력 시험. 실제 모델/카메라/마이크/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/epoch/quality를 공급한다; 실제 인증·quality classifier가 아니다.

도구 참조: [ONNX Runtime](https://onnxruntime.ai/docs/) — 후속 후보; 미설치/미연결.
