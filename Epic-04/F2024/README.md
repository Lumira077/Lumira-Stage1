# [F2024] 대화 의미 기반 제스처 선택

Jira: https://lumira077.atlassian.net/browse/KR1-190

대화 의미·감정 후보·개인 선호·상황에 맞는 허용 제스처와 강도를 선택하고 위험/불확실 시 움직임을 보류한다.

bounded trusted intent tag/confidence·emotion candidate/unknown·profile/persona·quiet·clearance·stop state·allowed gestures·policy/version·reason.

F2010 intent/F2018 감정 후보·F2002 선호 → allowlist policy → GestureProposal → F2022 safety validation → F2023 timeline. 자유 생성 joint trajectory는 직접 실행하지 않는다.

## 단계별 개발
- intent-gesture mapping·연령/거리/quiet/피로·confidence·금지 제스처·표현 강도·우선순위 및 reason 계약을 정의한다.
- 현재 GestureSelector는 trusted greeting/agreement/comfort fixture를 wave/nod/still로 매핑하고 quiet/clearance/stop/low confidence에서 still proposal을 반환한다.
- 실제 intent classifier/감정 unknown/conflict·잘못된 의미/인용·사용자 변경·환경/접촉·안전 우선순위 회귀를 시험한다.
- 사용자 적합성/과도한 표현·정정/선호·문화/연령 조건별 이해·policy rollback을 검토한다.

## 검증·제한

intent-gesture 적합률·금지/unknown 제스처·unsafe proposal 0건·사용자 선호/불편·selection p95

실제 의미 classifier/LLM·profile/emotion·거리/clearance 인식 연결 없음. emotion 인자는 현재 예약된 계약으로 선택에 반영하지 않으며 강도/개인화는 추가 구현한다.

S01 계약/평가 기준 검토, S02 실제 renderer/TTS/제어 adapter 및 재현 버전, S03 실제 장비의 표현 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-04/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 8개 합성 입력 시험. 실제 TTS/디스플레이/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/clearance/rights/intent를 공급한다; 실제 인증·환경/권리/의미 검증 서비스가 아니다.

도구 참조: [Transformers classification 후속 intent 후보](https://huggingface.co/docs/transformers/tasks/sequence_classification) — 후속 후보; 미설치/미연결.
