# F2024-S02

Jira: https://lumira077.atlassian.net/browse/KR1-192

현재 GestureSelector는 trusted greeting/agreement/comfort fixture를 wave/nod/still로 매핑하고 quiet/clearance/stop/low confidence에서 still proposal을 반환한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 renderer/TTS/제어 adapter 및 재현 버전, S03 실제 장비의 표현 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: intent-gesture 적합률·금지/unknown 제스처·unsafe proposal 0건·사용자 선호/불편·selection p95

제한: 실제 의미 classifier/LLM·profile/emotion·거리/clearance 인식 연결 없음. emotion 인자는 현재 예약된 계약으로 선택에 반영하지 않으며 강도/개인화는 추가 구현한다.

증적: source/model/asset/hash/license/config/policy version, device/calibration, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
