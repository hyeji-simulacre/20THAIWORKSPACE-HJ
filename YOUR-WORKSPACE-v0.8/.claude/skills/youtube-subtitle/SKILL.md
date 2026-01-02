---
name: youtube_subtitle_eduv
description: YouTube 영상의 자막을 JSON으로 추출하는 스킬.
---

# YouTube Subtitle

YouTube 영상의 자막을 JSON으로 저장합니다.

---

## 🚀 3분 퀵스타트

### 설치 (최초 1회)
```powershell
# 워크스페이스 루트에서
.\.venv\Scripts\Activate.ps1
python -m pip install -r .claude/skills/_education_skills/youtube_subtitle_eduv/requirements.txt
```

### 실행
```powershell
python .claude\skills\_education_skills\youtube_subtitle_eduv\scripts\yt_sub_extract_yt-transcript-api_eduv.py "YOUTUBE_URL"
```

### 업무 활용 예시
- **마케터**: 경쟁사 마케팅 영상 내용 분석
- **교육자**: 강의 영상 자막 추출하여 학습 자료 제작
- **연구원**: 웨비나/세미나 내용 문서화

### 클로드코드로 더 쉽게
```
"유튜브 영상 [URL]의 자막을 추출하고 핵심 내용 5가지로 요약해줘"
```

---

## 환경 설정 및 의존성 설치

이 스킬을 사용하기 전에 독립적인 실행 환경(가상환경)을 구성하는 것을 권장합니다.

1.  **가상환경 확인 및 생성** (워크스페이스 루트 기준):
    ```powershell
    # 가상환경이 없다면 생성 (사용자 동의 시)
    if (-not (Test-Path ".venv")) { python -m venv .venv }

    # 가상환경 활성화
    .\.venv\Scripts\Activate.ps1
    ```

2.  **의존성 확인 및 설치**:
    ```powershell
    # 설치된 패키지 확인
    python -m pip list

    # 필요한 패키지가 없다면 설치
    python -m pip install -r .claude/skills/_education_skills/youtube_subtitle_eduv/requirements.txt
    ```

> **주의**: 가상환경을 사용하지 않고 전역(Global) 환경에 설치할 경우 다른 프로젝트와 충돌할 수 있습니다. 명시적인 이유가 없다면 가상환경을 사용하세요.

## 스킬 기능

### **자막 추출**
- **`yt_sub_extract_yt-transcript-api_eduv.py`**
  - `youtube-transcript-api` 사용
  - 속도 빠르고 안정적
  - Rate Limit 회피 가능
  - 자막 + 메타 정보 전체 저장 (언어, 번역 가능 여부, 사용 가능한 자막 목록 등)
  - 출력: `50_resources/57_youtube_CA/YYYYMMDD_<videoId>_transcript.json`

**실행:**
```powershell
python ".claude\skills\_education_skills\youtube_subtitle_eduv\scripts\yt_sub_extract_yt-transcript-api_eduv.py" "https://www.youtube.com/watch?v=VIDEO_ID"
```

## 의존성 상세
- **Python 3.12.4** (`python` 명령)
- **필수 라이브러리**: `youtube-transcript-api==1.2.3`

## 🗂️ 출력 위치

모든 스크립트는 다음 경로에 저장합니다:
```
50_resources/57_youtube_CA/
└── YYYYMMDD_<videoId>_transcript.json # 자막
```

## 🛠️ 트러블슈팅

### "패키지 없음" 오류
```powershell
# 가상환경 활성화 후
python -m pip install -r .claude/skills/_education_skills/youtube_subtitle_eduv/requirements.txt
```

### "자막 없음" 오류
- 영상에 자동 생성 자막이 없는 경우
- 제한된 영상 (연령 제한, 비공개 등)
