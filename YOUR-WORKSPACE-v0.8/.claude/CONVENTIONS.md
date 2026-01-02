# AI Workspace 규칙 및 컨벤션

이 문서는 새로운 명령어, 스킬, 에이전트, 폴더, 템플릿을 생성할 때 반드시 따라야 하는 규칙입니다.

---

## 1. Johnny Decimal 번호 체계

### 메인 폴더 구조

| 번호대 | 폴더 | 용도 |
|--------|------|------|
| 00 | `00-templates/` | 반복 사용 서식 |
| 10 | `10-working/` | 진행 중인 프로젝트 |
| 20 | `20-created/` | 내가 만든 것 |
| 30 | `30-collected/` | 외부에서 가져온 것 |
| 40 | `40-archive/` | 완료/보관 |
| 50 | `50-periodic/` | 정기 기록 |

### 하위 폴더 번호

하위 폴더는 상위 폴더의 십의 자리를 따릅니다:

```
20-created/
├── 21-ideas/      ← 20번대의 첫 번째 하위
├── 22-notes/      ← 20번대의 두 번째 하위 (필요시)
└── 23-xxx/        ← 확장 시

30-collected/
├── 31-web-clips/
├── 32-readings/
└── 33-news/

50-periodic/
├── 51-daily/
└── 52-weekly/
```

---

## 2. 명령어-폴더-템플릿 1:1 매칭

### 규칙

새 명령어를 만들 때 반드시 확인:

| 항목 | 네이밍 규칙 | 예시 |
|------|-------------|------|
| 명령어 파일 | `XX-명령어.md` | `21-idea-note.md` |
| 저장 폴더 | `X0-분류/XX-하위/` | `20-created/21-ideas/` |
| 템플릿 파일 | `XX-명령어-template.md` | `21-idea-template.md` |

### 현재 매핑

| 번호 | 명령어 | 저장 폴더 | 템플릿 |
|------|--------|-----------|--------|
| 10 | `/10-project-roadmap` | `10-working/` | `10-project-template.md` |
| 21 | `/21-idea-note` | `20-created/21-ideas/` | `21-idea-template.md` |
| 31 | `/31-web-clip` | `30-collected/31-web-clips/` | `31-web-clip-template.md` |
| 32 | `/32-reading-note` | `30-collected/32-readings/` | `32-reading-template.md` |
| 33 | `/33-news-briefing` | `30-collected/33-news/` | `33-news-template.md` |
| 51 | `/51-daily-note` | `50-periodic/51-daily/` | `51-daily-template.md` |
| 52 | `/52-weekly-note` | `50-periodic/52-weekly/` | `52-weekly-template.md` |

### 새 명령어 추가 시 체크리스트

- [ ] 번호가 저장 폴더와 일치하는가?
- [ ] `.claude/commands/`에 명령어 파일 생성
- [ ] `00-templates/`에 템플릿 파일 생성
- [ ] 저장될 하위 폴더가 존재하는가? (없으면 생성)
- [ ] CLAUDE.md의 명령어 목록 업데이트

---

## 3. 스킬 (Skills) 네이밍 규칙

### 폴더 위치

`.claude/skills/스킬명/`

### 네이밍 규칙

| 규칙 | 예시 |
|------|------|
| 소문자 + 하이픈 | `pdf-reader`, `web-scraper` |
| 기능 명시 | `youtube-subtitle`, `pkm-search` |
| 레벨 표시 (필요시) | `notion-upload-lv1`, `gdrive-download-lv2` |

### 현재 스킬 목록

| 스킬명 | 용도 |
|--------|------|
| `pkm-search` | 시맨틱 검색 |
| `youtube-subtitle` | YouTube 자막 추출 |
| `pdf-reader` | PDF 텍스트 추출 |
| `web-scraper` | 웹 스크래핑 |
| `notion-upload-lv1` | Notion 업로드 (초급) |
| `notion-download-lv2` | Notion 다운로드 (중급) |
| `gdrive-upload-lv1` | Google Drive 업로드 (초급) |
| `gdrive-download-lv2` | Google Drive 다운로드 (중급) |

### 새 스킬 추가 시 체크리스트

- [ ] 스킬 폴더 생성: `.claude/skills/스킬명/`
- [ ] `SKILL.md` 파일 생성 (트리거 문구 포함)
- [ ] 필요시 `requirements.txt` 추가
- [ ] README 또는 설정 가이드 포함

---

## 4. 에이전트 (Agents) 네이밍 규칙

### 폴더 위치

`.claude/agents/에이전트명.md`

### 네이밍 규칙

| 규칙 | 예시 |
|------|------|
| 소문자 + 하이픈 | `zettelkasten-linker` |
| 역할 명시 | `code-reviewer`, `note-connector` |

### 현재 에이전트 목록

| 에이전트 | 트리거 | 용도 |
|----------|--------|------|
| `zettelkasten-linker` | "볼트 분석해줘", "노트 연결 찾아줘" | 노트 간 연결 분석 |

### 새 에이전트 추가 시 체크리스트

- [ ] `.claude/agents/`에 파일 생성
- [ ] `name`, `description` 메타데이터 포함
- [ ] 트리거 문구 명시
- [ ] 분석 범위 정의 (포함/제외 폴더)

---

## 5. 학습자료 번호 체계

`_GPTers 20기 학습자료실/` 폴더 전용 규칙:

### 폴더 구조

| 번호 | 폴더 | 용도 |
|------|------|------|
| 00 | `00-시작하기/` | 공통/환경설정 |
| 10 | `10-1주차-xxx/` | 1주차 학습 |
| 20 | `20-2주차-xxx/` | 2주차 학습 |
| 30 | `30-3주차-xxx/` | 3주차 학습 |
| 40 | `40-4주차-xxx/` | 4주차 학습 |
| 90 | `90-부록/` | 참고자료 |

### 파일 번호

파일은 폴더 번호의 십의 자리를 따릅니다:

```
10-1주차-Structure/
├── 11_첫번째문서.md
├── 12_두번째문서.md
└── 13_세번째문서.md

20-2주차-Collect/
├── 21_첫번째문서.md
├── 22_두번째문서.md
└── ...
```

---

## 6. 일반 파일 이름 규칙

| 유형 | 형식 | 예시 |
|------|------|------|
| Daily Note | `YYYY-MM-DD.md` | `2026-01-14.md` |
| Weekly Note | `YYYY-WXX.md` | `2026-W03.md` |
| 아이디어 | `YYYY-MM-DD 제목.md` | `2026-01-14 AI 서비스.md` |
| 웹클립 | `YYYYMMDD-제목.md` | `20260114-마케팅.md` |

---

## 7. 금지 사항

- ❌ 번호 없이 폴더/파일 생성
- ❌ 명령어와 다른 번호의 템플릿 생성
- ❌ 대문자 폴더명 (스킬, 에이전트)
- ❌ 공백 포함 폴더명 (하이픈 사용)
- ❌ 기존 번호 체계와 충돌하는 번호 사용

---

## 8. 확장 시 번호 할당

### 새 메인 폴더
- 60, 70, 80번대 사용 가능
- 90번대는 시스템/부록 예약

### 새 하위 폴더
- 해당 십의 자리 내에서 순차 할당
- 예: `30-collected/`에 추가 → `34-xxx/`, `35-xxx/`

### 새 명령어
- 저장될 하위 폴더 번호와 동일하게 생성
- 예: `34-podcasts/` → `/34-podcast-note`

---

*이 규칙을 따르면 전체 시스템의 일관성이 유지됩니다.*
