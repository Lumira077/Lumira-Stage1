# [F2141-S04] Safety MCU 독립 Torque 차단·검증 Evidence·Compliance·Release 승인

Jira: https://lumira077.atlassian.net/browse/KR1-573

운영 지표·검토/배포·중단/rollback·완료증적 기준: Safety MCU의 독립 watchdog·torque disable·feedback·reset을 검증

데이터: MCU heartbeat·hardware enable·feedback·fault

검증: Linux freeze·bus 단절·sensor fault·reset glitch

지표: 독립 차단시간·실제 torque 0·fault coverage

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
