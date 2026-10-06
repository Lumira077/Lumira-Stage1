# [F2144-S04] Force·Slip 기반 Adaptive Soft Grasp 실환경 임무 검증·Parameter Freeze

Jira: https://lumira077.atlassian.net/browse/KR1-363

실환경 반복임무·Parameter Freeze·운용제한/rollback: force/slip feedback로 힘 증분·재파지·중단을 결정

데이터: force·slip·max force·force rate·feedback age

검증: 계속 slip·과압·센서 stale·파손 위험

지표: slip 회복률·힘 overshoot·낙하/파손

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
