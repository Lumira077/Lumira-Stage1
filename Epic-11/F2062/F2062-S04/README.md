# [F2062-S04] 일정·복약·콘텐츠 원격 설정 운영 Dashboard·SLA·Release

Jira: https://lumira077.atlassian.net/browse/KR1-451

운영 지표·검토/배포·중단/rollback·완료증적 기준: 일정/복약/콘텐츠의 versioned 설정·검증·device ACK를 구성

데이터: settings version·patch·request id·ACK

검증: 동시변경·오프라인 큐·구버전 ACK·재시도

지표: 충돌처리·동기화 지연·일관성

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
