# F2026-S03

Jira: https://lumira077.atlassian.net/browse/KR1-219

실제 동의된 subject-separated dataset의 FAR/FRR/ROC/EER·미등록/동점·조명/거리/가림/연령·사진/재생 위조·철회/삭제·지연을 검증한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 인식 모델/센서/제어 adapter 및 재현 버전, S03 실제 장비의 인지/추적 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: FAR/FRR·ROC/EER·등록/unknown coverage·조명/각도/거리/연령 subgroup·p50/p95·위조 방어·타 사용자 정보 공개/철회 후 매칭 0건

제한: 실제 camera/YuNet/SFace/embedding/liveness·production auth/동의 이벤트·암호화 DB/backup purge·사용자 dataset 미연결. fixture 8차원/threshold는 실제 모델 계약/품질이 아니다. 후보를 authenticated=false로 반환한다.

증적: source/model/asset/hash/license/config/policy version, device/calibration, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
