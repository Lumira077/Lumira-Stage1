# [F2096-S04] Battery·BMS·전용 전원·안전 Board 설계 DFM·Design Freeze·양산 인계

Jira: https://lumira077.atlassian.net/browse/KR1-746

공차/조립/검사/DFM·Design Freeze·양산/정비 인계: Battery/BMS·24/12/5/3.3V 예시 rail·e-fuse·역극성·종료 sequencing을 설계

데이터: chemistry·ratings·rail·fault·power budget

검증: 과전류·brownout·AI hang·충전고장

지표: 보호차단·종료ordering·rail 측정

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
