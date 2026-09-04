"""콘솔 기반 프롬프트 관리 프로그램.

프롬프트와 즐겨찾기 상태는 프로그램 폴더의 prompts.json에 저장된다.
"""

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Prompt:
    """프롬프트 한 건의 정보를 표현한다."""

    prompt_id: int
    title: str
    category: str
    content: str
    favorite: bool = False


class PromptManager:
    """프롬프트 등록, 조회, 수정, 삭제, 검색, 즐겨찾기를 관리한다."""

    DATA_FILE = Path(__file__).with_name("prompts.json")

    @staticmethod
    def default_prompts() -> list[Prompt]:
        return [
            Prompt(
                1,
                "회의자료 핵심 요약",
                "문서작성",
                "다음 회의자료를 핵심 내용, 결정사항, 후속 조치로 구분하여 "
                "5줄 이내로 요약해 주세요.",
            ),
            Prompt(
                2,
                "행사 참석 안내문 작성",
                "행사운영",
                "다음 행사 정보를 바탕으로 목적, 일시, 장소, 주요 내용, "
                "참가 방법이 포함된 정중한 참석 안내문을 작성해 주세요.",
            ),
            Prompt(
                3,
                "제조 데이터 이상 원인 분석",
                "제조AI",
                "다음 설비 데이터와 알람 이력을 분석하여 가능한 이상 원인, "
                "확인 항목, 권장 조치를 우선순위 순으로 제시해 주세요.",
                True,
            ),
        ]

    def __init__(self) -> None:
        self.prompts = self.load_prompts()
        self.next_id = max(
            (prompt.prompt_id for prompt in self.prompts), default=0
        ) + 1

    @classmethod
    def load_prompts(cls) -> list[Prompt]:
        try:
            with cls.DATA_FILE.open(encoding="utf-8") as file:
                data = json.load(file)
            prompts = [
                Prompt(
                    prompt_id=item["prompt_id"],
                    title=item["title"],
                    category=item["category"],
                    content=item["content"],
                    favorite=item.get("favorite", False),
                )
                for item in data
            ]
            cls.validate_prompts(prompts, data)
            return prompts
        except (OSError, json.JSONDecodeError, TypeError, KeyError, ValueError):
            prompts = cls.default_prompts()
            cls.save_prompts(prompts)
            return prompts

    @staticmethod
    def validate_prompts(
        prompts: list[Prompt], data: object
    ) -> None:
        if not isinstance(data, list):
            raise ValueError("프롬프트 데이터는 목록이어야 합니다.")
        if len({prompt.prompt_id for prompt in prompts}) != len(prompts):
            raise ValueError("프롬프트 ID가 중복되었습니다.")
        for prompt, item in zip(prompts, data):
            if (
                not isinstance(item, dict)
                or type(prompt.prompt_id) is not int
                or prompt.prompt_id < 1
                or not all(
                    isinstance(value, str) and value.strip()
                    for value in (prompt.title, prompt.category, prompt.content)
                )
                or type(prompt.favorite) is not bool
            ):
                raise ValueError("프롬프트 데이터 형식이 올바르지 않습니다.")

    @classmethod
    def save_prompts(cls, prompts: list[Prompt]) -> None:
        with cls.DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(
                [asdict(prompt) for prompt in prompts],
                file,
                ensure_ascii=False,
                indent=2,
            )

    @staticmethod
    def read_nonempty(label: str) -> str:
        """공백이 아닌 문자열을 입력받는다."""
        while True:
            value = input(label).strip()
            if value:
                return value
            print("빈 내용은 입력할 수 없습니다.")

    def find_by_id(self, prompt_id: int) -> Prompt | None:
        return next(
            (prompt for prompt in self.prompts if prompt.prompt_id == prompt_id),
            None,
        )

    @staticmethod
    def print_summary(prompt: Prompt) -> None:
        favorite_mark = "★" if prompt.favorite else "☆"
        print(
            f"{prompt.prompt_id:>3} | {favorite_mark} | "
            f"{prompt.category:<10} | {prompt.title}"
        )

    def print_prompt_list(self, prompts: list[Prompt]) -> None:
        if not prompts:
            print("조회된 프롬프트가 없습니다.")
            return

        print("\n ID | 즐겨찾기 | 카테고리   | 제목")
        print("-" * 60)
        for prompt in prompts:
            self.print_summary(prompt)
        print(f"\n총 {len(prompts)}개")

    def add_prompt(self) -> None:
        print("\n[프롬프트 추가]")
        title = self.read_nonempty("제목: ")
        category = self.read_nonempty("카테고리: ")
        content = self.read_nonempty("프롬프트 내용: ")

        self.prompts.append(
            Prompt(self.next_id, title, category, content)
        )
        self.save_prompts(self.prompts)
        print(f"프롬프트가 등록되었습니다. (ID: {self.next_id})")
        self.next_id += 1

    def edit_prompt(self) -> None:
        print("\n[프롬프트 수정]")
        prompt_id = self.read_prompt_id()
        if prompt_id is None:
            return

        prompt = self.find_by_id(prompt_id)
        if prompt is None:
            print("해당 ID의 프롬프트가 없습니다.")
            return

        title = input(f"제목 [{prompt.title}]: ").strip()
        category = input(f"카테고리 [{prompt.category}]: ").strip()
        content = input(f"프롬프트 내용 [{prompt.content}]: ").strip()

        if title:
            prompt.title = title
        if category:
            prompt.category = category
        if content:
            prompt.content = content

        self.save_prompts(self.prompts)
        print(f"'{prompt.title}' 프롬프트가 수정되었습니다.")

    def delete_prompt(self) -> None:
        print("\n[프롬프트 삭제]")
        prompt_id = self.read_prompt_id()
        if prompt_id is None:
            return

        prompt = self.find_by_id(prompt_id)
        if prompt is None:
            print("해당 ID의 프롬프트가 없습니다.")
            return

        while True:
            answer = input(f"'{prompt.title}' 프롬프트를 삭제할까요? (Y/N): ").strip().lower()
            if answer in {"y", "n"}:
                break
            print("Y 또는 N으로 입력해 주세요.")

        if answer == "n":
            print("삭제를 취소했습니다.")
            return

        self.prompts.remove(prompt)
        self.save_prompts(self.prompts)
        print(f"'{prompt.title}' 프롬프트가 삭제되었습니다.")

    def show_list(self) -> None:
        print("\n[전체 프롬프트 목록]")
        self.print_prompt_list(self.prompts)

    def show_by_category(self) -> None:
        print("\n[카테고리별 조회]")
        categories = sorted({prompt.category for prompt in self.prompts})
        for index, category in enumerate(categories, start=1):
            count = sum(p.category == category for p in self.prompts)
            print(f"{index}. {category} ({count}개)")

        category = input("조회할 카테고리명 또는 번호: ").strip()
        if category.isdigit():
            index = int(category) - 1
            if not 0 <= index < len(categories):
                print("존재하지 않는 카테고리 번호입니다.")
                return
            category = categories[index]

        results = [
            prompt
            for prompt in self.prompts
            if prompt.category.casefold() == category.casefold()
        ]
        self.print_prompt_list(results)

    def search_prompt(self) -> None:
        print("\n[프롬프트 검색]")
        keyword = self.read_nonempty("검색어: ").casefold()
        results = [
            prompt
            for prompt in self.prompts
            if keyword in prompt.title.casefold()
            or keyword in prompt.category.casefold()
            or keyword in prompt.content.casefold()
        ]
        self.print_prompt_list(results)

    def read_prompt_id(self) -> int | None:
        value = input("프롬프트 ID: ").strip()
        if not value.isdigit():
            print("ID는 숫자로 입력해 주세요.")
            return None
        return int(value)

    def show_detail(self) -> None:
        print("\n[프롬프트 상세 보기]")
        prompt_id = self.read_prompt_id()
        if prompt_id is None:
            return

        prompt = self.find_by_id(prompt_id)
        if prompt is None:
            print("해당 ID의 프롬프트가 없습니다.")
            return

        print("-" * 60)
        print(f"ID       : {prompt.prompt_id}")
        print(f"제목     : {prompt.title}")
        print(f"카테고리 : {prompt.category}")
        print(f"즐겨찾기 : {'등록됨 ★' if prompt.favorite else '등록 안 됨 ☆'}")
        print(f"내용     : {prompt.content}")
        print("-" * 60)

    def toggle_favorite(self) -> None:
        print("\n[즐겨찾기 등록/해제]")
        prompt_id = self.read_prompt_id()
        if prompt_id is None:
            return

        prompt = self.find_by_id(prompt_id)
        if prompt is None:
            print("해당 ID의 프롬프트가 없습니다.")
            return

        prompt.favorite = not prompt.favorite
        self.save_prompts(self.prompts)
        state = "등록" if prompt.favorite else "해제"
        print(f"'{prompt.title}' 프롬프트의 즐겨찾기가 {state}되었습니다.")

    def show_favorites(self) -> None:
        print("\n[즐겨찾기 목록]")
        favorites = [prompt for prompt in self.prompts if prompt.favorite]
        self.print_prompt_list(favorites)

    @staticmethod
    def show_menu() -> None:
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
0. 종료
============================================================"""
        )

    def get_action(self, choice: str):
        actions = {
            "1": self.add_prompt,
            "2": self.show_list,
            "3": self.show_by_category,
            "4": self.search_prompt,
            "5": self.show_detail,
            "6": self.toggle_favorite,
            "7": self.show_favorites,
            "8": self.edit_prompt,
            "9": self.delete_prompt,
        }
        return actions.get(choice)

    def run(self) -> None:
        while True:
            self.show_menu()
            choice = input("메뉴 번호를 선택하세요: ").strip()

            if choice == "0":
                print("프로그램을 종료합니다. 이용해 주셔서 감사합니다.")
                return

            action = self.get_action(choice)
            if action is None:
                print("0부터 9까지의 메뉴 번호를 입력해 주세요.")
                continue

            action()
            input("\nEnter 키를 누르면 메뉴로 돌아갑니다...")


def main() -> None:
    try:
        PromptManager().run()
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 종료합니다.")


if __name__ == "__main__":
    main()
