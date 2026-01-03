# 05. 구글 드라이브 연동 (Rclone) - 전문가를 위한 만능 도구

> **"명령어 한 줄로 수TB 데이터를 옮긴다구요? 네, Rclone이라면 가능합니다."**

## 1. 🎯 개념 및 필요성 (Concept)

### 🧐 이게 뭐죠?
**"클라우드 스토리지의 스위스 아미 나이프"**라고 불리는 도구입니다. 구글 드라이브뿐만 아니라 AWS S3, Dropbox 등 40개 이상의 클라우드를 명령어로 제어합니다. 설치형 프로그램보다 훨씬 가볍고 빠릅니다.

### 💡 왜 써야 하죠?
- **압도적인 속도**: 일반 업로드보다 3~4배 빠릅니다. (병렬 전송 기술)
- **서버/NAS 환경**: 그래픽 화면(GUI)이 없는 서버나 NAS에서도 돌아갑니다.
- **정교한 동기화**: "변경된 파일만", "특정 확장자 제외하고", "100MB 이상만" 등 내 맘대로 규칙을 정할 수 있습니다.

---

## 2. 🚦 특징 비교 (vs 데스크톱 앱)

| 특징 | Rclone (CLI 전문가용) | 데스크톱 앱 (일반 사용자용) |
|---|---|---|
| **핵심 가치** | **속도 & 자동화** | 편의성 & 직관성 |
| **인터페이스** | 검은색 터미널 화면 (CLI) | 친숙한 윈도우 탐색기 (GUI) |
| **속도** | ⭐⭐⭐⭐⭐ (매우 빠름) | ⭐⭐⭐ (보통) |
| **안정성** | 대용량/수만 개 파일도 거뜬함 | 파일 많으면 느려지거나 멈춤 |

> **"대용량 데이터를 백업하거나, 매일 밤 자동으로 파일을 옮기고 싶다면 Rclone이 정답입니다."**

---

## 3. 🚀 설치 및 설정 (Setup)

### 1️⃣ 다운로드 및 설치
1. [Rclone 다운로드 페이지](https://rclone.org/downloads/) 접속
2. Windows용 `zip` 파일 다운로드 및 압축 해제
3. (선택) `rclone.exe`가 있는 폴더를 환경 변수 `PATH`에 등록하면 어디서든 실행 가능합니다.

### 2️⃣ 연결 설정 (Config)
처음에 한 번만 해주면 됩니다. (조금 복잡해 보이지만 따라하면 쉬워요!)

```powershell
rclone config
```

1. `n` (New remote) 입력
2. 이름 입력: `gdrive` (짧을수록 편합니다)
3. 스토리지 선택: `drive` (Google Drive 번호 찾아서 입력)
4. `Client ID`, `Secret`: 엔터 (기본값 사용)
5. `Scope`: `1` (Full access)
6. 나머지는 대부분 엔터(Enter) 누르다가...
7. 브라우저 열리면 **로그인 & 권한 혀용** 클릭!
8. `q` 눌러서 종료

### 3️⃣ 연결 테스트
```powershell
rclone ls gdrive:
```
내 구글 드라이브의 파일 목록이 주르륵 뜬다면 성공입니다! 🎉

---

## 4. 💻 핵심 명령어 (Basic Commands)

가장 많이 쓰는 3가지만 기억하세요.

### 1. 복사하기 (`copy`)
원본을 유지하면서 복사합니다. (가장 안전)
```powershell
# 내 컴퓨터의 photos 폴더를 구글 드라이브의 Backup 폴더로 복사
rclone copy ./photos gdrive:Backup
```

### 2. 동기화하기 (`sync`)
**⚠️ 주의**: 원본과 똑같이 만듭니다. 원본에 없으면 **지워버립니다!**
```powershell
# 내 폴더 내용을 구글 드라이브와 완벽하게 일치시킴 (지워질 수 있음 주의)
rclone sync ./local_folder gdrive:remote_folder
```

### 3. 마운트하기 (`mount`)
데스크톱 앱처럼 Z: 드라이브로 연결해서 씁니다.
```powershell
rclone mount gdrive: Z: --vfs-cache-mode writes
```

---

## 5. 🍯 활용 꿀팁 (Transformation)

### 🏎️ 속도 더 빠르게 하기
파일이 너무 많아서 느린가요? 옵션을 추가하세요.
- `--transfers 8`: 한 번에 8개씩 옮겨라 (기본 4개)
- `--progress`: 진행 상황을 보여줘라

```powershell
rclone copy ./big_data gdrive:Backup --transfers 16 --progress
```

### 🧹 필터링 (필요한 것만 쏙쏙)
```powershell
# jpg 파일만 복사하고 싶을 때
rclone copy ./images gdrive:Images --include "*.jpg"

# 임시 파일, 로그 파일 빼고 복사할 때
rclone copy ./project gdrive:Backup --exclude "*.{log,tmp}"
```

---

## 6. ⚠️ 주의사항

1. **`sync` 명령어 조심**: 실수로 원본 폴더 경로를 잘못 적으면 구글 드라이브 파일이 다 날아갈 수도 있습니다. 처음엔 `copy`를 애용하세요.
2. **`--dry-run`**: 불안하면 명령어 끝에 이걸 붙이세요. 실제로 실행하진 않고 "가상으로" 보여주기만 합니다.
