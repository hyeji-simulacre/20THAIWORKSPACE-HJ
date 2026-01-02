---
name: share_notion_lv2_eduv
description: "(핵심) 노션 단방향 다운로드. 지정한 Notion 페이지의 하위 페이지들을 로컬 폴더로 다운로드합니다."
allowed-tools: Bash, Read, Write
---

# share_notion_lv2_eduv (Notion 다운로드)

이 스킬은 **Notion API**를 사용하여 Notion 페이지의 내용을 로컬 Markdown 파일로 **다운로드**하는 과정을 자동화합니다.
안정성을 위해 재귀 호출 없이, 1-depth(직계 하위) 페이지들만 명확하게 저장합니다.

## 특징
- **단일 폴더 저장**: 폴더 구조 생성 없이 지정된 폴더에 모든 파일을 저장.
- **메타데이터 보존**: 다운로드된 파일 상단에 원본 Page ID, URL, 다운로드 시간 기록.
- **안전한 설정**: `.env` 파일을 사용하여 API 키 관리.

## 🛠️ 사전 준비 (필수)

### 1단계: Notion API 토큰 발급
*(이미 업로드 실습에서 했다면 건너뛰세요)*
1. [Notion My Integrations](https://www.notion.so/my-integrations) 접속.
2. **[+ New integration]** 클릭 -> 이름 입력 -> Submit.
3. **Internal Integration Secret** (토큰) 복사.

### 2단계: Notion 페이지 준비 및 권한 부여
1. Notion에서 다운로드 대상인 **부모 페이지**를 찾습니다 (또는 생성).
2. 페이지 우측 상단 **[...]** 더보기 메뉴 클릭.
3. **[Connect to]** (또는 연결) 메뉴에서 Integration 추가.
4. **Page ID 추출**: URL 맨 뒤 32자리 숫자 복사.

### 3단계: 로컬 환경 설정 (.env)
1. 워크스페이스 루트에 `.env` 파일 생성 (또는 기존 파일 수정).
2. 위에서 구한 정보를 입력:
   ```env
   # (업로드와 같은 토큰을 써도 됩니다)
   NOTION_TOKEN=secret_XXXX...
   
   # 다운로드할 부모 페이지 ID
   NOTION_DOWNLOAD_DEFAULT_PAGE_ID=123456789abc...
   
   NOTION_DOWNLOAD_DIR=01_inbox/06_notion
   ```
   *(참고: 교육(학생) 환경에서는 워크스페이스 루트의 `.env`만 사용합니다.)*

### 4단계: 패키지 설치
```powershell
python -m pip install -r .claude/skills/_education_skills/share_notion_lv2_eduv/requirements.txt
```

## 사용법

**실행**:
```powershell
# 1. 미리보기 (Dry Run)
python .claude/skills/_education_skills/share_notion_lv2_eduv/scripts/notion_download_tree.py --dry-run

# 2. 실제 다운로드
python .claude/skills/_education_skills/share_notion_lv2_eduv/scripts/notion_download_tree.py

# 3. (선택) 하위 페이지 중 특정 제목(부분 일치)만 다운로드
python .claude/skills/_education_skills/share_notion_lv2_eduv/scripts/notion_download_tree.py --select-child-name "회의록"

```

## 결과 확인
- `01_inbox/06_notion` 폴더에 `제목__ID_날짜.md` 형식으로 파일이 생성됩니다.
