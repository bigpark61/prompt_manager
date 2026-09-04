현재 `prompt_manager.py`는 기본 기능이 잘 갖춰져 있습니다. 다음 단계로는 아래 두 가지 업그레이드를 추천합니다.

## 1. JSON 파일을 이용한 영구 저장

현재는 프로그램을 종료하면 사용자가 추가한 프롬프트와 즐겨찾기 상태가 초기화됩니다. 이를 `prompts.json` 파일에 저장하면 프로그램을 다시 실행해도 데이터가 유지됩니다.

주요 기능:

- 프로그램 시작 시 `prompts.json` 불러오기
    
- 프롬프트 추가 시 자동 저장
    
- 즐겨찾기 변경 시 자동 저장
    
- 저장 파일이 없으면 기본 프롬프트 3개 생성
    
- 데이터 손상 시 기본 데이터로 안전하게 복구
    

예상 구조:

```json
[
  {
    "prompt_id": 1,
    "title": "회의자료 핵심 요약",
    "category": "문서작성",
    "content": "다음 회의자료를 핵심 내용으로 요약해 주세요.",
    "favorite": false
  }
]
```

이 기능을 추가하면 단순 실습 프로그램에서 실제 사용할 수 있는 프롬프트 관리 도구로 발전합니다.

## 2. 프롬프트 수정 및 삭제 기능

현재 등록된 프롬프트는 조회만 가능하고 잘못 입력한 내용을 변경하거나 삭제할 수 없습니다.

추가할 메뉴는 다음과 같습니다.

```text
8. 프롬프트 수정
9. 프롬프트 삭제
```

수정 기능:

- ID로 수정할 프롬프트 선택
    
- 제목·카테고리·내용 수정
    
- Enter만 입력하면 기존 값 유지
    
- 수정 결과 확인
    

삭제 기능:

- ID로 삭제할 프롬프트 선택
    
- 삭제 전 프롬프트 정보 표시
    
- `Y/N`으로 최종 확인
    
- 삭제 후 목록에서 제거
    

추천 개발 순서는 다음과 같습니다.

```text
1단계: 수정·삭제 기능 추가
2단계: JSON 영구 저장 적용
```

두 기능을 함께 추가하면 프롬프트의 **등록·조회·검색·수정·삭제·저장**이 가능한 완전한 관리 프로그램이 됩니다.

---
.gitignore 파일을 생성하여 불필요한 파일을 제외한다. 어떤 내용인지 설명해줘

`.gitignore`는 **Git이 추적하거나 GitHub에 업로드하지 않아도 되는 파일과 폴더를 지정하는 설정 파일**입니다.

프로젝트 최상위 폴더에 다음과 같이 생성합니다.

```text
prompt_manager/
├── .git/
├── .venv/
├── .gitignore
└── prompt_manager.py
```

현재 Python 프로젝트에는 다음 내용을 추천합니다.

```gitignore
# Python이 자동으로 생성하는 캐시 파일
__pycache__/
*.py[cod]

# Python 가상환경
.venv/
venv/
env/

# 환경변수 및 비밀정보
.env
.env.*

# 테스트 및 분석 도구가 생성하는 파일
.pytest_cache/
.mypy_cache/
.coverage
htmlcov/

# 프로그램 실행 중 생성되는 로그와 임시파일
*.log
*.tmp
*.bak

# 운영체제에서 생성하는 파일
.DS_Store
Thumbs.db

# VS Code 개인 설정
.vscode/
```

## 주요 항목 설명

|항목|제외하는 내용|제외 이유|
|---|---|---|
|`__pycache__/`|Python 캐시 폴더|실행하면 자동으로 다시 생성됨|
|`*.py[cod]`|`.pyc`, `.pyo`, `.pyd` 파일|Python이 생성하는 실행 보조파일|
|`.venv/`|현재 프로젝트의 가상환경|용량이 크고 컴퓨터마다 환경이 다름|
|`venv/`, `env/`|다른 이름의 가상환경|GitHub에 올릴 필요가 없음|
|`.env`|API Key, 비밀번호 등|보안상 GitHub 업로드 금지|
|`*.log`|프로그램 실행 기록|소스코드가 아니며 계속 변경됨|
|`*.tmp`, `*.bak`|임시파일·백업파일|개발에 필요하지 않음|
|`.DS_Store`|macOS 자동 생성 파일|프로젝트와 관계없음|
|`Thumbs.db`|Windows 이미지 미리보기 정보|프로젝트와 관계없음|
|`.vscode/`|VS Code 개인 설정|사용자별 설정 차이로 충돌 가능|

## VS Code에서 `.gitignore` 생성하기

프로젝트 탐색기에서:

1 localhost. 프로젝트 폴더를 마우스 오른쪽 버튼으로 선택  
unexpected. `New File` 선택  
3. 파일 이름을 `.gitignore`로 입력  
4. 위 설정 내용을 붙여넣고 저장

파일명 앞에 점이 있고 확장자가 없다는 점에 주의해야 합니다.

```text
올바른 이름: .gitignore
잘못된 이름: .gitignore.txt
```

## Git 동작 예시

`.gitignore`가 없으면:

```text
Changes
├── prompt_manager.py
├── .venv/
├── __pycache__/
└── 여러 라이브러리 파일
```

`.gitignore`를 적용하면:

```text
Changes
├── .gitignore
└── prompt_manager.py
```

즉, 실제 작성한 프로그램과 Git 설정 파일만 Git의 관리 대상이 됩니다.

## Git 상태 확인

파일을 만든 후 터미널에서 실행합니다.

```bash
git status
```

정상이라면 `.venv`와 `__pycache__`는 변경 목록에 나타나지 않습니다.

그다음 `.gitignore`를 Git에 기록합니다.

```bash
git add .gitignore
git commit -m "불필요한 파일 제외 설정 추가"
```

## 이미 Git이 추적하고 있다면

`.gitignore`는 아직 Git에 등록되지 않은 파일에 적용됩니다. `.venv` 등이 이미 Git에 등록된 상태라면 `.gitignore`에 추가해도 계속 표시될 수 있습니다.

이 경우 Git의 추적 대상에서만 제거합니다.

```bash
git rm -r --cached .venv
git rm -r --cached __pycache__
git commit -m "가상환경 및 캐시 파일 추적 제외"
```

`--cached`를 사용하므로 컴퓨터의 실제 폴더는 삭제되지 않고 Git의 추적만 해제됩니다.

핵심적으로 `.gitignore`는 **프로그램 실행에 불필요한 자동 생성 파일, 개인 환경 파일, 보안정보가 GitHub에 올라가는 것을 막는 역할**을 합니다.

---
github 에 올라가 있는 **pycache** 를 제거하는 방법

GitHub에 올라간 `__pycache__`를 제거하려면, **로컬 파일은 유지하고 Git 추적만 해제한 뒤 Commit·Push**하면 됩니다.

## 1. `.gitignore`에 추가

프로젝트 최상위의 `.gitignore` 파일에 다음 내용을 넣습니다.

```gitignore
# Python 캐시
__pycache__/
*.py[cod]
```

이 설정은 모든 하위 폴더의 `__pycache__`도 앞으로 Git에 올라가지 않게 합니다.

## 2. Git 추적에서 제거

프로젝트 최상위 폴더의 VS Code 터미널에서 실행합니다.

`__pycache__`가 최상위 폴더에 있다면:

```powershell
git rm -r --cached __pycache__
```

여러 하위 폴더에 있다면:

```powershell
git rm -r --cached --ignore-unmatch ":(glob)**/__pycache__/**"
```

여기서 `--cached`는 실제 컴퓨터의 파일을 삭제하지 않고 Git과 GitHub에서만 제거한다는 의미입니다.

## 3. 변경 상태 확인

```powershell
git status
```

다음과 비슷하게 표시되면 정상입니다.

```text
deleted: __pycache__/prompt_manager.cpython-313.pyc
modified: .gitignore
```

Git의 관점에서는 GitHub에서 파일을 삭제하기 때문에 `deleted`로 표시됩니다.

## 책4. Commit과 Push

```powershell
git add .gitignore
git commit -m "Python 캐시 파일 제거 및 추적 제외"
git push origin main
```

현재 브랜치가 `main`이라면 GitHub의 `__pycache__`가 제거됩니다.

## 전체 명령 정리

```powershell
git rm -r --cached --ignore-unmatch ":(glob)**/__pycache__/**"
git add .gitignore
git commit -m "Python 캐시 파일 제거 및 추적 제외"
git push origin main
```

Push 후 GitHub 페이지를 새로고침해서 `__pycache__`가 사라졌는지 확인하세요.

참고로 이 방법은 현재 GitHub 파일 목록에서는 제거하지만 과거 커밋 기록까지 삭제하지는 않습니다. `__pycache__`는 보안정보가 아니므로 일반적으로 과거 이력까지 제거할 필요는 없습니다.