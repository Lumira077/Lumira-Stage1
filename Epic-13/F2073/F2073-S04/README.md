# [F2073-S04] 인증·권한·기기 신뢰 Evidence·Compliance·Release 승인

Jira: https://lumira077.atlassian.net/browse/KR1-543

운영 지표·검토/배포·중단/rollback·완료증적 기준: 사용자/기기 인증·tenant/owner scope·RBAC·세션 revoke를 구성

데이터: principal·role·device/tenant·token ref·epoch

검증: cross-tenant·replay·expired·owner 변경

지표: 권한우회 0건·revoke 지연·session 감사

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
