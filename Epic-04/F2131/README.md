# [F2131] Stage2~3 리얼형 Face R&D 옵션

Jira: https://lumira077.atlassian.net/browse/KR1-210

Stage 2~3 리얼형 얼굴의 GPU/립싱크/Uncanny Valley/권리·개인정보를 비교 평가하여 제품 채택 또는 연구 지속을 결정한다.

renderer/model/asset hash/license·GPU/RAM/온도·FPS/frame p95·립싱크 skew·participant count/age·discomfort·rights/privacy evidence·go/no-go decision.

측정된 성능/실사용 평가 metadata → R&D evidence gate → CTO/Q1 제품 적용 검토. Stage 1 기본 2D 캐릭터 유지; gate 통과는 production 승인과 구분한다.

## 단계별 개발
- 리얼형/2D 비교·Edge GPU budget·가독성/불쾌감·동의/초상권·no-clone·성능/윤리/비용·go/no-go 프로토콜을 설계한다.
- 현재 FaceResearchGate는 supplied 측정 metadata를 예시 budget/사용자 수·rights/privacy gate로 평가하며 production_enabled=false를 유지한다.
- 실제 GPU/renderer·립싱크·발열/RAM·장시간·다양한 사용자 불편/선호·권리/개인정보와 2D fallback을 평가한다.
- 사용자/하드웨어 증적·비용/권리/위험 비교와 CTO/Q1의 채택/연구 지속 결정·선택적 OTA/rollback을 기록한다.

## 검증·제한

GPU/RAM/온도·FPS/render p95·lip-sync skew·discomfort/Uncanny Valley·실사용 sample·license/privacy·비용

실제 renderer/실존 인물 asset·GPU·participant study·비용/권리/privacy review 없음. 예시 threshold/가상 측정은 실제 R&D 연구 결과가 아니다.

S01 계약/평가 기준 검토, S02 실제 renderer/TTS/제어 adapter 및 재현 버전, S03 실제 장비의 표현 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-04/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 8개 합성 입력 시험. 실제 TTS/디스플레이/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/clearance/rights/intent를 공급한다; 실제 인증·환경/권리/의미 검증 서비스가 아니다.

도구 참조: [Qt Quick (후속 renderer 후보)](https://doc.qt.io/qt-6/qtquick-index.html) — 후속 후보; 미설치/미연결.
