`clone`은 **GitHub에 저장된 프로젝트 전체를 내 컴퓨터로 복사하는 기능**입니다.

단순히 파일만 다운로드하는 것이 아니라 다음 정보까지 함께 가져옵니다.

- 프로그램 소스코드
    
- 폴더 구조
    
- 전체 커밋 기록
    
- 브랜치 정보
    
- GitHub 원격 저장소 연결 정보
    

## 기본 명령어

```powershell
git clone GitHub저장소주소
```

예:

```powershell
git clone https://github.com/사용자이름/prompt-manager.git
```

실행하면 현재 위치에 `prompt-manager` 폴더가 자동으로 만들어집니다.

```text
현재 폴더
└── prompt-manager
    ├── .git
    ├── .gitignore
    ├── README.md
    └── prompt_manager.py
```

프로젝트 폴더로 이동합니다.

```powershell
cd prompt-manager
```

VS Code에서 엽니다.

```powershell
code .
```

## Clone 이후의 일반적인 작업 흐름

```powershell
git clone https://github.com/사용자이름/prompt-manager.git
cd prompt-manager
code .
```

그다음 가상환경을 생성합니다.

```powershell
py -m venv .venv
```

가상환경을 활성화합니다.

```powershell
.\.venv\Scripts\Activate.ps1
```

프로그램을 실행합니다.

```powershell
python prompt_manager.py
```

## Download ZIP과 차이

|구분|`git clone`|Download ZIP|
|---|---|---|
|프로그램 파일|가져옴|가져옴|
|커밋 기록|가져옴|가져오지 않음|
|브랜치 정보|가져옴|가져오지 않음|
|GitHub 연결|자동 연결|연결되지 않음|
|`git pull` 사용|가능|바로 사용할 수 없음|
|`git push` 사용|권한이 있으면 가능|별도 Git 설정 필요|

GitHub 프로젝트를 계속 수정하거나 협업하려면 ZIP 다운로드보다 `git clone`을 사용하는 것이 좋습니다.

## Clone 후 GitHub 연결 확인

```powershell
git remote -v
```

결과 예:

```text
origin  https://github.com/사용자이름/prompt-manager.git (fetch)
origin  https://github.com/사용자이름/prompt-manager.git (push)
```

`origin`은 복제한 GitHub 저장소에 붙은 기본 이름입니다.

## Clone과 Pull의 차이

- `clone`: 프로젝트를 내 컴퓨터에 **처음 한 번 가져올 때**
    
- `pull`: 이미 Clone한 프로젝트에서 **최신 변경사항만 추가로 가져올 때**
    

```text
최초 작업: git clone
이후 업데이트: git pull
```

이미 컴퓨터에 현재 프로젝트 폴더가 있다면 같은 위치에서 다시 `clone`할 필요는 없습니다. 그 경우에는 다음 명령으로 최신 변경사항만 가져오면 됩니다.

```powershell
git pull origin main
```