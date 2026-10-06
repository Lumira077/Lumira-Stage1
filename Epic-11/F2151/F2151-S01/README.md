# [F2151-S01] Stage2 User & Space Onboarding App 사용 흐름·Data Model·API 설계

Jira: https://lumira077.atlassian.net/browse/KR1-463

요구사항·데이터/API·오류/동의·시험 기준 및 검토 초안: Stage2 계정/로봇/네트워크/공간/사용자/IoT 온보딩 재개 흐름을 구성

데이터: wizard version·step·map ref·owner epoch

검증: 중단·재개·기기 복구·로봇과 상태 불일치

지표: 필수 설정 완료율·복구 일치·동의 보존

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
