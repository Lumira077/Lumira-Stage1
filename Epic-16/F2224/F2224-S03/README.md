# [F2224-S03] STM32 Motion·I/O·Safety Controller Board Bench·통합·안전 시험

Jira: https://lumira077.atlassian.net/browse/KR1-825

Bench·통합·열/소음/전원/내구/EMI·고장안전 시험: STM32G4/H7 Motion/I/O/Safety 보드의CAN-FD/RS485·timer·enable·fault를 설계

데이터: MCU firmware·ICD·timer·I/O·watchdog

검증: bus off·AI hang·sensor fault·reset glitch

지표: jitter·독립정지·fault isolation·I/O

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
