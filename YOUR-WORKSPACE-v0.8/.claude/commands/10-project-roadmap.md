# Project Roadmap 생성

프로젝트의 일일 로드맵을 생성합니다.

## 사용법

```
/project-roadmap [프로젝트명]
```

### 예시

```
/project-roadmap 신규 서비스 기획
/project-roadmap Q1 마케팅 캠페인
```

---

## 작업 흐름

### Step 1: 프로젝트 확인

1. `10-working/` 폴더에서 해당 프로젝트 폴더 찾기
2. 없으면: 새 프로젝트 폴더 생성할지 물어보기

### Step 2: 로드맵 파일 확인

- 프로젝트 폴더 내 `daily-roadmap.md` 확인
- 있으면: 오늘 날짜 섹션 추가
- 없으면: 새로 생성

### Step 3: 로드맵 업데이트

**새 파일 생성 시:**

```markdown
---
project: [프로젝트명]
created: YYYY-MM-DD
status: active
tags:
  - project
  - roadmap
---

# [프로젝트명] Daily Roadmap

## 프로젝트 개요

- 목표:
- 기간:
- 담당:

---

## YYYY-MM-DD (요일)

### 오늘 할 일

- [ ]

### 완료한 일

-

### 메모

-

---
```

**기존 파일에 추가 시:**

```markdown
---

## YYYY-MM-DD (요일)

### 오늘 할 일

- [ ]

### 완료한 일

-

### 메모

-
```

### Step 4: 완료 안내

```
✅ Project Roadmap 업데이트 완료!

📄 파일: 10-working/[프로젝트명]/daily-roadmap.md
📅 오늘: YYYY-MM-DD

"오늘 할 일"을 채우고 시작하세요!
```

---

## 프로젝트 폴더 구조

```
10-working/
└── [프로젝트명]/
    ├── daily-roadmap.md    ← 일일 로드맵
    ├── 00-overview.md      ← 프로젝트 개요 (선택)
    └── [기타 자료들]
```

## 상태 표시

- `active`: 진행 중
- `paused`: 일시 중지
- `completed`: 완료
- `archived`: 보관

## 팁

- 매일 아침 `/project-roadmap` 실행
- 저녁에 "완료한 일" 정리
- 완료된 프로젝트는 `40-archive/`로 이동
