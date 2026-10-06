# [F2026] 얼굴 등록 및 사용자 인식

Jira: https://lumira077.atlassian.net/browse/KR1-216

동의된 얼굴 등록/삭제와 등록 사용자 후보 인식을 제공하며 미등록/불확실/위조 의심 시 기본 게스트로 처리한다.

owner/동의 epoch·authorized enrollment·model/hash/license·face quality/live 결과·embedding dimension/version·similarity/margin·등록/삭제 증적. 얼굴 template는 생체정보로 취급하며 원본 영상 기본 비저장·Local 암호화 저장 제안.

F2001 등록/F2002 동의 → face detector/alignment/embedding → registry match candidate → F2004 활성 사용자 확인. 후보는 인증/권한 허용과 구분하며 실제 profile 공개에는 별도 인증·확인이 필요하다.

## 단계별 개발
- 등록 sample 품질/수·동의·owner 결합·미등록/동점 처리·model dimension/version·등록/철회/삭제/backup purge 및 FAR/FRR 기준을 설계한다.
- 현재 FaceRegistry는 8차원 fixture vector 정규화·메모리 등록·cosine similarity/margin·version/시간/live flag 검사·철회 epoch 재등록 거절을 구현한다. 실제 detector/embedding/liveness/auth는 후속이다.
- 실제 동의된 subject-separated dataset의 FAR/FRR/ROC/EER·미등록/동점·조명/거리/가림/연령·사진/재생 위조·철회/삭제·지연을 검증한다.
- 등록/정정/삭제 UX·게스트 fallback·실제 암호화/backup purge·접근 제어/운영 지표·model migration/rollback을 확정한다.

## 검증·제한

FAR/FRR·ROC/EER·등록/unknown coverage·조명/각도/거리/연령 subgroup·p50/p95·위조 방어·타 사용자 정보 공개/철회 후 매칭 0건

실제 camera/YuNet/SFace/embedding/liveness·production auth/동의 이벤트·암호화 DB/backup purge·사용자 dataset 미연결. fixture 8차원/threshold는 실제 모델 계약/품질이 아니다. 후보를 authenticated=false로 반환한다.

S01 계약/평가 기준 검토, S02 실제 인식 모델/센서/제어 adapter 및 재현 버전, S03 실제 장비의 인지/추적 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-05/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 11개 합성 입력 시험. 실제 카메라/인식 모델/센서/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/epoch/quality/live/VAD/echo를 공급한다; 실제 인증·동의·센서/분류 서비스가 아니다.

도구 참조: [OpenCV FaceDetectorYN/FaceRecognizerSF](https://docs.opencv.org/4.x/d0/dd4/tutorial_dnn_face.html) — 후속 후보; 미설치/미연결.
