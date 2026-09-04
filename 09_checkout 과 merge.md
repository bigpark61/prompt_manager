`checkout`과 `merge`는 브랜치를 활용할 때 자주 사용하는 Git 기능입니다.

- `checkout`: 작업할 브랜치로 이동
    
- `merge`: 다른 브랜치의 변경사항을 현재 브랜치에 합침
    

## 1. checkout 기능

`checkout`은 특정 브랜치로 이동하거나 과거 커밋의 파일 상태를 확인할 때 사용합니다.

### 브랜치 이동

```powershell
git checkout main
```

의미:

> 현재 작업 위치를 `main` 브랜치로 변경한다.

개발 브랜치로 이동하려면:

```powershell
git checkout feature/edit-delete
```

### 브랜치를 만들면서 이동

```powershell
git checkout -b feature/edit-delete
```

위 명령은 다음 두 작업을 한 번에 수행합니다.

```text
feature/edit-delete 브랜치 생성
→ feature/edit-delete 브랜치로 이동
```

현재는 역할을 명확하게 구분한 `git switch` 사용을 권장합니다.

|기존 명령|권장 명령|의미|
|---|---|---|
|`git checkout main`|`git switch main`|브랜치 이동|
|`git checkout -b feature/edit-delete`|`git switch -c feature/edit-delete`|브랜치 생성 후 이동|

## 2. merge 기능

`merge`는 다른 브랜치에서 개발한 내용을 현재 브랜치에 합치는 기능입니다.

예를 들어 브랜치 구조가 다음과 같다고 가정합니다.

```text
main
└── feature/edit-delete
    ├── 수정 기능
    └── 삭제 기능
```

`feature/edit-delete`의 기능을 `main`에 합치려면 먼저 `main`으로 이동해야 합니다.

```powershell
git switch main
```

그다음 병합합니다.

```powershell
git merge feature/edit-delete
```

중요한 원칙은 다음과 같습니다.

> `git merge 합칠브랜치` 명령은 합쳐질 목적지 브랜치에서 실행합니다.

즉:

```powershell
git switch main
git merge feature/edit-delete
```

의미는 다음과 같습니다.

```text
feature/edit-delete의 변경사항을 현재 main에 합친다.
```

반대로 실행하면 결과가 달라집니다.

```powershell
git switch feature/edit-delete
git merge main
```

이는 `main`의 변경사항을 `feature/edit-delete`로 가져오는 것입니다.

## 3. 전체 실습 예시

### 1단계: main 확인

```powershell
git switch main
git status
```

### 2단계: 기능 브랜치 생성

```powershell
git switch -c feature/edit-delete
```

### 3단계: 프로그램 수정

VS Code에서 `prompt_manager.py`에 수정·삭제 기능을 추가합니다.

### 4단계: 기능 커밋

```powershell
git add prompt_manager.py
git commit -m "프롬프트 수정 및 삭제 기능 추가"
```

### 5단계: main으로 이동

```powershell
git switch main
```

이 시점에 `prompt_manager.py`를 실행하면 수정·삭제 기능이 없는 이전 프로그램이 나타납니다.

```powershell
python prompt_manager.py
```

### 6단계: 기능 브랜치 병합

```powershell
git merge feature/edit-delete
```

다시 실행하면 수정e 수정·삭제 기능이 포함됩니다.

```powershell
python prompt_manager.py
```

### 7단계: GitHub에 올리기

```powershell
git push origin main
```

### 8단계: 작업이 끝난 브랜치 삭제

```powershell
git branch -d feature/edit-delete
```

## 4. checkout과 merge의 관계

```text
main에서 리더 → feature 브랜치 생성
→ checkout/switch로 feature 이동
→ 프로그램 수정
→ commit
→ checkout/switch로 main 이동
→ merge로 기능 합치기
```

실제 명령은 다음과 같습니다.

```powershell
git switch main
git switch -c feature/edit-delete

# 프로그램 수정

git add prompt_manager.py
git commit -m "프롬프트 수정 및 삭제 기능 추가"

git switch main
git merge feature/edit-delete
git push origin main
```

## 5. 브랜치 이동이 안 되는 경우

수정한 내용을 커밋하지 않고 브랜치를 이동하면 다음과 같은 오류가 발생할 수 있습니다.

```text
Your local changes would be overwritten by checkout
```

이때는 변경사항을 먼저 커밋합니다.

```powershell
git add .
git commit -m "작업 중인 변경사항 저장"
git switch main
```

아직 커밋하고 싶지 않다면 임시 보관할 수 있습니다.

```powershell
git stash
git switch main
```

다시 가져오려면:

```powershell
git stash pop
```

## 6. 병합 충돌이 발생할 때

두 브랜치에서 같은 부분을 서로 다르게 수정하면 충돌이 발생합니다.

```text
CONFLICT (content): Merge conflict in prompt_manager.py
```

VS Code에서 충돌 파일을 열고 원하는 내용을 선택합니다.

- Accept Current Change: 현재 브랜치 내용 유지
    
- Accept Incoming Change: 합쳐오는 브랜치 내용 유지
    
- Accept Both Changes: 두 내용 모두 유지
    

수정한 후:

```powershell
git add prompt_manager.py
git commit -m "브랜치 병합 충돌 해결"
```

## 핵심 정리

|기능|명령|의미|
|---|---|---|
|브랜치 이동|`git checkout main`|기존 방식|
|브랜치 이동|`git switch main`|권장 방식|
|브랜치 생성·이동|`git switch -c feature/test`|새 작업 공간 생성|
|브랜치 병합|`git merge feature/test`|기능을 현재 브랜치에 합침|
|브랜치 삭제|`git branch -d feature/test`|완료된 브랜치 정리|

가장 중요한 병합 명령은 다음 순서입니다.

```powershell
git switch main
git merge feature/edit-delete
git push origin main
```