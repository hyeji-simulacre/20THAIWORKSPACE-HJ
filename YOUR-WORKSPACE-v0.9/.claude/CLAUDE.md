# AI Workspace 규칙

이 폴더는 **GPTers 20기 AI 워크스페이스** 스터디용 지식관리 시스템입니다.

> **중요**: 새 명령어, 스킬, 에이전트, 폴더, 템플릿을 생성할 때는 반드시 `.claude/CONVENTIONS.md` 파일을 먼저 읽고 규칙을 따르세요.

---

## 폴더 구조 규칙 (게으른 자들을 위한 출처주의)

```
AI-Workspace/
├── 00-templates/      ← 반복 사용 서식
├── 10-working/        ← 지금 진행 중인 것
├── 20-created/        ← 내가 만든 것
├── 30-collected/      ← 외부에서 가져온 것
├── 40-archive/        ← 끝난 것
└── 50-periodic/       ← 정기 기록 (daily/weekly)
```

---

## 분류 핵심 질문

**"이거 내가 만들었나? 외부에서 가져왔나?"**

| 질문 | 답변 | 폴더 |
|------|------|------|
| 반복 사용 양식? | 예 | `00-templates/` |
| 지금 진행 중 프로젝트? | 예 | `10-working/` |
| 내가 만들었나? | 예 | `20-created/` |
| 외부에서 왔나? | 예 | `30-collected/` |
| 끝난 프로젝트? | 예 | `40-archive/` |
| 날짜 기반? | 예 | `50-periodic/` |

---

## 하위 폴더 구조

### 20-created (내가 만든 것)

```
20-created/
├── 21-ideas/          ← 아이디어, 기획
└── 22-reading-notes/  ← 독서노트 (책, 논문)
```

### 30-collected (외부에서 가져온 것)

```
30-collected/
├── 31-web-scraps/     ← 웹 스크래핑 결과물
├── 32-youtube/        ← YouTube 자막 추출물
└── 33-news/           ← 뉴스 브리핑
```

### 50-periodic (정기 기록)

```
50-periodic/
├── 51-daily/          ← 일일 노트
└── 52-weekly/         ← 주간 리뷰
```

---

## 파일 이름 규칙

| 유형 | 형식 | 예시 |
|------|------|------|
| Daily Note | `YYYY-MM-DD.md` | `2026-01-14.md` |
| Weekly Note | `YYYY-WXX.md` | `2026-W03.md` |
| 아이디어 | `YYYY-MM-DD 제목.md` | `2026-01-14 AI 회의록 서비스.md` |
| 웹클립 | `YYYYMMDD-제목.md` | `20260114-마케팅트렌드.md` |

---

## 사용 가능한 슬래시 명령어

| 명령어 | 설명 | 저장 위치 |
|--------|------|-----------|
| `/21-idea-note` | 아이디어 노트 생성 | `20-created/21-ideas/` |
| `/22-reading-note` | 독서 노트 생성 | `20-created/22-reading-notes/` |
| `/33-news-briefing` | 뉴스 브리핑 정리 | `30-collected/33-news/` |
| `/51-daily-note` | 오늘 Daily Note 생성 | `50-periodic/51-daily/` |
| `/52-weekly-note` | 이번 주 Weekly Note 생성 | `50-periodic/52-weekly/` |

## 에이전트

| 에이전트 | 트리거 | 저장 위치 |
|----------|--------|-----------|
| `roadmap-builder` | "로드맵 짜줘", "프로젝트 계획 세워줘" | `10-working/1X-프로젝트명/` |

---

## 스킬 기본 저장 경로

| 스킬 | 기본 저장 경로 | 비고 |
|------|---------------|------|
| YouTube 자막 | `30-collected/32-youtube/` | 고정 |
| 웹 스크래핑 | `30-collected/31-web-scraps/` | 고정 |
| PDF Reader | 원본 PDF 위치 | 용도에 따라 질문 |
| Notion 다운로드 | `10-working/{프로젝트}/notion/` | 프로젝트 선택 |
| GDrive 다운로드 | `10-working/{프로젝트}/gdrive/` | 프로젝트 선택 |

---

## 작업 흐름 예시

### 아침 루틴

```
/51-daily-note
```
→ 오늘 할 일 정리

### 아이디어가 떠오르면

```
/21-idea-note 새로운 서비스 아이디어
```
→ 자동으로 20-created/21-ideas/에 저장

### 주말 회고

```
/52-weekly-note
```
→ 이번 주 정리

---

## Johnny Decimal 번호 체계 (필수)

**모든 폴더/파일 생성 시 반드시 번호 체계를 따라야 합니다.**

### 프로젝트 폴더 (10-working)

새 프로젝트 생성 시:
1. `10-working/` 내 기존 `1X-*` 폴더 스캔
2. 가장 높은 번호 + 1 할당
3. 폴더명: `1X-프로젝트명/`
4. 파일명: `XX1-roadmap.md`, `XX2-daily-schedule.md`

```
예시: 11, 12 존재 → 새 프로젝트는 13-프로젝트명/
     파일: 131-roadmap.md, 132-daily-schedule.md
```

### 번호 할당 프로세스

```
새 폴더/파일 생성 요청
        │
        ▼
기존 폴더 스캔 (해당 위치)
        │
        ▼
다음 번호 계산
        │
        ▼
사용자에게 제안: "13-xxx로 생성할까요?"
        │
        ▼
확인 후 생성
```

### 자세한 규칙

> 상세 번호 체계는 `.claude/CONVENTIONS.md` 참조

---

## 주의사항

- 모든 날짜는 **한국 시간(KST)** 기준
- **새 프로젝트/파일 생성 시 번호 체계 필수 적용**
- 파일은 항상 적절한 폴더에 저장
- 프로젝트 완료 시 `40-archive/`로 이동
- 새 폴더 생성 시 숫자 prefix 유지 (XX-폴더명)

---

*GPTers 20기 AI 워크스페이스 스터디*
*Made with Claude Code*
