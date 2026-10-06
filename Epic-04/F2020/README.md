# [F2020] 디스플레이 얼굴 표정 엔진

Jira: https://lumira077.atlassian.net/browse/KR1-170

감정·대화 상태를 눈·입·색상·표정 전환으로 표현하고 디스플레이에서 일관되게 재생한다.

expression id·intensity·smile/brow/mouth/gaze normalized pose, asset/policy version, resolution/FPS·turn/epoch·transition duration·state 우선순위.

ExpressionRequest → expression pose/interpolation → SVG/offline renderer. 실제 디스플레이 frame loop/Qt adapter 및 상태 event bus는 후속 연결.

## 단계별 개발
- neutral/happy/sad/listening/thinking/speaking 상태·색상/눈/입 파라미터와 가독성·transition·fallback·끼어들기 계약을 정의한다.
- 현재 FaceEngine은 pose 생성·선형 blend·입/눈 SVG 문자열 생성 및 color/숫자 검증을 구현한다. animation clock/frame compositor는 후속이다.
- 실제 LCD/OLED 해상도·프레임률·render p95·전환 latency·표정 가독성·오류 neutral/취소 reset을 검증한다.
- 대상 연령/거리별 표정 이해·선호·눈부심/피로·상태 이해를 평가하고 asset rollback을 확정한다.

## 검증·제한

표정/상태 이해율·transition 가독성·FPS/dropped frame·render p50/p95·취소 후 residual frame·장시간 발열

실제 디스플레이/GPU/Qt frame loop·blink/brow rendering·event bus·대상 사용자 가독성 평가 미실시. SVG 정적 샘플은 실기 FPS 검증이 아니다.

S01 계약/평가 기준 검토, S02 실제 renderer/TTS/제어 adapter 및 재현 버전, S03 실제 장비의 표현 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-04/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 9개 합성 입력 시험. 실제 TTS/디스플레이/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/clearance/rights/intent를 공급한다; 실제 인증·환경/권리/의미 검증 서비스가 아니다.

도구 참조: [Qt Quick (후속 renderer 후보)](https://doc.qt.io/qt-6/qtquick-index.html) — 후속 후보; 미설치/미연결.
