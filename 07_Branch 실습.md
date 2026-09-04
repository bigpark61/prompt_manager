
`prompt_manager.py`의 브랜치 실습용 업그레이드는 **프롬프트 수정·삭제 기능 추가**가 가장 적합합니다. 기존 `main`은 그대로 보존하면서 새 브랜치에서 기능을 개발하고, 테스트 후 병합하는 전 과정을 경험할 수 있습니다.

## 1. 추천 업그레이드

### 1차 실습: 수정·삭제 기능

새 메뉴를 추가합니다.

```text
8. 프롬프트 수정
9. 프롬프트 삭제
```

기능 내용:

- 프롬프트 ID로 수정 대상 선택
    
- 제목·카테고리·내용 변경
    
- Enter만 누르면 기존 값 유지
    
- 삭제 전 `Y/N` 확인
    
- 존재하지 않는 ID 입력 예외 처리
    

추천 브랜치명:

```text
feature/edit-delete
```

### 2차 실습: JSON 영구 저장

프로그램을 종료해도 추가한 프롬프트와 즐겨찾기 상태가 유지되도록 합니다.

추천 브랜치명:

```text
feature/json-storage
```

처음에는 수정·삭제 기능으로 브랜치를 연습한 뒤, 두 번째로 JSON 저장 기능을 개발하는 것이 이해하기 쉽습니다.

---

# 2. 브랜치 개념

브랜치는 기존 프로그램을 건드리지 않고 별도의 작업 공간에서 기능을 개발하는 방법입니다.

```text
main
 └─ 현재 정상 작동하는 prompt_manager.py

feature/edit-delete
 └─ 수정·삭제 기능을 개발하는 버전
```

`feature/edit-delete`에서 오류가 발생해도 `main`의 프로그램은 영향을 받지 않습니다.

개발이 완료되면 다음과 같이 합칩니다.

```text
main
  └─ feature/edit-delete 병합
       └─ 수정·삭제 기능이 포함된 새로운 main
```

---

# 3. 사전 확인

VS Code에서 프로젝트 폴더를 열고 터미널을 실행합니다.

```text
Terminal → New Terminal
```

현재 Git 상태를 확인합니다.

```powershell
git status
```

다음처럼 나오면 가장 좋습니다.

```text
On branch main
nothing to commit, working tree clean
```

현재 브랜치도 확인합니다.

```powershell
git branch
```

결과:

```text
* main
```

별표 `*`는 현재 작업 중인 브랜치를 뜻합니다.

수정 중인 파일이 있다면 먼저 커밋합니다.

```powershell
git add .
git commit -m "프롬프트 관리 프로그램 기본 버전 완성"
git push origin main
```

---

# 4. 기능 개발 브랜치 생성

다음 명령을 실행합니다.

```powershell
git switch -c feature/edit-delete
```

이 명령은 두 가지 작업을 동시에 수행합니다.

1. `feature/edit-delete` 브랜치 생성
    
2. 생성한 브랜치로 이동
    

확인합니다.

```powershell
git branch
```

결과:

```text
* feature/edit-delete
  main
```

VS Code 왼쪽 아래에도 현재 브랜치명이 표시됩니다.

```text
feature/edit-delete
```

---

# 5. 프로그램 업그레이드

## 5.1 메뉴에 기능 추가

`print_menu()`의 메뉴에 다음 두 줄을 추가합니다.

```python
8. 프롬프트 수정
9. 프롬프트 삭제
```

수정된 부분은 다음과 같습니다.

```python
@staticmethod
def print_menu() -> None:
    print(
        """
============================================================
                 프롬프트 관리 프로그램
============================================================
1. 프롬프트 추가
2. 전체 목록 보기
3. 카테고리별 조회
4. 프롬프트 검색
5. 상세 보기
6. 즐겨찾기 등록/해제
7. 즐겨찾기 목록 보기
8. 프롬프트 수정
9. 프롬프트 삭제
10. 종료
============================================================"""
    )
```

## 5.2 수정 기능 추가

`PromptManager` 클래스 안에 다음 메서드를 추가합니다.

```python
def edit_prompt(self) -> None:
    print("\n[프롬프트 수정]")
    prompt_id = self.read_prompt_id()

    if prompt_id is None:
        return

    prompt = self.find_by_id(prompt_id)

    if prompt is None:
        print("해당 ID의 프롬프트가 없습니다.")
        return

    print("변경하지 않을 항목은 Enter 키를 누르세요.")

    title = input(f"제목 [{prompt.title}]: ").strip()
    category = input(f"카테고리 [{prompt.category}]: ").strip()
    content = input(f"내용 [{prompt.content}]: ").strip()

    if title:
        prompt.title = title

    if category:
        prompt.category = category

    if content:
        prompt.content = content

    print("프롬프트가 수정되었습니다.")
```

예를 들어 제목만 입력하고 나머지는 Enter를 누르면 제목만 변경됩니다.

## 5.3 삭제 기능 추가

같은 클래스 안에 다음 메서드를 추가합니다.

```python
def delete_prompt(self) -> None:
    print("\n[프롬프트 삭제]")
    prompt_id = self.read_prompt_id()

    if prompt_id is None:
        return

    prompt = self.find_by_id(prompt_id)

    if prompt is None:
        print("해당 ID의 프롬프트가 없습니다.")
        return

    print(f"제목: {prompt.title}")
    confirm = input("정말 삭제하시겠습니까? (Y/N): ").strip().lower()

    if confirm == "y":
        self.prompts.remove(prompt)
        print("프롬프트가 삭제되었습니다.")
    else:
        print("삭제가 취소되었습니다.")
```

## 5.4 메뉴 번호와 메서드 연결

`run()` 메서드의 `actions`에 다음 두 항목을 추가합니다.

```python
actions = {
    "1": self.add_prompt,
    "2": self.show_all,
    "3": self.show_by_category,
    "4": self.search_prompts,
    "5": self.show_detail,
    "6": self.toggle_favorite,
    "7": self.show_favorites,
    "8": self.edit_prompt,
    "9": self.delete_prompt,
}
```

잘못된 번호 안내도 수정합니다.

기존:

```python
print("0부터 7까지의 메뉴 번호를 입력해 주세요.")
```

변경:

```python
print("0부터 9까지의 메뉴 번호를 입력해 주세요.")
```

---

# 6. 기능 테스트

프로그램을 실행합니다.

```powershell
python prompt_manager.py
```

가상환경이 활성화되어 있다면 터미널 앞에 `(.venv)`가 표시됩니다.

```text
(.venv) PS C:\...\prompt_manager>
```

## 수정 기능 테스트

1. `2`를 입력해 목록 확인
    
2. `8`을 입력
    
3. 수정할 프롬프트 ID 입력
    
4. 제목 또는 내용 수정
    
5. 다시 `2`를 입력해 변경 확인
    
6. `5` 상세 보기에서 변경 확인
    

## 삭제 기능 테스트

1. 먼저 `1`로 테스트 프롬프트 추가
    
2. `9`를 입력
    
3. 추가한 프롬프트 ID 입력
    
4. `Y` 입력
    
5. `2`를 입력해 삭제 여부 확인
    

기본 프롬프트를 바로 삭제하기보다 테스트용 프롬프트를 추가한 후 삭제하는 것이 좋습니다.

---

# 7. 변경 내용 확인

새 터미널을 열지 않고 현재 터미널에서 실행합니다.

```powershell
git status
```

결과 예시:

```text
On branch feature/edit-delete
modified: prompt_manager.py
```

수정된 내용을 확인합니다.

```powershell
git diff
```

VS Code에서는 왼쪽의 `Source Control`을 열고 `prompt_manager.py`를 클릭하면 변경 전후를 비교할 수 있습니다.

---

# 8. 브랜치에서 Commit

수정한 파일을 Stage에 올립니다.

```powershell
git add prompt_manager.py
```

커밋합니다.

```powershell
git commit -m "프롬프트 수정 및 삭제 기능 추가"
```

커밋 이력을 확인합니다.

```powershell
git log --oneline --all --graph
```

예상 형태:

```text
* a12bc34 프롬프트 수정 및 삭제 기능 추가
* 82de541 프롬프트 관리 프로그램 기본 버전 완성
```

---

# 9. GitHub에 새 브랜치 올리기

```powershell
git push -u origin feature/edit-delete
```

여기서:

- `origin`: 연결된 GitHub 저장소
    
- `feature/edit-delete`: 업로드할 브랜치
    
- `-u`: 로컬 브랜치와 GitHub 브랜치를 연결
    

이후 같은 브랜치에서는 다음 명령만 사용해도 됩니다.

```powershell
git push
```

GitHub 저장소의 브랜치 목록을 확인하면 다음 두 브랜치가 보입니다.

```text
main
feature/edit-delete
```

---

# 10. Pull Request 생성

GitHub 저장소에 접속하면 보통 다음 버튼이 표시됩니다.

```text
Compare & pull request
```

선택 후 병합 방향을 확인합니다.

|구분|브랜치|
|---|---|
|Base|`main`|
|Compare|`feature/edit-delete`|

Pull Request 제목:

```text
프롬프트 수정 및 삭제 기능 추가
```

설명 예시:

```markdown
## 변경 내용

- 프롬프트 수정 기능 추가
- 프롬프트 삭제 기능 추가
- 삭제 전 확인 절차 추가
- 잘못된 ID 입력 예외 처리

## 테스트 결과

- 제목 및 내용 수정 정상
- Enter 입력 시 기존 값 유지
- 프롬프트 삭제 정상
- 삭제 취소 정상
```

`Create pull request`를 선택합니다.

---

# 11. main 브랜치에 병합

Pull Request 화면에서 변경 내용을 검토한 후 다음을 선택합니다.

```text
Merge pull request
→ Confirm merge
```

이제 GitHub의 `main` 브랜치에 수정·삭제 기능이 포함됩니다.

하지만 내 컴퓨터의 `main` 브랜치는 아직 이전 버전이므로 최신 코드를 가져와야 합니다.

---

# 12. 로컬 main 최신화

VS Code 터미널에서 실행합니다.

```powershell
git switch main
git pull origin main
```

프로그램을 다시 실행합니다.

```powershell
python prompt_manager.py
```

이제 `main`에서도 8번과 9번 메뉴가 나타나면 성공입니다.

---

# 13. 작업이 끝난 브랜치 삭제

병합이 완료된 로컬 브랜치를 삭제합니다.

```powershell
git branch -d feature/edit-delete
```

GitHub에서 원격 브랜치도 제거하려면:

```powershell
git push origin --delete feature/edit-delete
```

브랜치를 삭제해도 `main`에 병합된 프로그램과 커밋 기록은 삭제되지 않습니다.

---

# 14. 전체 실습 명령 요약

```powershell
# 1. main 최신화
git switch main
git pull origin main

# 2. 기능 브랜치 생성
git switch -c feature/edit-delete

# 3. VS Code에서 코드 수정하고 테스트
python prompt_manager.py

# 4. 변경 확인
git status
git diff

# 5. 커밋
git add prompt_manager.py
git commit -m "프롬프트 수정 및 삭제 기능 추가"

# 6. GitHub에 브랜치 업로드
git push -u origin feature/edit-delete

# 7. GitHub에서 Pull Request 생성·검토·병합

# 8. 로컬 main 최신화
git switch main
git pull origin main

# 9. 완료된 브랜치 삭제
git branch -d feature/edit-delete
git push origin --delete feature/edit-delete
```

이번 실습에서 가장 중요한 흐름은 다음과 같습니다.

```text
main 최신화
→ 기능 브랜치 생성
→ 코드 수정
→ 테스트
→ Commit
→ Push
→ Pull Request
→ main 병합
→ 로컬 main 최신화
```

이 실습을 완료한 다음에는 `feature/json-storage` 브랜치를 새로 만들어 **JSON 영구 저장 기능**을 추가하면 브랜치 활용법을 한 번 더 확실하게 익힐 수 있습니다.