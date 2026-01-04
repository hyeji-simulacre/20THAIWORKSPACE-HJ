---
name: notion-up-lv1
description: "노션 단방향 업로드. 파일명 변경으로 진행 상태를 관리하고, 프론트매터(Frontmatter)를 통해 업로드 정보를 기록합니다."
allowed-tools: Bash, Read, Write
---

# notion-up-lv1 (Notion 업로드)

이 스킬은 **Notion API**를 사용하여 로컬 Markdown 파일을 Notion 페이지로 **업로드**하는 기능을 제공합니다.
복잡한 폴더 이동 대신, **파일명 변경**(`(done)_...`)을 통해 직관적으로 상태를 관리합니다.

## 스킬 호출 시 필수 질문

> **이 스킬이 호출되면, 반드시 사용자에게 다음을 질문하세요:**

1. **"어느 폴더의 파일을 업로드할까요?"**
   - 예시 답변: `20-created/21-ideas/`, `10-working/11-프로젝트명/`
   - 사용자가 지정한 폴더를 업로드 대상으로 사용

2. **"특정 파일만 업로드할까요, 폴더 전체를 업로드할까요?"**
   - 특정 파일: `--files "파일명.md"` 옵션 사용
   - 폴더 전체: 옵션 없이 실행

## 특징

1. **유연한 폴더 선택**: 사용자가 지정한 폴더에서 업로드
2. **시각적 상태 관리**: 파일명 접두사로 성공/실패 확인.
   - 대기/진행: `파일명.md`
   - 성공: `(done)_파일명.md` (내용 상단에 링크 정보 추가됨)
   - 실패: `(fail)_파일명.md`
3. **안전한 설정**: `.env` 파일을 사용하여 API 키 관리.

## 🛠️ 사전 준비 (필수)

### 1단계: Notion API 토큰 발급
1. [Notion My Integrations](https://www.notion.so/my-integrations) 접속.
2. **[+ New integration]** 클릭.
3. 이름 입력 (예: `My Workspace Upload`).
4. **Submit** 후 **Internal Integration Secret** (토큰) 복사.
   - 예: `secret_XXXX...`

### 2단계: Notion 페이지 준비 및 권한 부여 (중요!)
1. Notion에서 업로드할 **새 페이지**를 만듭니다 (또는 기존 페이지 사용).
2. 페이지 우측 상단 **[...]** 더보기 메뉴 클릭.
3. **[Connect to]** (또는 연결) 메뉴 찾기.
4. 위에서 만든 Integration(`My Workspace Upload`)을 검색하여 선택/추가.
   - *이 단계를 건너뛰면 API가 페이지를 찾지 못합니다.*
5. **Page ID 추출**:
   - 페이지 링크 복사 (`https://notion.so/My-Page-123456789abc...`)
   - 맨 뒤의 32자리 숫자(`123456789abc...`)가 **Page ID**입니다.

### 3단계: 로컬 환경 설정 (.env)
1. 워크스페이스 루트에 `.env` 파일 생성 (또는 기존 파일 수정).
2. 위에서 구한 정보를 입력:
   ```env
   NOTION_TOKEN=secret_XXXX...
   NOTION_UPLOAD_DEFAULT_PAGE_ID=123456789abc...
   ```
   *(참고: 업로드 폴더는 스킬 실행 시 질문을 통해 결정됩니다.)*

### 4단계: 패키지 설치
```powershell
python -m pip install -r .claude/skills/notion-up-lv1/requirements.txt
```

## 사용법

**실행 예시**:
```powershell
# 1. 미리보기 (Dry Run) - 사용자가 지정한 폴더
python .claude/skills/notion-up-lv1/scripts/notion_upload.py --dir "20-created/21-ideas" --dry-run

# 2. 실제 업로드
python .claude/skills/notion-up-lv1/scripts/notion_upload.py --dir "20-created/21-ideas"

# 3. (선택) 특정 파일만 업로드
python .claude/skills/notion-up-lv1/scripts/notion_upload.py --dir "20-created/21-ideas" --files "my_test.md"
```

## 결과 확인
- 업로드 성공 시: 지정 폴더 내의 파일명이 `(done)_파일명.md`로 변경됩니다.
- 파일 내용을 열어보면 상단에 `notion_url` 등이 포함된 정보가 추가되어 있습니다.
