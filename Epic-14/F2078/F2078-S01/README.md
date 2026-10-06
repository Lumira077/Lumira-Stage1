# [F2078-S01] 콘텐츠 카탈로그 및 배포 사용 흐름·Data Model·API 설계

Jira: https://lumira077.atlassian.net/browse/KR1-626

요구사항·데이터/API·오류/동의·시험 기준 및 검토 초안: 콘텐츠 license·age band·검수·version·cache/rollback을 구성

데이터: content id·license·rating·version·manifest

검증: 권리만료·유해콘텐츠·손상파일·호환성

지표: 배포정합성·검수coverage·rollback

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
