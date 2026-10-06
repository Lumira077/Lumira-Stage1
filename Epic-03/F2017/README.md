# [F2017] 대화 내용 기반 감정 추정

Jira: https://lumira077.atlassian.net/browse/KR1-154

대화의 자기보고와 의미/문맥을 구분하여 감정 후보·근거·불확실성을 제공하고 부정·인용·타인·위기 문맥을 별도로 검증한다.

활성 사용자/epoch·turn id·locale·bounded text·문맥 범위·자기보고/추론 origin·모델/prompt 버전·확률 및 근거 metadata. 원문 기본 비저장; 기억/프로필은 동의 범위 내 참조.

F2009 전사/F2011 활성 turn → text emotion adapter → EmotionObservation; F2014 의미 안전성/위기 정책에 별도 연결. 감정 label을 진단·긴급 신고 근거로 직접 사용하지 않는다.

## 단계별 개발
- 부정/인용/반어/타인/문맥·다국어 label 기준과 위기 신호 경로·학습/평가 분할을 명세화한다.
- 현재 SelfReport는 한국어/영어 8개 명시 자기보고 문장을 exact-match 처리한다. 확률은 fixture이며 calibrated confidence가 아니다. 실제 의미/문맥 분류기는 후속 adapter다.
- 부정·인용·타인·반어·언어·age subgroup의 macro-F1·ECE·context false positive·위기 경로 회귀를 검증한다.
- 원문 비저장·동의/기억 접근 제한·모델/prompt 변경 회귀와 사용자 정정 흐름을 검증한다.

## 검증·제한

문맥별 macro-F1·ECE·self-report/추론 구분률·부정/타인 오탐·unknown·위기 경로 false positive/negative(별도 검증)

실제 sentiment/context/위기 의미 분류기·LLM·동의된 대화 dataset·사용자 연구 미연결. exact-match의 unknown은 실제 위기 감지 실패를 해결한 것으로 간주하지 않는다.

S01 계약/평가 기준 검토, S02 실제 모델/서비스 및 재현 버전, S03 동의된 subject-separated 평가·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-03/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 11개 합성 입력 시험. 실제 모델/카메라/마이크/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/epoch/quality를 공급한다; 실제 인증·quality classifier가 아니다.

도구 참조: [Transformers text classification](https://huggingface.co/docs/transformers/tasks/sequence_classification) — 후속 후보; 미설치/미연결.
