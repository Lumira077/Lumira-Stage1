# F2010-S01

Jira: https://lumira077.atlassian.net/browse/KR1-99

- system policy/사용자 입력/검색 근거를 구분하고 response·tool proposal·TTS 계약 정의
- DialogueRequest: turn_id, epoch, language, context_refs, decision; Reply: text, backend, policy_version, output_plan의 필수값·민감도·보존기간·권한·revision/epoch를 표로 정의한다.
- Dialogue.answer(request) → safe reply; F2021 text/voice plan 및 cancel token 연결의 정상·오류·취소·stale 입력 계약 및 시험 데이터 분할을 명세화한다.

산출물: 요구사항·데이터/인터페이스 계약·예외표·시험 기준

상위 Feature 완료조건: 실제 다중 Provider에서 문맥이 유지되고 모델별 지연·비용·실패·안전 출력 증적이 남는다.

현재 제한: 현재 고정 응답 가상 Gateway 통합; 실제 자연어 생성·prompt 평가·TTS·기억/콘텐츠 Tool 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
