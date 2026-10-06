# [F2068-S03] OTA 소프트웨어 업데이트 통합·보안·부하·복구 시험

Jira: https://lumira077.atlassian.net/browse/KR1-491

정상/예외/경계조건·실제 통합 검증 계획·근거/재시험: 서명·hash·호환성·version·전원/안전 preflight와 A/B 설치를 설계

데이터: manifest·signature ref·digest·HW revision·slot

검증: 서명위조·다운그레이드·전원단절·용량부족

지표: 검증 실패 차단·부팅 성공·복구시간

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
