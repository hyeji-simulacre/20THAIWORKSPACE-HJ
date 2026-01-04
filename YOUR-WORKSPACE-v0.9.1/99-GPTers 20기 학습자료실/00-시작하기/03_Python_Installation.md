# 파이썬(Python) 설치 가이드 (Windows 10/11)

이 문서는 **Windows 10/11**에서 **Python(파이썬)**을 설치하는 방법을 아주 자세히 설명합니다.
초등학생도 따라 할 수 있도록 **하나씩, 천천히** 진행합니다.

이 워크스페이스(`AI-Workspace`)에서 자동화 스킬을 실행하려면 Python이 꼭 필요합니다.

---

## 이 가이드를 끝내면 할 수 있는 것

- Python 설치 완료
- PowerShell(파워셸)에서 `python --version`으로 설치 확인
- `pip`(파이썬 도구 설치기)도 같이 확인
- 다음 단계(가상환경 만들기)까지 준비 완료

---

## 0) 먼저 확인: 이미 Python이 설치되어 있나요? (1분)

Python을 **이미 설치**했을 수도 있어요. 먼저 확인해볼게요.

### 0-1. PowerShell(파워셸) 열기

1. 키보드에서 `Windows` 키를 누르세요.
2. `PowerShell`이라고 입력하세요.
3. 검색 결과에서 **Windows PowerShell**을 클릭하세요.

### 0-2. Python 버전 확인하기

PowerShell 창에 아래를 입력하고 `Enter`를 누르세요.

```powershell
python --version
```

#### 결과가 이렇게 나오면 성공

- `Python 3.12.4` 또는 `Python 3.12.x` 처럼 **3.12로 시작**하면, 대부분 OK입니다.

#### 결과가 이렇게 나오면 설치가 필요해요

- `python을(를) 찾을 수 없습니다`
- `python은(는) 내부 또는 외부 명령, 실행할 수 있는 프로그램...`
- Microsoft Store(마이크로소프트 스토어)가 갑자기 열림

이런 경우는 아래 1번부터 따라 하세요.

---

## 1) 준비물 체크(설치 전에 이것만 확인해요)

- [ ] Windows 10 또는 Windows 11
- [ ] 인터넷 연결(다운로드 때문에 필요)
- [ ] PC에 프로그램 설치할 수 있는 권한(가끔 관리자 비밀번호가 필요할 수 있어요)

---

## 2) Python 다운로드하기 (공식 사이트에서 안전하게)

### 2-1. 브라우저 열기

Edge(엣지) 또는 Chrome(크롬)을 여세요.

### 2-2. 주소 입력하기

브라우저 맨 위 **주소창**에 아래 주소를 그대로 입력하고 `Enter`를 누르세요.

```
https://www.python.org/downloads/
```

### 2-3. 어떤 버튼을 눌러야 하나요?

다운로드 페이지에서 보통 **큰 다운로드 버튼**이 보입니다.

- 버튼 글자 예시: `Download Python 3.12.x`
- 여기서 `3.12`가 보이면, 우리가 원하는 버전(3.12 계열)에 가깝습니다.

> 참고  
> 이 워크스페이스는 `Python 3.12.4`를 기준으로 만들어졌습니다.  
> 다운로드 버튼에 `3.12.4`가 딱 보이지 않아도, `3.12.x`(3.12로 시작하는 버전)면 대부분 잘 동작합니다.

### 2-4. 다운로드 파일은 어디에 생기나요?

대부분 `다운로드(Downloads)` 폴더에 생깁니다.

- 파일 이름 예시: `python-3.12.4-amd64.exe` 또는 `python-3.12.x-amd64.exe`

---

## 3) Python 설치하기 (가장 중요한 체크 1개)

이제 다운로드한 설치 파일(`.exe`)을 실행할 차례입니다.

### 3-1. 설치 파일 실행하기

1. 파일 탐색기(폴더 아이콘)를 여세요.
2. `다운로드(Downloads)` 폴더로 이동하세요.
3. `python-3.12.x-amd64.exe` 같은 파일을 **더블 클릭**하세요.
4. “이 앱이 디바이스를 변경하도록 허용하시겠습니까?”가 나오면 **예(Yes)**를 누르세요.

### 3-2. 첫 화면에서 꼭 해야 하는 것: PATH 체크

설치 화면 맨 아래쪽에 이런 체크박스가 보일 수 있어요.

- `Add python.exe to PATH`

이 체크박스는 **반드시 체크**하세요.

#### PATH가 뭐예요? (아주 쉽게)

- `PATH`는 “Windows가 프로그램을 찾는 길(주소록)”이에요.
- 이걸 체크하면, PowerShell에서 `python`이라고 입력했을 때 **Python을 바로 찾을 수 있어요**.

### 3-3. 설치 시작하기

초보자는 보통 아래 버튼이 가장 쉽습니다.

- `Install Now`

`Install Now`를 누르고, 설치가 끝날 때까지 기다리세요. (1~3분 정도 걸릴 수 있어요)

### 3-4. 설치가 끝나면 한 번 더 눌러야 하는 버튼(있으면 눌러요)

설치가 끝나면 이런 문구가 보일 수 있어요.

- `Disable path length limit`

이 버튼이 보이면 눌러주세요. 그리고 확인 창이 나오면 **Yes**를 누르세요.

그 다음 `Close`로 설치 창을 닫으면 됩니다.

---

## 4) 설치 확인하기 (여기가 제일 중요해요)

설치가 끝났다고 해도, “진짜로 됐는지” 꼭 확인해야 합니다.

### 4-1. PowerShell을 새로 열기(중요)

설치 전부터 PowerShell을 켜놓았다면, **그 창은 닫고 새로 여세요.**

Windows는 가끔 “새로 열린 창”에서만 PATH 변경을 제대로 반영해요.

### 4-2. 아래 3개를 차례대로 입력하기

```powershell
python --version
python -m pip --version
where python
```

### 4-3. 기대하는 결과(예시)

1) `python --version`
- `Python 3.12.4` 또는 `Python 3.12.x`

2) `python -m pip --version`
- `pip 24.x ... (python 3.12)` 처럼 나옵니다.

3) `where python`
- Python이 설치된 위치(경로)가 1줄 이상 나옵니다.

---

## 5) 자주 생기는 문제 해결(설치가 안 된 것처럼 보일 때)

여기에서 대부분 해결됩니다. 하나씩만 따라 해보세요.

---

### 문제 1) `python`을 쳤더니 Microsoft Store가 열려요

이건 Python이 없어서가 아니라, Windows가 “스토어에서 설치하라”고 유도하는 설정 때문에 생길 수 있어요.

#### 해결 방법(Windows 설정에서 끄기)

1. `Windows` 키를 누르고 **설정**(톱니바퀴)을 여세요.
2. **앱**으로 들어가세요.
3. **앱 실행 별칭(App execution aliases)** 를 찾으세요.
4. 목록에서 아래 항목이 있으면 **끔(Off)**으로 바꾸세요.
   - `python.exe`
   - `python3.exe`
5. PowerShell을 닫고 다시 열어서 아래를 다시 해보세요.

```powershell
python --version
```

---

### 문제 2) `python을(를) 찾을 수 없습니다` / `python은(는) 내부 또는 외부 명령...`

대부분 아래 중 하나입니다.

- 설치할 때 `Add python.exe to PATH`를 체크하지 않았어요.
- PowerShell을 설치 전부터 켜놔서, PATH가 아직 반영이 안 됐어요.

#### 해결 순서(쉬운 것부터)

1) PowerShell을 전부 닫고 다시 열기  
2) 그래도 안 되면 PC를 한 번 재부팅  
3) 그래도 안 되면 Python을 다시 설치(아래 5-2-1 참고)

#### 5-2-1. Python 다시 설치하는 가장 쉬운 방법

1. `다운로드(Downloads)` 폴더에서 Python 설치 파일(`python-3.12.x-amd64.exe`)을 다시 실행하세요.
2. 설치 화면이 나오면 이번에는 꼭 `Add python.exe to PATH`를 체크하세요.
3. `Install Now`로 설치하세요.
4. 설치 후 PowerShell을 새로 열고 다시 확인하세요.

```powershell
python --version
```

---

### 문제 3) `pip`이 없다고 나와요 / `pip`이 동작 안 해요

Windows에서는 `pip`만 단독으로 쓰는 것보다, 아래처럼 쓰는 게 가장 안전해요.

```powershell
python -m pip --version
```

그리고 아래로 `pip`를 최신으로 올릴 수 있어요.

```powershell
python -m pip install --upgrade pip
```

---

### 문제 4) `where python`을 했더니 여러 줄이 나와요

여러 줄이 나온다는 건, 내 컴퓨터에 Python이 **여러 개** 있을 수 있다는 뜻이에요.

- 첫 번째 줄에 나온 경로가, PowerShell에서 `python`을 쳤을 때 실제로 실행되는 Python입니다.

이 워크스페이스에서는 **`python --version`이 3.12로 시작**하도록 맞추는 것이 중요합니다.

---

### 문제 5) `python --version`이 3.12가 아니에요(예: 3.10, 3.11, 3.13)

이럴 때는 아래 중 하나를 선택하세요.

- 선택 A: Python 3.12를 추가로 설치하고, `python --version`이 3.12가 나오게 맞춘다
- 선택 B: 수업/워크스페이스 안내에 따라 “정해진 방법(예: pyenv-win)”으로 버전을 고정한다

이 문서는 “선택 A(가장 쉬운 방법)”을 기준으로 설명합니다.

---

## 6) 다음 단계(설치가 끝났다면 여기까지 하면 더 좋아요)

Python 설치가 끝났고, `python --version`이 잘 나온다면 이제 스킬을 실행할 준비가 됐습니다.

아래는 “Python 설치 다음에” 보통 바로 하는 최소 단계입니다.

### 6-1. 워크스페이스 폴더로 이동하기

```powershell
cd D:\AI-Workspace
```

### 6-2. 가상환경 만들기(최초 1회)

```powershell
python -m venv .venv
```

### 6-3. 가상환경 켜기

```powershell
.\.venv\Scripts\Activate.ps1
```

만약 “실행 정책” 에러가 나오면 아래를 1번만 실행하세요.

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 7) 최종 체크리스트(여기까지 체크되면 완료)

- [ ] PowerShell에서 `python --version`이 실행된다
- [ ] 버전이 `Python 3.12.x`로 나온다
- [ ] `python -m pip --version`이 실행된다
- [ ] (선택) `where python`에서 경로가 나온다

---

## 도움말(정말 막히면 이렇게 해주세요)

PowerShell에 나온 에러 메시지를 그대로 복사해서 Claude Code에게 이렇게 물어보면 빠르게 해결됩니다.

```text
"Python 설치를 했는데, PowerShell에서 이런 에러가 나요. 어떻게 해결하죠?
[에러 메시지 그대로 붙여넣기]"
```

