# [F2225-S01] RK3588 SoM 양산 Carrier Board 개발 요구사양·Interface·BOM 설계

Jira: https://lumira077.atlassian.net/browse/KR1-828

성능/환경/안전·전기/기구/통신 ICD·목표 BOM 검토: DVT 이후 RK3588 SoM Carrier의USB/MIPI/HDMI/DDR관련SI·Ethernet/M.2·전원/boot를 설계

데이터: SoM pinout·carrier revision·interface·power·test point

검증: SI/EMI·부팅실패·OTA차단·thermal

지표: interface bring-up·SI/EMI·boot·공급gate

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
