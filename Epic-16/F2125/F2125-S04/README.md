# [F2125-S04] 4~6채널 MEMS Mic Array HW DFM·Design Freeze·양산 인계

Jira: https://lumira077.atlassian.net/browse/KR1-786

공차/조립/검사/DFM·Design Freeze·양산/정비 인계: 4~6채널 MEMS Mic Array의 동기/beamforming/AEC/AGC/DOA 경로를 검증

데이터: channel map·sample rate·reference·DOA

검증: speaker leakage·fan/motor·channel dropout

지표: SNR·AEC/DOA 오차·동기·지연

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
