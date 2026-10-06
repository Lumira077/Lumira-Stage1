# [F2225-S04] RK3588 SoM 양산 Carrier Board 개발 DFM·Design Freeze·양산 인계

Jira: https://lumira077.atlassian.net/browse/KR1-831

공차/조립/검사/DFM·Design Freeze·양산/정비 인계: DVT 이후 RK3588 SoM Carrier의USB/MIPI/HDMI/DDR관련SI·Ethernet/M.2·전원/boot를 설계

데이터: SoM pinout·carrier revision·interface·power·test point

검증: SI/EMI·부팅실패·OTA차단·thermal

지표: interface bring-up·SI/EMI·boot·공급gate

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
