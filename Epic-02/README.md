# EPIC-02 AI 대화 및 음성 인터랙션

Jira: https://lumira077.atlassian.net/browse/KR1-42

20개 Feature·80개 Sub-task의 설계와 실행 가능한 로컬 핵심 로직을 제공한다. Python 3.11 이상, 표준 라이브러리만 사용한다.

```
python Epic-02/runtime/run.py
python Epic-02/runtime/demo.py
python Epic-02/F2205/F2205-S04/assess.py Epic-02/runtime/evidence/report.json
```

각 S01은 설계 계약, S02는 Feature별 runtime entrypoint, S03은 자동 시험, S04는 출시 판단 초안이다. 실제 공통 코드는 runtime/core.py에 있으며 각 Feature 문서에 심볼·시험·미연결 범위를 표시했다. GitHub Actions는 source SHA를 담은 report.json과 Epic-01 회귀시험 증적을 Artifact로 저장한다.

## 구현 경계

- 실제 Cloud API 호출 0건. Gateway는 openai_sample/gemini_sample 가상 Provider다. ChatGPT/Google 계정·토큰·가격·quota와 연결된 서비스가 아니다.
- WakeGate는 detector score를 소비하고 TranscriptAssembler는 이미 전사된 partial/final 이벤트를 조립한다. 음성 인식 모델 실행이나 정확도 검증이 아니다.
- AudioLab은 채널 평균·고정 계수 subtraction·주어진 delay의 기하 계산이다. adaptive AEC·TDOA 추정·실제 Beamforming 품질을 제공하지 않는다.
- LocalModelGate는 manifest/hash 문자열 형식과 예시 자원 한계만 검사한다. 실제 모델 파일 무결성·라이선스·NPU 지원·추론은 별도 확인해야 한다. llama.cpp CPU/GPU 실행이 RK3588 NPU 실행을 의미하지 않는다.
- 개인정보/위험 분류·동의·계정별 권한은 신뢰된 호출자가 제공하는 태그/값이다. 실제 분류기·인증·동의 epoch 이벤트·PII 익명화는 미구현이다. 위험 태그 기반 gate는 완전한 의미 안전성 검사를 대신하지 않는다.
- Context는 합성 fixture lexical 검색, 세션/예산/metrics는 process-local 메모리다. 실제 F2002/F2003·분산 인증·예약/청구·삭제·복귀 이벤트는 미연결이다.
- Dialogue는 정책·프라이버시·신뢰된 위험 태그·가상 Gateway·세션 fence를 연결한다. 생성 후 실제 의미 안전 검사와 streaming cancel은 별도 adapter가 필요하다. 모델 생성 중 사용자 전환은 출력 전 epoch 재검사로 차단한다.
- Cancel ACK는 테스트 입력이다. 실제 오디오/모터 큐의 정지 확인을 뜻하지 않는다. 실제 안전 제어기와 F2021(KR1-175) 취소 계약을 연결해야 한다.
- Credit은 예시 정수 단위, 지연/온도/score 임계치는 예시값이다. 제품 승인 목표·실물 성능·실제 비용이 아니다. 실패하거나 usage가 불명확한 실제 요청의 환불 정책은 Provider billing 계약에 따라 결정한다.
- 실사용 참가자 0명, 실기 시험 미실시, release_ready=false. S03/S04 전체 완료로 판정하지 않는다.

## 자료·일정 차이

현재 Jira와 첨부 상세 Feature 목록(20개/3페이지)을 기준으로 한다. 예전 7 Feature 이미지와 요약 이미지의 일부 기능군/번호는 최신 상세 목록과 불일치한다. 예: F2126은 현재 AEC·Beamforming·DOA이며 안전 대화 정책은 F2014다. 기존 이미지를 삭제하지 않고 차이를 명세에 기록한다.

KR1-42 종료일은 2028-05-31이다. F2208/F2212/F2122는 상세 첨부상 2028-07-31까지, F2123은 2029-10-31까지로 범위·출시/OTA 단계 조정이 필요하다. 실제 Jira 날짜와 책임자 배정은 변경하지 않는다.

## 개입 필요 및 추가 Tool 링크

tools.json과 각 Feature README의 공식 문서/소스 링크는 후속 연결 후보이며 설치·계정 연결 완료를 뜻하지 않는다.

1. Cloud Provider·모델·승인 사용지역/데이터 정책·호출 한도/예산과 Secret 설정. 비밀키를 Jira Description이나 소스에 넣지 않는다.
2. 로컬 보드·RAM·OS·runtime·모델 hash/라이선스·NPU 지원 범위 확정 및 실물 benchmark 접근.
3. 마이크 배열 geometry/driver·스피커 loopback·카메라·ROS2/실제 TTS·취소/stop ACK adapter 제공.
4. 연령/위기/PII 분류 정책, 실제 사용자별 인증·동의/삭제 이벤트, 실제 요금제/credit/가격 서비스 연결.
5. 한국어·영어·고령/아동 등 평가 대상/동의된 음성 데이터, FAR/FRR/CER/WER·지연·AEC/DOA·비용 목표 승인 및 Q1/R1 검토.
6. Epic과 하위 장기 확장 Feature의 일정/출시 단계 불일치 조정.
