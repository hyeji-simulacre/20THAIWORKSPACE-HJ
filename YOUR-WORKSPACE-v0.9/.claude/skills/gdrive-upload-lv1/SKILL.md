---
name: gdrive-upload-lv1
description: "구글드라이브 연동(업로드 전용): Outbox 워크플로우를 통해 로컬 파일을 구글 드라이브 지정 폴더로 업로드합니다."
allowed-tools: Bash, Read, Write
---

# Google Drive 업로드 스킬 (Lv1)

로컬 워크스페이스의 **Outbox** 폴더에 파일을 넣으면, 자동으로 Google Drive의 지정된 폴더로 **업로드**하고 상태별 폴더로 이동시키는 스킬입니다.

> **운영 원칙**:
> - **로컬 = 원본 (Source)**
> - **구글 드라이브 = 아카이브/공유 (Destination)**
> - 모든 파일 형식 지원 (PDF, PPT, Image, etc.)

---

## 📋 **워크플로우**

**Outbox 구조 (`02_outbox`):**

1. **01_ready**: 사용자가 파일을 이곳에 복사/이동 (Trigger)
2. **02_inprogress**: 스크립트가 실행되면 작업 중인 파일이 잠시 머무름
3. **03_complete**: 업로드 성공 시 이곳으로 이동
4. **04_failed**: 업로드 실패 시 이곳으로 이동 (로그 확인 필요)

---

## ⚙️ **환경 설정 (필수)**

워크스페이스 루트의 `.env` 파일에 다음 설정을 추가해야 합니다.
(구글 드라이브 API 인증 `credentials.json`, `token.json` 발급 선행 필요)

```env
# [Google Drive Auth]
GDRIVE_CREDENTIALS_PATH=D:\1my_1stAI_Agent\credentials.json
GDRIVE_TOKEN_PATH=D:\1my_1stAI_Agent\token.json

# [Upload Configuration] - Outbox to Drive
# 업로드할 구글 드라이브 기본 폴더 ID (웹 주소 창에서 확인: folders/뒤의 문자열)
GDRIVE_UPLOAD_DEFAULT_FOLDER_ID=

# 로컬 Outbox 경로 설정
GDRIVE_UPLOAD_READY_DIR=02_outbox\01_ready
GDRIVE_UPLOAD_INPROGRESS_DIR=02_outbox\02_inprogress
GDRIVE_UPLOAD_COMPLETE_DIR=02_outbox\03_complete
GDRIVE_UPLOAD_FAILED_DIR=02_outbox\04_failed
```

---

## 🚀 **사용 방법**

### **1. 기본 실행 (Outbox 처리)**

`01_ready` 폴더에 있는 모든 파일을 순차적으로 업로드합니다.

```powershell
python .claude/skills/gdrive-upload-lv1/scripts/gdrive_upload.py
```

### **2. 특정 타겟(폴더/파일) 지정 업로드**

폴더뿐만 아니라 특정 파일 ID나 URL을 지정하여 업로드할 수 있습니다.

```powershell
# 폴더 ID/URL로 지정
python .claude/skills/gdrive-upload-lv1/scripts/gdrive_upload.py --targetfolder "URL_OR_ID"
```

### **3. 시뮬레이션 (Dry Run)**

파일 이동이나 업로드를 실제로 하지 않고, 어떤 파일이 대상인지 확인합니다.

```powershell
python .claude/skills/gdrive-upload-lv1/scripts/gdrive_upload.py --dry-run
```

### **4. 수동 단일 파일 업로드**

Outbox 경로가 아닌 특정 파일을 직접 올리고 싶을 때 사용합니다. (이동 처리 없음)

```powershell
python .claude/skills/gdrive-upload-lv1/scripts/gdrive_upload.py --file "D:\MyFile.pdf"
```

---

## 📦 **설치 및 인증**

### **패키지 설치**

```powershell
python -m pip install -r .claude/skills/gdrive-upload-lv1/requirements.txt
```

### **인증 (최초 1회)**

```powershell
# credentials.json이 루트에 있어야 함
python .claude/skills/gdrive-upload-lv1/scripts/gdrive_auth.py
```

---

## 🔒 **보안**

- `credentials.json`과 `token.json`은 절대 공유하지 마십시오.
- `.gitignore`에 포함되어 있는지 확인하십시오.
