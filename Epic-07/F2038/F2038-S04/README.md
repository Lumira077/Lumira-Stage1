# [F2038-S04] 자기 위치 추정 실환경 임무 검증·Parameter Freeze

Jira: https://lumira077.atlassian.net/browse/KR1-297

실환경 반복임무·Parameter Freeze·운용제한/rollback: map 기반 pose/covariance를 추정하고 위치 상실·kidnapped robot 재초기화를 처리

데이터: pose·covariance·map revision·TF age

검증: 잘못된 지도·재배치·센서 stale·confidence 저하

지표: 위치 오차·재위치추정 시간·오복구

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
