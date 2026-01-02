---
name: share_gdrive_lv2_eduv
description: "구글드라이브 연동(업로드+다운로드): Outbox/Inbox 워크플로우를 통해 구글 드라이브와 로컬 파일을 양방향으로 관리합니다."
allowed-tools: Bash, Read, Write
---

# Google Drive 스킬 (Lv2 - 업로드 + 다운로드)

**Lv1 기능을 포함**하며, 다운로드 및 검색 기능을 추가로 제공합니다.

- **업로드**: 로컬 Outbox → Google Drive (자동 이동 워크플로우)
- **다운로드**: Google Drive → 로컬 Inbox

> **운영 원칙**:
>
> - **로컬 = 원본/작업 공간**
> - **구글 드라이브 = 아카이브/공유/소스**
> - 모든 파일 형식 지원

---

## 📋 **워크플로우**

### 업로드 (Outbox → Drive)

1. **01_ready**: 파일을 이곳에 복사/이동 (Trigger)
2. **02_inprogress**: 업로드 중
3. **03_complete**: 업로드 성공
4. **04_failed**: 업로드 실패

### 다운로드 (Drive → Inbox)

- `01_inbox/05_gdrive`: 다운로드 경로

---

## ⚙️ **환경 설정 (필수)**

워크스페이스 루트 `.env`:

```env
# [Google Drive Auth]
GDRIVE_CREDENTIALS_PATH=D:\1my_1stAI_Agent\credentials.json
GDRIVE_TOKEN_PATH=D:\1my_1stAI_Agent\token.json

# [Upload Configuration] - Outbox to Drive
GDRIVE_UPLOAD_DEFAULT_FOLDER_ID=
GDRIVE_UPLOAD_READY_DIR=02_outbox\01_ready
GDRIVE_UPLOAD_INPROGRESS_DIR=02_outbox\02_inprogress
GDRIVE_UPLOAD_COMPLETE_DIR=02_outbox\03_complete
GDRIVE_UPLOAD_FAILED_DIR=02_outbox\04_failed

# [Download Configuration] - Drive to Inbox
GDRIVE_DOWNLOAD_DEFAULT_FOLDER_ID=
GDRIVE_DOWNLOAD_DIR=01_inbox\05_gdrive\01_ready
```

---

## 🚀 **업로드 사용법**

### 1. 기본 실행 (Outbox 업로드)

```powershell
python .claude/skills/_education_skills/share_gdrive_lv2_eduv/scripts/gdrive_upload.py
```

### 2. 미리보기 (Dry Run)

```powershell
python .claude/skills/_education_skills/share_gdrive_lv2_eduv/scripts/gdrive_upload.py --dry-run
```

### 3. 업로드 개수 제한

```powershell
python .claude/skills/_education_skills/share_gdrive_lv2_eduv/scripts/gdrive_upload.py --limit 5
```

### 4. 특정 파일만 업로드

```powershell
python .claude/skills/_education_skills/share_gdrive_lv2_eduv/scripts/gdrive_upload.py --files "report.pdf" "data.xlsx"
```

### 5. 대상 폴더 지정

```powershell
python .claude/skills/_education_skills/share_gdrive_lv2_eduv/scripts/gdrive_upload.py --target-upload "URL_OR_ID"
```

### 6. 상세 출력

```powershell
python .claude/skills/_education_skills/share_gdrive_lv2_eduv/scripts/gdrive_upload.py --verbose
```

---

## 🚀 **다운로드 사용법**

### 1. 기본 실행 (Inbox 다운로드)

```powershell
python .claude/skills/_education_skills/share_gdrive_lv2_eduv/scripts/gdrive_download.py
```

### 2. 미리보기 (Dry Run)

```powershell
python .claude/skills/_education_skills/share_gdrive_lv2_eduv/scripts/gdrive_download.py --dry-run
```

### 3. 다운로드 개수 제한

```powershell
python .claude/skills/_education_skills/share_gdrive_lv2_eduv/scripts/gdrive_download.py --limit 10
```

### 4. 대상 폴더 지정

```powershell
python .claude/skills/_education_skills/share_gdrive_lv2_eduv/scripts/gdrive_download.py --target-download "URL_OR_ID"
```

### 5. 파일/폴더 검색

```powershell
python .claude/skills/_education_skills/share_gdrive_lv2_eduv/scripts/gdrive_search.py "검색어"
```

---

## 📊 **매개변수 요약**

| 매개변수 | 업로드 | 다운로드 | 설명 |
|---|:---:|:---:|---|
| `--dry-run` | ✅ | ✅ | 시뮬레이션 (실제 실행 없음) |
| `--limit N` | ✅ | ✅ | 최대 N개 파일만 처리 |
| `--verbose` | ✅ | ✅ | 상세 출력 |
| `--target-upload` | ✅ | - | 업로드 대상 폴더 |
| `--target-download` | - | ✅ | 다운로드 소스 폴더 |
| `--files` | ✅ | - | 특정 파일만 선택 |

> **하위 호환**: `--targetfolder`도 계속 사용 가능

---

## 📦 **설치 및 인증**

### 패키지 설치

```powershell
python -m pip install -r .claude/skills/_education_skills/share_gdrive_lv2_eduv/requirements.txt
```

### 인증 (최초 1회)

```powershell
python .claude/skills/_education_skills/share_gdrive_lv2_eduv/scripts/gdrive_auth.py
```

---

## 🔒 **보안**

- `credentials.json`과 `token.json`은 절대 공유하지 마십시오.
- `.gitignore`에 포함되어 있는지 확인하십시오.
