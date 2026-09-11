"""
    사용자 입력 도우미

    - 잘못된 값이면 해당 항목만 다시 물어봄
    - 어느 입력 칸에서든 q 를 치면 CancelInput 으로 메뉴 복귀
"""

from models import (
    DuplicateContactError,
    CustomerNotFoundError,
    InvalidContactError,
    InvalidNameError,
    EmptyInputError,
)


class CancelInput(Exception):
    """ 사용자가 q 를 입력해 작업을 취소했을 때 발생 """


def read(prompt):
    """ 입력을 받되, q 를 치면 CancelInput 을 발생시켜 메뉴로 돌아감 """
    text = input(prompt).strip()
    if text.lower() == "q":
        raise CancelInput()
    return text


def ask(prompt, check):
    """
    입력을 받고 check 함수로 검사.
    통과할 때까지 같은 항목만 다시 물어봄 (처음부터 다시 안 쳐도 됨)
    """
    while True:
        value = read(prompt)
        try:
            check(value)
            return value
        except (EmptyInputError, InvalidContactError, InvalidNameError,
                DuplicateContactError, CustomerNotFoundError, ValueError) as e:
            print(f"    [다시 입력] {e}")


def ask_int(prompt, min_value=None):
    """
    숫자 입력을 받되, 숫자가 아니거나 min_value 미만이면 다시 물어봄.
    10,000 처럼 콤마를 넣어도 허용
    """
    while True:
        text = read(prompt).replace(",", "")
        if not text.lstrip("-").isdigit():
            print(f"    [다시 입력] 숫자를 입력해주세요: '{text}'")
            continue
        value = int(text)
        if min_value is not None and value < min_value:
            print(f"    [다시 입력] {min_value:,} 이상이어야 합니다: {value:,}")
            continue
        return value


def check_yn(value):
    """ y 또는 n 만 허용 """
    if value.lower() not in ("y", "n"):
        raise ValueError(f"y 또는 n 을 입력해주세요: '{value}'")


def normalize_contact(text):
    """ 01011112222 처럼 하이픈 없이 입력해도 010-1111-2222 로 바꿔줌 """
    digits = text.replace("-", "").replace(" ", "")
    if len(digits) == 11 and digits.isdigit():
        return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
    return text
