# [F2040-S04] 동적 장애물 회피 실환경 임무 검증·Parameter Freeze

Jira: https://lumira077.atlassian.net/browse/KR1-307

실환경 반복임무·Parameter Freeze·운용제한/rollback: 사람/반려동물/가구/낙하위험의 costmap 반영과 안전한 감속·정지를 처리

데이터: obstacle·velocity·clearance·cliff·sensor age

검증: 가림·급접근·낙하센서 고장·맵 외 영역

지표: 접촉/낙하 0건·정지거리·최소거리

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
