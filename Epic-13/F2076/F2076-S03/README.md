# [F2076-S03] 관절·주행 비상 정지 Fault Injection·침투·안전 시험

Jira: https://lumira077.atlassian.net/browse/KR1-557

정상/예외/경계조건·실제 통합 검증 계획·근거/재시험: 관절/주행 stop latch·local 우선순위·물리 ACK·검토 reset을 연결

데이터: stop source·safety epoch·velocity·torque feedback

검증: AI hang·통신단절·늦은명령·자동재시작

지표: 정지시간/거리·안전상태·restart 차단

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
