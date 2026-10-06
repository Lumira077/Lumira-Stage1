# [F2158-S01] Fashion·Accessory 상품·Catalog 운영 사용 흐름·Data Model·API 설계

Jira: https://lumira077.atlassian.net/browse/KR1-646

요구사항·데이터/API·오류/동의·시험 기준 및 검토 초안: Fashion/Accessory SKU·모델 호환·재고·NFC·테마권리를 관리

데이터: SKU·compatibility·NFC tag ref·stock·license

검증: 비호환·위조tag·재고0·테마권리 만료

지표: catalog 정합성·인증·적용이력

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
