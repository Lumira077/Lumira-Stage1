# [F2092-S04] Safety MCU·Motor Interface·I/O 제어 Architecture DFM·Design Freeze·양산 인계

Jira: https://lumira077.atlassian.net/browse/KR1-726

공차/조립/검사/DFM·Design Freeze·양산/정비 인계: Linux AI와 Safety MCU의 CAN-FD/RS485·enable/watchdog·I/O 책임을 분리

데이터: ICD·message seq·fault·hardware enable·MCU version

검증: AI freeze·bus off·restart·watchdog

지표: 독립정지·통신무결성·제어주기

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
