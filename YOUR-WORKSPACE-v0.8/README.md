# AI Workspace Template

> **GPTers 20기 AI 워크스페이스 스터디**
>
> "지식과 문서를 다루는 분에게 탁월한, 나만의 지식활용 AI 워크스페이스"

---

## 목차

- [스터디 소개](#스터디-소개)
- [시작하기](#시작하기)
- [폴더 구조](#폴더-구조)
- [폴더 구조 설명](#폴더-구조-설명)
- [Claude Code 확장 기능 이해하기](#claude-code-확장-기능-이해하기)
- [Claude Code 설정 레벨](#claude-code-설정-레벨-유저-vs-프로젝트)
- [슬래시 명령어 (Skills)](#슬래시-명령어-skills)
- [일일 워크플로우](#일일-워크플로우)
- [커스터마이징](#커스터마이징)
- [문제 해결](#문제-해결)
- [문의 및 커뮤니티](#문의-및-커뮤니티)
- [라이선스](#라이선스)

---

## 스터디 소개

이 워크스페이스는 **Claude Code**를 활용한 지식관리 시스템입니다.

> "자료 찾느라 업무할 시간을 다 놓치고 계신가요?"
>
> 쌓인 회의록, 주간보고, 할 일 정리 문서에 치여 사는 분들을 위해
> **슬래시 명령어 하나로 자동 분류되는 AI 워크스페이스**를 만들었습니다.

### 이 워크스페이스로 할 수 있는 것

- **자동 정리**: 내가 지시만 하면 자료가 알맞은 폴더에 자동 저장
- **즉시 검색**: 나만의 AI가 내 자료를 즉시 검색하고 연관 자료까지 추천
- **자동 작성**: 문서 검색과 정리는 물론, 원하는 내용까지 작성

**활용 예시:**
- 기획 회의 전: "OO관련 자료 모아 정리해줘" → 2분 내 브리핑 자료 완성
- 주간보고 작성: "이번 주 내가 한 일 정리해줘" → 야근 탈출
- 콘텐츠 기획: "최근 트렌드 적용해줘" → 트렌드 + 내 업무 기반 신규 기획안

### 공동 스터디장

| 이름 | 소개 |
|------|------|
| **안상영** | 디지털 사업 전문가 · 노에스이오 테크놀로지 대표 · 자체 AI Agent 개발 및 데이터 수집/분석 설계 |
| **정혜지** | 기록관리 전문가(아키비스트) · ContextA 대표 · 브런치 칼럼니스트 · 서울대/한국외대/명지대 기록대학원 강의 |

> **기록관리 전문가의 '지식 구조'** × **디지털 전문가의 '자동화 기술'** 결합

---

## 시작하기

### 1단계: 사전 준비 확인

- [ ] Claude Pro 구독 완료 ($20/월)
- [ ] VSCode 설치 완료
- [ ] Claude Code 설치 완료

> 설치 안내: [Claude Code 공식 가이드](https://docs.anthropic.com/ko/docs/claude-code/getting-started)

### 2단계: 템플릿 설정

1. **압축 해제**
   - 다운로드한 ZIP 파일을 원하는 위치에 압축 해제
   - 예: `~/Documents/AI-Workspace/`

2. **VSCode로 폴더 열기**
   - VSCode 실행 → File → Open Folder
   - `AI-Workspace-Template` 폴더 선택

3. **Claude Code 실행**
   - 터미널 열기: `Ctrl+`` (백틱) 또는 Terminal → New Terminal
   - 입력: `claude`

### 3단계: 첫 명령 실행

```
/51-daily-note
```

오늘 날짜의 Daily Note가 생성됩니다!

---

## 폴더 구조

```
AI-Workspace-Template/
├── .claude/
│   ├── commands/        ← 슬래시 명령어
│   └── CLAUDE.md        ← 폴더 규칙
├── 00-templates/        ← 반복 사용 서식
├── 10-working/          ← 지금 진행 중인 것
├── 20-created/          ← 내가 만든 것
│   └── 21-ideas/
├── 30-collected/        ← 외부에서 가져온 것
│   ├── 31-web-clips/
│   ├── 32-readings/
│   └── 33-news/
├── 40-archive/          ← 끝난 것
├── 50-periodic/         ← 정기 기록
│   ├── 51-daily/
│   └── 52-weekly/
└── README.md
```

---

## 핵심 원칙: 게으른 자들을 위한 출처주의

**"이거 내가 만들었나? 외부에서 가져왔나?"**

| 내가 만든 것 | 외부에서 가져온 것 |
|-------------|-------------------|
| `20-created/` | `30-collected/` |
| 아이디어, 기획서, 회의록 | 웹 아티클, 책, PDF |

---

## 폴더 구조 설명

| 폴더 | 한 줄 설명 |
|------|-----------|
| `00-templates/` | 내가 지정하고 AI가 참조하는 템플릿 |
| `10-working/` | 지금 하는 것 (진행 중인 프로젝트) |
| `20-created/` | 내가 만든 것 (내 생각, 메모, 초안) |
| `30-collected/` | 남에게서 가져온 것 (스크랩, 레퍼런스, PDF) |
| `40-archive/` | 보관 (끝난 10번) |
| `50-periodic/` | 주기적 기록 (일기, 회고) |

### 왜 00번이 Inbox가 아닌가?

일반적인 PKM에서는 `00-inbox`에 미분류 문서를 넣고, 나중에 분류합니다.
하지만 **AI 에이전트가 자동 분류**하는 이 워크스페이스에서는 "미분류" 상태가 불필요합니다.
대신 AI가 참조할 템플릿을 넣어두면 더 유용합니다.

### 왜 5개인가?

PKM 시맨틱 검색 시, 우선순위별 벡터 스토어를 5~7개로 나누면 효율적입니다.
이 구조는 그대로 검색 우선순위로 활용할 수 있어, 확장 시에도 고민 없이 적용됩니다.

> 필요에 따라 `temp/` 등 커스텀 폴더를 추가해도 됩니다.

---

## Claude Code 확장 기능 이해하기

Claude Code는 세 가지 방식으로 기능을 확장할 수 있습니다.

| 구분 | 설명 | 호출 방식 |
|------|------|----------|
| **Commands** | 저장된 프롬프트 템플릿 | `/명령어`로 명시적 호출 |
| **Skills** | Claude가 자동 감지하는 능력 | 상황에 맞게 자동 적용 |
| **Agents** | 독립 컨텍스트의 전문가 AI | 자동 또는 명시적 호출 |

### 쉽게 말하면

- **Commands** = "이 프롬프트 저장해두고 `/이름`으로 불러쓸래"
- **Skills** = "이런 상황이면 알아서 이 능력 써"
- **Agents** = "별도의 전문가를 불러서 독립적으로 일 시키기"

> 이 워크스페이스의 `/51-daily-note`, `/31-web-clip` 등은 Commands 형태로 호출하지만, Skill처럼 자동화된 워크플로우를 수행합니다.

**공식 문서:**
- [Slash Commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands)
- [Skills](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)

---

## Claude Code 설정 레벨 (유저 vs 프로젝트)

Claude Code 설정은 **유저 레벨**(홈 디렉토리)과 **프로젝트 레벨**(작업 폴더)로 나뉘며, 프로젝트 레벨이 우선 적용됩니다.

| 구분 | 유저 레벨 | 프로젝트 레벨 |
|------|-----------|---------------|
| **경로** | `~/.claude/` | `프로젝트폴더/.claude/` |
| **적용 범위** | 모든 프로젝트 | 해당 프로젝트만 |
| **비유** | 나의 정체성 | 이 작업 공간의 규칙 |
| **팀 공유** | 불가 (개인용) | 가능 (Git 커밋) |

### 어디에 뭘 넣을까?

**유저 레벨에 넣을 것** (나를 따라다니는 것)
- 내 응답 스타일 선호 ("반말로", "이모지 쓰지마")
- 범용 스킬 (Google Calendar, 웹 검색 등)
- API 키 같은 인증 정보

**프로젝트 레벨에 넣을 것** (이 프로젝트 전용)
- 폴더 구조 설명
- 프로젝트 전용 스킬 (`/51-daily-note`, `/31-web-clip` 등)
- 글쓰기 스타일 가이드

> 이 워크스페이스의 `.claude/` 폴더에는 프로젝트 전용 설정이 들어있습니다.
> 개인 선호도는 `~/.claude/`에 따로 설정하세요.

**공식 문서:**
- [Settings](https://docs.anthropic.com/en/docs/claude-code/settings)
- [Memory (CLAUDE.md)](https://docs.anthropic.com/en/docs/claude-code/memory)

---

## 슬래시 명령어 (Skills)

슬래시 명령어는 Claude Code에게 특정 작업을 자동화하도록 지시하는 단축키입니다.
터미널에 명령어를 입력하면, AI가 알아서 적절한 폴더에 파일을 생성하고 내용을 구성합니다.

### 명령어 목록

| 명령어 | 설명 | 저장 위치 |
|--------|------|-----------|
| `/10-project-roadmap [프로젝트명]` | 프로젝트 로드맵 생성 | `10-working/` |
| `/21-idea-note [제목]` | 아이디어/기획 노트 생성 | `20-created/21-ideas/` |
| `/31-web-clip [URL]` | 웹 콘텐츠 스크랩 및 정리 | `30-collected/31-web-clips/` |
| `/32-reading-note [책 제목]` | 독서/PDF/논문 노트 생성 | `30-collected/32-readings/` |
| `/33-news-briefing [주제]` | 뉴스 브리핑 정리 | `30-collected/33-news/` |
| `/51-daily-note` | 오늘의 Daily Note 생성 | `50-periodic/51-daily/` |
| `/52-weekly-note` | 이번 주 Weekly Note 생성 | `50-periodic/52-weekly/` |

### 명령어 상세 설명

#### `/10-project-roadmap` - 프로젝트 관리

새 프로젝트를 시작할 때 로드맵을 만들어 체계적으로 관리하세요.

```
/10-project-roadmap 신규 서비스 런칭
```

#### `/21-idea-note` - 아이디어 캡처

번뜩이는 아이디어를 놓치지 마세요.

```
/21-idea-note AI 기반 회의록 자동화 서비스
```

#### `/31-web-clip` - 웹 콘텐츠 스크랩

좋은 아티클, 블로그 포스트, SNS 콘텐츠를 저장하고 핵심만 정리합니다.

```
/31-web-clip https://example.com/great-article
```

#### `/32-reading-note` - 독서 & 학습 기록

책, PDF, 논문에서 얻은 인사이트를 기록합니다.

```
/32-reading-note 생각에 관한 생각
```

#### `/33-news-briefing` - 뉴스 브리핑

특정 주제의 최신 뉴스를 정리합니다.

```
/33-news-briefing AI 산업 동향
```

#### `/51-daily-note` - 일일 기록의 시작점

매일 아침 실행하여 오늘 하루를 계획하세요.

```
/51-daily-note
```

#### `/52-weekly-note` - 주간 회고

한 주를 마무리하며 돌아보는 시간.

```
/52-weekly-note
```

---

## 일일 워크플로우

### 아침

```
/51-daily-note
```
→ 오늘 할 일 정리

### 작업 중

```
/31-web-clip [좋은 자료 URL]
/21-idea-note [떠오른 아이디어]
```
→ 자동으로 적절한 폴더에 저장

### 저녁

Daily Note에서 "오늘 한 일" 정리

### 주말

```
/52-weekly-note
```
→ 이번 주 회고

---

## 커스터마이징

### 20-created 하위 폴더

"내가 주로 뭘 만드나?" 기준으로 수정

예시:
- 기획자: `21-specs/`, `22-meetings/`, `23-research/`
- 마케터: `21-campaigns/`, `22-contents/`, `23-reports/`

### 30-collected 하위 폴더

"내가 주로 어디서 자료 가져오나?" 기준으로 수정

예시:
- `31-trends/` - 트렌드 자료
- `32-competitors/` - 경쟁사 분석
- `33-references/` - 레퍼런스

---

## 문제 해결

### "command not found: claude"

→ Claude Code가 설치 안 됨. [설치 가이드](https://docs.anthropic.com/ko/docs/claude-code/getting-started) 확인

### "Authentication failed"

→ Claude Pro 미구독 또는 로그인 필요. `claude login` 실행

### 한글 깨짐

→ VSCode 터미널 인코딩 설정 확인

---

## 문의 및 커뮤니티

- 카톡 오픈채팅: [20기 AI워크스페이스](https://open.kakao.com/o/gRW6fE7h)
- 지피터스 게시판: [gpters.org](https://gpters.org)

---

## 라이선스

이 저작물은 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.ko) 라이선스를 따릅니다.

- **자유롭게 사용·수정·배포** 가능
- **저작자 표시 필수**: 안상영, 정혜지 (GPTers 20기)
- **동일 조건 변경 허락**: 파생 저작물도 동일한 라이선스 적용

저작권 관련 문의: [@context.a](https://www.threads.net/@context.a) (정혜지)

---

**Made with Claude Code for GPTers 20기**

*스터디장: 안상영 & 정혜지*
*버전: v1.0.0 | 2026-01-14*
