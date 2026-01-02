# Daily Note 생성

오늘 날짜의 Daily Note를 생성합니다.

## 사용법

```
/daily-note
```

---

## 작업 흐름

### Step 1: 날짜 확인

1. 오늘 날짜 확인 (한국 시간 기준)
2. 파일명 형식: `YYYY-MM-DD.md`
3. 저장 경로: `50-periodic/daily/`

### Step 2: 기존 파일 확인

- 이미 오늘 Daily Note가 있으면: 내용 표시하고 종료
- 없으면: 새로 생성

### Step 3: Daily Note 생성

다음 구조로 생성:

```markdown
---
date: YYYY-MM-DD
type: daily
tags:
  - daily-note
---

# YYYY-MM-DD (요일)

## 오늘 할 일

- [ ]

## 오늘 한 일

-

## 메모

-

## 내일 할 일

- [ ]

---

[[YYYY-MM-DD(어제)|어제]] | [[YYYY-MM-DD(내일)|내일]]
```

### Step 4: 완료 안내

```
✅ Daily Note 생성 완료!

📄 파일: 50-periodic/daily/YYYY-MM-DD.md

오늘 하루도 화이팅!
```

---

## 주의사항

- 타임존: Asia/Seoul (한국 시간)
- 요일은 한글로 표시 (월, 화, 수, 목, 금, 토, 일)
