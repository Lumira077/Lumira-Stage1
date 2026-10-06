# [F2164-S02] Fleet 최소 Metadata·Privacy·Security Policy 보호기능·통제 로직 구현

Jira: https://lumira077.atlassian.net/browse/KR1-581

핵심 서비스/adapter 계획·재현 환경·구현 범위와 미연동 표시: fleet 최소 metadata와 목적/보유/접근·raw 비전송을 구성

데이터: metadata allowlist·consent epoch·tenant·retention

검증: raw 영상/대화/집배치·cross-tenant·철회

지표: 원문전송 0건·삭제전파·접근검증

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
