---
name: gdrive-download-lv2
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

### 다운로드 (Drive → 프로젝트 폴더)

- AI가 "어느 프로젝트에 저장할까요?"라고 질문합니다.
- 저장 경로: `10-working/{프로젝트}/gdrive/`

---

## ⚙️ **환경 설정 (필수)**

워크스페이스 루트 `.env`:

```env
# [Google Drive Auth]
GDRIVE_CREDENTIALS_PATH=D:\1my_1stAI_Agent\credentials.json
GDRIVE_TOKEN_PATH=D:\1my_1stAI_Agent\token.json

# [Upload Configuration]
GDRIVE_UPLOAD_DEFAULT_FOLDER_ID=

# [Download Configuration]
GDRIVE_DOWNLOAD_DEFAULT_FOLDER_ID=
# 다운로드 기본 폴더 (AI가 프로젝트별 하위 폴더 질문)
GDRIVE_DOWNLOAD_DIR=10-working
```

---

## 🚀 **업로드 사용법**

### 1. 기본 실행 (Outbox 업로드)

```powershell
python .claude/skills/gdrive-download-lv2/scripts/gdrive_upload.py
```

### 2. 미리보기 (Dry Run)

```powershell
python .claude/skills/gdrive-download-lv2/scripts/gdrive_upload.py --dry-run
```

### 3. 업로드 개수 제한

```powershell
python .claude/skills/gdrive-download-lv2/scripts/gdrive_upload.py --limit 5
```

### 4. 특정 파일만 업로드

```powershell
python .claude/skills/gdrive-download-lv2/scripts/gdrive_upload.py --files "report.pdf" "data.xlsx"
```

### 5. 대상 폴더 지정

```powershell
python .claude/skills/gdrive-download-lv2/scripts/gdrive_upload.py --target-upload "URL_OR_ID"
```

### 6. 상세 출력

```powershell
python .claude/skills/gdrive-download-lv2/scripts/gdrive_upload.py --verbose
```

---

## 🚀 **다운로드 사용법**

### 1. 기본 실행 (Inbox 다운로드)

```powershell
python .claude/skills/gdrive-download-lv2/scripts/gdrive_download.py
```

### 2. 미리보기 (Dry Run)

```powershell
python .claude/skills/gdrive-download-lv2/scripts/gdrive_download.py --dry-run
```

### 3. 다운로드 개수 제한

```powershell
python .claude/skills/gdrive-download-lv2/scripts/gdrive_download.py --limit 10
```

### 4. 대상 폴더 지정

```powershell
python .claude/skills/gdrive-download-lv2/scripts/gdrive_download.py --target-download "URL_OR_ID"
```

### 5. 파일/폴더 검색

```powershell
python .claude/skills/gdrive-download-lv2/scripts/gdrive_search.py "검색어"
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
python -m pip install -r .claude/skills/gdrive-download-lv2/requirements.txt
```

### 인증 (최초 1회)

```powershell
python .claude/skills/gdrive-download-lv2/scripts/gdrive_auth.py
```

---

## 🔒 **보안**

- `credentials.json`과 `token.json`은 절대 공유하지 마십시오.
- `.gitignore`에 포함되어 있는지 확인하십시오.

---

## 🗂️ 저장 위치 결정 프로세스 (AI 필수 규칙)

> **Google Drive 다운로드는 팀 작업물이므로, 반드시 프로젝트 폴더에 저장합니다.**

### 다운로드 전 필수 질문

```
Q: 이 Google Drive 자료를 어느 프로젝트에 저장할까요?

[10-working/ 하위 폴더 목록 표시]
예:
  1. 10-working/GPTers-20기/
  2. 10-working/사이드-프로젝트/
  3. 새 프로젝트 폴더 생성

선택:
```

### 저장 경로 결정

| 선택 | 저장 경로 |
|------|----------|
| 기존 프로젝트 | `10-working/{프로젝트명}/gdrive/` |
| 새 프로젝트 | `10-working/{새프로젝트명}/gdrive/` (폴더 생성) |

### AI 행동 규칙

1. **다운로드 전**: `10-working/` 하위 폴더 목록 확인
2. **사용자에게 질문**: "어느 프로젝트에 저장할까요?"
3. **폴더 없으면**: 새 프로젝트 폴더 생성 제안
4. **저장 경로**: `10-working/{프로젝트}/gdrive/`

> ⚠️ `.env`의 `GDRIVE_DOWNLOAD_DIR`은 기본값일 뿐, 실제로는 프로젝트 폴더에 저장합니다.
