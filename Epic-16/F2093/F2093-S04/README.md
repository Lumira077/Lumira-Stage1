# [F2093-S04] 목·팔·허리·손 구동 HW 및 Actuator 선정 DFM·Design Freeze·양산 인계

Jira: https://lumira077.atlassian.net/browse/KR1-731

공차/조립/검사/DFM·Design Freeze·양산/정비 인계: DYNAMIXEL 후보의 torque/speed/current/heat/size와 BLDC 전환 gate를 검증

데이터: actuator spec·load·gear·torque curve·bench

검증: stall·열·소음·수명·끼임

지표: torque margin·추종·열·소음·수명

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
