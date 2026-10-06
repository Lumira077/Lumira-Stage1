# [F2041-S04] 자동 복귀 및 무선 충전 도킹 실환경 임무 검증·Parameter Freeze

Jira: https://lumira077.atlassian.net/browse/KR1-312

실환경 반복임무·Parameter Freeze·운용제한/rollback: 저전력 복귀·dock 탐색/정렬·충전 확인·횟수 제한 재시도를 상태기로 구성

데이터: SOC·dock pose·contact·charge feedback·retry

검증: dock 막힘·false contact·BMS fault·재시도 소진

지표: 도킹 성공률·소요시간·충전 실제 ACK

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
