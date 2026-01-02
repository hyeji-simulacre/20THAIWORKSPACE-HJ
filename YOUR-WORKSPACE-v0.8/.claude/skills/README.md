# 🚀 교육용 스킬 가이드 (eduv)

> **빠르게 따라하고 업무에 바로 사용하기**
>
> 이론 최소화 · 실무 중심 · 10분 완성

---

## 📖 시작하기

### 1️⃣ 환경 설정 (5분, 최초 1회)

```powershell
# PowerShell 열기
# 워크스페이스 루트로 이동
cd D:\1my_1stAI_Agent

# 가상환경 생성 및 활성화
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**에러 발생 시**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2️⃣ 첫 스킬 실행 (5분)

**추천**: YouTube 자막 추출부터 시작

```powershell
# 패키지 설치
pip install -r .claude/skills/_educatoin_skills/youtube_subtitle_eduv/requirements.txt

# 실행
python .claude\skills\_educatoin_skills\youtube_subtitle_eduv\scripts\yt_sub_extract_yt-transcript-api_eduv.py "YOUTUBE_URL"
```

✅ **성공!** 이제 업무에 활용하세요.

---

## 📚 스킬 목록

### 난이도별 추천 순서

| 순서 | 스킬 | 소요 | 난이도 | 업무 활용도 | 문서 |
|------|------|------|--------|-------------|------|
| 1 | YouTube 자막 추출 | 5분 | ⭐ | ⭐⭐⭐⭐⭐ | [SKILL.md](youtube_subtitle_eduv/SKILL.md) |
| 2 | PDF 텍스트 추출 | 5분 | ⭐ | ⭐⭐⭐⭐⭐ | [SKILL.md](pdf_reader_eduv/SKILL.md) |
| 3 | 커스텀 스크래핑 | 15분 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | [SKILL.md](create_scrapping_eduv/SKILL.md) |

---

## 🎯 스킬별 빠른 참조

### 1. YouTube 자막 추출 (`youtube_subtitle_eduv`)

**설치**:
```powershell
pip install -r .claude/skills/_educatoin_skills/youtube_subtitle_eduv/requirements.txt
```

**실행**:
```powershell
python .claude\skills\_educatoin_skills\youtube_subtitle_eduv\scripts\yt_sub_extract_yt-transcript-api_eduv.py "YOUTUBE_URL"
```

**업무 활용**:
- 강의 영상 → 학습 자료
- 웨비나 → 회의록
- 경쟁사 발표 → 분석 자료

---

### 2. PDF 텍스트 추출 (`pdf_reader_eduv`)

**설치**:
```powershell
pip install -r .claude/skills/_educatoin_skills/pdf_reader_eduv/requirements.txt
```

**실행**:
```powershell
python .claude\skills\_educatoin_skills\pdf_reader_eduv\scripts\pdf_to_text_eduv.py "파일.pdf"
```

**업무 활용**:
- 계약서 → 핵심 조항 추출
- 논문 → 요약
- 보고서 → 데이터 추출

---

### 3. 커스텀 스크래핑 (`create_scrapping_eduv`)

**설치**:
```powershell
pip install -r .claude/skills/_educatoin_skills/create_scrapping_eduv/requirements.txt
playwright install chromium
```

**사용법**: 클로드코드에게 직접 요청
```
"https://example.com 사이트의 [원하는 데이터]를 스크래핑하는 스크립트 만들어줘"
```

**업무 활용**:
- 채용 공고 자동 수집
- 경쟁사 가격 모니터링
- 뉴스/블로그 콘텐츠 수집

---

## 💼 업무별 활용 가이드

### 📊 마케터

#### 경쟁사 분석 자동화
```
1. YouTube 자막: 경쟁사 마케팅 영상 분석
2. 커스텀 스크래핑: 경쟁사 블로그 콘텐츠 수집
3. 클로드코드: "트렌드 3가지 분석해줘"
```

#### 콘텐츠 리서치
```
1. PDF 추출: 업계 보고서 핵심 내용 정리
2. 클로드코드: "콘텐츠 아이디어 10개 제안해줘"
```

---

### 💻 개발자/PM

#### 기술 문서 자동화
```
1. PDF 추출: API 문서 텍스트화
2. YouTube 자막: 기술 강의 내용 정리
3. 클로드코드: "핵심 코드 예제만 추출해줘"
```

#### 경쟁 제품 분석
```
1. 커스텀 스크래핑: 경쟁 제품 기능 목록 수집
2. 클로드코드: "우리 제품과 비교 분석해줘"
```

---

### 📚 연구원/학생

#### 논문 리서치
```
1. PDF 추출: 논문 여러 개 → Markdown
2. 클로드코드: "핵심 연구 방법론 비교해줘"
3. 참고문헌 자동 정리
```

#### 데이터 수집
```
1. 커스텀 스크래핑: 학술 데이터베이스 검색 자동화
2. YouTube 자막: 강의 내용 텍스트화
```

---

### 👔 법무/HR

#### 문서 분석
```
1. PDF 추출: 계약서 → 핵심 조항 추출
2. 클로드코드: "리스크 요소 3가지 분석해줘"
```

#### 채용 공고 모니터링
```
1. 커스텀 스크래핑: 경쟁사 채용 공고 수집
2. 클로드코드: "우리 공고와 비교 분석해줘"
```

---

## 🔗 워크플로우 템플릿

### 템플릿 1: 주간 트렌드 리포트

```
월요일:
1. 경쟁사 블로그 스크래핑 (15분)

화요일:
2. 수집 데이터 클로드 분석 (20분)
   "트렌드 5가지와 인사이트 도출해줘"

수요일:
3. 경영진 보고서 생성 (10분)
   "1페이지 요약 보고서 만들어줘"

총 소요: 45분 → 기존 반나절 업무 자동화
```

---

### 템플릿 2: 콘텐츠 제작 파이프라인

```
Step 1: 자료 수집 (30분)
- YouTube 자막 10개
- PDF 보고서 5개
- 블로그 글 20개

Step 2: 클로드 분석 (15분)
"공통 주제 3가지와 독창적 관점 찾아줘"

Step 3: 콘텐츠 초안 (20분)
"블로그 글 3개 초안 만들어줘"

총 소요: 65분 → 기존 하루 업무 자동화
```

---

### 템플릿 3: 경쟁사 모니터링

```
매일 오전:
1. 경쟁사 가격 스크래핑 (5분)
2. 변동사항 자동 알림

매주:
3. 주간 변동 리포트 (10분)
   "가격 변동 추이와 시사점 분석해줘"

매월:
4. 월간 전략 리포트 (30분)
   "대응 전략 3가지 제안해줘"
```

---

## 🛠️ 필수 트러블슈팅

### ❌ "python을 찾을 수 없습니다"
```powershell
# Python 설치 확인
where python

# 없으면 https://www.python.org/downloads/ 설치
# "Add to PATH" 반드시 체크
```

---

### ❌ "스크립트 실행 불가"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### ❌ "ModuleNotFoundError"
```powershell
# 가상환경 활성화 확인
.\.venv\Scripts\Activate.ps1

# 패키지 재설치
pip install -r [스킬경로]/requirements.txt
```

---

### ❌ "Playwright 에러"
```powershell
playwright install chromium
```

---

## 💡 클로드코드 활용 팁

### 자연어로 간단하게
```
❌ 복잡한 명령어 외우기
✅ "유튜브 영상 [URL] 자막 추출해줘"
```

### 분석까지 한 번에
```
"PDF 파일 내용 추출하고 핵심 3가지로 요약해줘"
"스크래핑 결과를 엑셀로 정리해줘"
"이 데이터로 그래프 만들어줘"
```

### 정기 실행 자동화
```
"매주 월요일 오전 9시에 GPTers 스크래핑 실행하는 스케줄러 만들어줘"
```

---

## 📈 성과 측정

### Before (수동 작업)
- 자료 수집: 2시간
- 정리: 1시간
- 분석: 1시간
- **총 4시간**

### After (스킬 + 클로드코드)
- 자료 수집: 10분 (자동)
- 정리: 5분 (자동)
- 분석: 10분 (AI 지원)
- **총 25분**

**시간 절감: 93% ⬇️**

---

## 🎯 다음 단계

### 1단계: 하나씩 익히기
- [ ] YouTube 자막 추출 성공
- [ ] PDF 추출 성공
- [ ] 스크래핑 성공

### 2단계: 업무에 적용
- [ ] 반복 작업 1개 자동화
- [ ] 워크플로우 구축
- [ ] 시간 절감 측정

### 3단계: 고도화
- [ ] 여러 스킬 조합
- [ ] 정기 실행 자동화
- [ ] 팀 공유

---

## 📞 도움이 필요하면

**클로드코드에게 물어보세요**:
```
"이 에러를 어떻게 해결하나요?
[에러 메시지 복사]"
```

---

## 📚 추가 자료

- **통합 가이드**: [00_QUICK_START.md](00_QUICK_START.md)
- **각 스킬 상세 문서**: 해당 폴더의 `SKILL.md` 참고

---

**🚀 10분 만에 시작하고, 바로 업무에 활용하세요!**
