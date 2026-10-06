# NAS DB 구축 현황 — 2026-10-06

**현재 상태: NAS 이미지 다운로드·전용 폴더·배포 파일 준비 완료. DB 관리자 자격 증명 생성 및 배포 작업 최종 실행 대기. DB 가동 완료가 아니다.**

[구성·운영 절차](../infra/nas-db/README.md)

| 구분 | 확인 결과 |
|---|---|
| NAS 로그인 | DSM에 실제 로그인하고 저장소·Docker 화면 확인 |
| 저장소 | SHR/Btrfs 풀 저하, 드라이브 1개 부족, 표시된 드라이브 1·2·4 정상, 스크럽 불가 |
| 볼륨 | 약 6.7TB / 10.5TB, 64% 사용 |
| 기존 컨테이너 | nginx 1개 실행 중, 다른 nginx 1개는 기존 bind mount 누락 오류; 변경 없음 |
| PostgreSQL 이미지 | Docker 검색 성공, 태그 조회 및 공식 URL 추가에서 레지스트리 쿼리 실패 |
| 이미지 다운로드 | 사용자 승인 후 root 수동 작업 1회 실행, 23:16:01~23:16:40 KST 정상 종료(0). Docker에 postgres:17-bookworm 445MB 등록 확인. 자동 활성화 OFF |
| 전용 폴더 | 볼륨1에 lumira-db 공유 폴더 생성, 일반 사용자 권한 추가 없음. Windows 네트워크 목록에서 숨김. 패키지 압축 해제 및 data 폴더, scripts/deploy-dsm.sh 확인 |
| 구현 파일 | CPU 1 / 메모리 1GiB / 연결20 / shared_buffers128MB, 3논리 DB, 포트 비공개 |
| 미완료 | DB 관리자 비밀 생성 및 컨테이너 배포 최종 실행, NAS 가동·영속성·외부 복원 |

다운로드용 root 수동 작업의 초기 자동 승인 차단은 사용자의 명시적 승인 후 해소되었다.
이미지 다운로드 작업은 성공했으며 자동 활성화는 계속 OFF다.

DSM 컨테이너 생성 마법사는 네트워크 목록 로딩에서 멈춰 배포에 사용하지 못했다.
브라우저 새로 고침으로 복구했으며, CPU/메모리 제한과 내부 네트워크를 그대로 적용하는
`scripts/deploy-dsm.sh`를 NAS에 업로드했다. 이 스크립트는 NAS 안에서 관리자 비밀을 생성하고,
실제 RepoDigest를 기록·사용하며, 3 DB 초기화와 동일 호스트 백업/복원까지 수행한다.
기존 컨테이너/네트워크/비밀/데이터가 있으면 덮어쓰지 않고 중단한다.

`Lumira DB - deploy synthetic test - manual` 작업 초안을 root/자동 활성화 OFF로 작성했다.
새 자격 증명을 생성하는 최종 단계이므로 사용자 직접 확인·실행을 위해 DSM 경고 창에서 대기한다.
아직 저장·실행하지 않았으며 실제 NAS DB 계정·컨테이너 생성도 미완료다.
실행 시 로그는 `/volume1/lumira-db/logs/deploy-<UTC시각>.log`에 남고 비밀번호는 기록하지 않는다.
비밀 파일은 NAS의 `secrets/db_admin_password`에만 권한 600으로 저장한다.

디스크 교체 전에는 이전 결정에 따른 재생성 가능한 합성 데이터 최소 시험만 준비한다.
실제 개인정보·협력사 기밀·부하 시험은 저장소 정상화 및 독립 백업 복원 확인 후 진행한다.

이 저장소의 CI는 별도 GitHub 시험 서버에서 패키지 초기화·자원·권한·재시작·논리 복원을 검증한다.
CI 성공은 NAS 설치, RAID 복구, 실기 연결 또는 독립 백업 성공의 증거가 아니다.

연결 Jira: KR1-472 / KR1-474 / KR1-475 / KR1-476 / KR1-494 / KR1-496.

## 별도 시험 서버 검증 결과

2026-10-06 GitHub Actions [37476807793](https://github.com/Lumira077/Lumira-Stage1/actions/runs/37476807793),
소스 커밋 `c374e5ba53fa72e5a84b0af2c0cf683dd2267f60`: **전체 성공**.

- 공식 PostgreSQL 컨테이너 초기화 및 health 확인
- 3 DB, NOLOGIN 권한 그룹, 교차 DB CONNECT 차단
- CPU 1코어 상당 quota, 메모리 1GiB, 연결20, shared_buffers128MB, 공개 포트 없음
- 재시작 후 3 DB의 migration 행 유지
- DB별 custom dump 생성·checksum·새 임시 DB 복원 및 migration 버전 비교

시험 환경은 GitHub Ubuntu runner다. NAS DSM/Docker 버전 호환성, NAS 영속 볼륨 권한,
실제 API 계정/TLS, 업무 데이터 정합성, 외부 독립 저장소 복원은 미검증이다.

## 추가 배포 방식 검증

[GitHub Actions 37480329786](https://github.com/Lumira077/Lumira-Stage1/actions/runs/37480329786),
커밋 `8f01bd735498360bd1dd9a7488c5df6c7b06a3c0`: Compose 방식과 DSM용 CLI 방식 **모두 성공**.
CLI 시험에서도 내부 네트워크·로컬 비밀 생성·실제 digest 사용·DB 초기화·권한·자원·3 DB 복원이 통과했다.
이 결과는 별도 Ubuntu 시험 서버의 결과이며, NAS 실제 실행 성공으로 간주하지 않는다.
