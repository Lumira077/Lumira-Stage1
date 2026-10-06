# [F2072-S04] 전송·저장 데이터 암호화 Evidence·Compliance·Release 승인

Jira: https://lumira077.atlassian.net/browse/KR1-538

운영 지표·검토/배포·중단/rollback·완료증적 기준: TLS/mTLS·저장 암호화·key lifecycle·rotation/복구를 설계

데이터: cipher policy·key ref·cert expiry·encryption envelope

검증: 잘못된 cert·revoked key·평문 cache·backup

지표: 평문 노출 0건·rotation 성공·복호화권한

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
