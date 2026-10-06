# [F2095-S01] 얼굴 Display·Touch LCD·Audio HW 구축 요구사양·Interface·BOM 설계

Jira: https://lumira077.atlassian.net/browse/KR1-738

성능/환경/안전·전기/기구/통신 ICD·목표 BOM 검토: Face/Touch display·Class-D/speaker chamber·AEC reference 경로를 설계

데이터: display resolution·touch HID·audio path·amplifier

검증: 발열·공진·volume·touch fault·Mic leakage

지표: frame latency·음질·AEC reference·온도

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
