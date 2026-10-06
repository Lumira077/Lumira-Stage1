# F2013-S01

Jira: https://lumira077.atlassian.net/browse/KR1-114

- locale 목록·fallback·언어 고정·code switching·unsupported 안내·언어별 안전 정책 정의
- LanguageProfile: selected_locale, supported_stt/llm/tts, catalog_version; locale에 따라 prompt/voice 매핑의 필수값·민감도·보존기간·권한·revision/epoch를 표로 정의한다.
- LanguageResolver.choose(requested,capabilities) → locale; 프로필은 F2002 권위 값의 정상·오류·취소·stale 입력 계약 및 시험 데이터 분할을 명세화한다.

산출물: 요구사항·데이터/인터페이스 계약·예외표·시험 기준

상위 Feature 완료조건: 출시 언어별 STT/응답/TTS/화면·콘텐츠가 일관되고 임의 언어 전환으로 동의·정책이 바뀌지 않는다.

현재 제한: 현재 한영 locale 지원 계약만 구현; 실제 다국어 모델·번역/언어 감지·음성 품질 평가 필요

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
