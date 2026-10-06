# [F2150-S02] 민감 IoT 기기 권한·재확인·감사 보호기능·통제 로직 구현

Jira: https://lumira077.atlassian.net/browse/KR1-576

핵심 서비스/adapter 계획·재현 환경·구현 범위와 미연동 표시: 도어/락 등 민감 IoT의 user/device scope·재확인·감사·취소를 구성

데이터: device·action·one-time confirmation·scope·expiry

검증: 낯선명령·replay·권한변경·원격취소

지표: 미승인 실행 0건·결과 감사·취소반영

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
