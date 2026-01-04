---
name: gdrive-up-lv1
description: "구글드라이브 연동(업로드 전용): 프로젝트 폴더에서 구글 드라이브로 파일을 업로드합니다."
allowed-tools: Bash, Read, Write
---

# Google Drive 업로드 스킬 (Lv1)

프로젝트 폴더의 파일을 Google Drive로 **업로드**하는 스킬입니다.

> **운영 원칙**:
> - **로컬 = 원본 (Source)**
> - **구글 드라이브 = 아카이브/공유 (Destination)**
> - 모든 파일 형식 지원 (PDF, PPT, Image, etc.)

---

## 📋 **워크플로우**

### 업로드 (프로젝트 → Drive)

1. AI가 "어떤 파일을 업로드할까요?" 질문
2. AI가 "어느 프로젝트에서요?" 질문
3. 경로: `10-working/{프로젝트}/gdrive/`
4. 업로드 완료 시 파일명 변경: `(done)_파일명.확장자`
5. 업로드 실패 시 파일명 변경: `(fail)_파일명.확장자`

---

## ⚙️ **환경 설정 (필수)**

워크스페이스 루트의 `.env` 파일에 다음 설정을 추가해야 합니다.
(구글 드라이브 API 인증 `credentials.json`, `token.json` 발급 선행 필요)

```env
# [Google Drive Auth]
GDRIVE_CREDENTIALS_PATH=D:\1my_1stAI_Agent\credentials.json
GDRIVE_TOKEN_PATH=D:\1my_1stAI_Agent\token.json

# [Upload Configuration]
# 업로드할 구글 드라이브 기본 폴더 ID (웹 주소 창에서 확인: folders/뒤의 문자열)
GDRIVE_UPLOAD_DEFAULT_FOLDER_ID=

# 업로드 기본 폴더 (AI가 프로젝트별 하위 폴더 질문)
GDRIVE_UPLOAD_DIR=10-working
```

---

## 🚀 **사용 방법**

### **1. 기본 실행**

```powershell
python .claude/skills/gdrive-up-lv1/scripts/gdrive_upload.py
```

### **2. 특정 파일 업로드**

```powershell
python .claude/skills/gdrive-up-lv1/scripts/gdrive_upload.py --file "파일경로.pdf"
```

### **3. 특정 폴더 지정 업로드**

```powershell
python .claude/skills/gdrive-up-lv1/scripts/gdrive_upload.py --targetfolder "URL_OR_ID"
```

### **4. 시뮬레이션 (Dry Run)**

```powershell
python .claude/skills/gdrive-up-lv1/scripts/gdrive_upload.py --dry-run
```

---

## 📦 **설치 및 인증**

### **패키지 설치**

```powershell
python -m pip install -r .claude/skills/gdrive-up-lv1/requirements.txt
```

### **인증 (최초 1회)**

```powershell
python .claude/skills/gdrive-up-lv1/scripts/gdrive_auth.py
```

---

## 🔒 **보안**

- `credentials.json`과 `token.json`은 절대 공유하지 마십시오.
- `.gitignore`에 포함되어 있는지 확인하십시오.

---

## 🗂️ 저장 위치 결정 프로세스 (AI 필수 규칙)

> **업로드할 파일은 프로젝트 폴더에서 가져옵니다.**

### 업로드 전 필수 질문

```
Q1: 어떤 파일을 업로드할까요?
Q2: 어느 프로젝트에서요?

[10-working/ 하위 폴더 목록 표시]
예:
  1. 10-working/GPTers-20기/
  2. 10-working/사이드-프로젝트/

선택:
```

### 저장 경로 결정

| 선택 | 업로드 소스 경로 |
|------|-----------------|
| 기존 프로젝트 | `10-working/{프로젝트명}/gdrive/` |

### AI 행동 규칙

1. **업로드 전**: "어떤 파일을 업로드할까요?" 질문
2. **프로젝트 확인**: `10-working/` 하위 폴더 목록 표시
3. **사용자에게 질문**: "어느 프로젝트에서요?"
4. **소스 경로**: `10-working/{프로젝트}/gdrive/`
5. **업로드 완료**: 파일명에 `(done)_` prefix 추가
