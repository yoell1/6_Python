"""
    고객 관리 CLI 프로그램 (진입점)
"""

from crm_manager import CRMManager
from models import (
    DuplicateContactError,
    CustomerNotFoundError,
    InvalidContactError,
    InvalidNameError,
    InvalidAmountError,
    EmptyInputError,
)
from input_utils import (
    CancelInput,
    ask,
    ask_int,
    check_yn,
    normalize_contact,
)

MENU = """
============================================================
  고객 관리 프로그램
============================================================
  1. 고객 등록
  2. 전체 고객 조회
  3. VIP 고객 조회
  4. 포인트로 검색
  5. 연락처 수정
  6. 포인트 적립
  7. 고객 삭제
  0. 종료
------------------------------------------------------------
  * 입력 중 q 를 치면 메뉴로 돌아갑니다."""


def print_list(customers):
    """ 고객 목록을 출력하는 함수 """
    if not customers:
        print("---> 조회된 고객이 없습니다.")
        return

    for c in customers:
        print(f"  {c}")
    print(f"---> 총 {len(customers)}명")




def ask_contact(crm, prompt):
    """ 연락처를 입력받아 보정(하이픈 자동 삽입)·검증 후 반환 """
    value = ask(prompt, lambda v: crm.validate_contact(normalize_contact(v)))
    return normalize_contact(value)


def ask_id(crm):
    """
    고객 ID 를 입력받아 존재하는 고객 객체를 반환.
    소문자로 쳐도 대문자로 바꿔서 찾고, 없으면 다시 물어봄
    """
    customer_id = ask("고객 ID : ", lambda v: crm.exists(v.upper()))
    return crm.exists(customer_id.upper())


# ============================================================
# 메뉴별 함수 — 각 메뉴가 하는 일을 하나의 함수로
# ============================================================
def menu_register(crm):
    """ 1. 고객 등록 """
    name = ask("이름 (한글/영문, 20자 이내) : ", crm.validate_name)
    contact = ask_contact(crm, "연락처 (010-0000-0000) : ")
    is_vip = ask("VIP 인가요? (y/n) : ", check_yn).lower() == "y"

    manager = ""
    if is_vip:
        manager = ask("전담 매니저 (한글/영문, 20자 이내) : ", crm.validate_manager)

    customer = crm.add_customer(name, contact, is_vip, manager)
    print(f"---> 등록 완료! 부여된 고객 ID: {customer.customer_id}")
    print(f"     {customer}")


def menu_list_all(crm):
    """ 2. 전체 고객 조회 """
    print_list(crm.get_all())


def menu_list_vip(crm):
    """ 3. VIP 고객 조회 """
    print_list(crm.get_vips())


def menu_search_point(crm):
    """ 4. 포인트로 검색 """
    min_point = ask_int("최소 포인트 (0 이상) : ", min_value=0)
    print_list(crm.search_by_point(min_point))


def menu_update_contact(crm):
    """ 5. 연락처 수정 """
    customer = ask_id(crm)
    new_contact = ask_contact(crm, "새 연락처 (010-0000-0000) : ")

    customer = crm.update_contact(customer.customer_id, new_contact)
    print(f"---> 수정 완료: {customer}")


def menu_earn_point(crm):
    """ 6. 포인트 적립 """
    customer = ask_id(crm)
    amount = ask_int("구매 금액 (1원 이상) : ", min_value=1)

    customer, earned = crm.earn_point(customer.customer_id, amount)
    if earned == 0:
        print(f"---> 금액이 적어 적립된 포인트가 없습니다. 현재 {customer.point:,}P")
    else:
        print(f"---> {earned:,}P 적립! 현재 {customer.point:,}P "
              f"({customer.grade} {int(customer.RATE * 100)}%)")


def menu_remove(crm):
    """ 7. 고객 삭제 """
    customer = ask_id(crm)

    answer = ask(f"'{customer.name}' 님을 삭제할까요? (y/n) : ", check_yn).lower()
    if answer != "y":
        print("---> 삭제를 취소했습니다.")
        return

    crm.remove_customer(customer.customer_id)
    print(f"---> 삭제 완료: {customer.name}")


# 메뉴 번호 → (제목, 실행할 함수)  (딕셔너리로 매핑)
MENU_ACTIONS = {
    "1": ("고객 등록", menu_register),
    "2": ("전체 고객 조회", menu_list_all),
    "3": ("VIP 고객 조회", menu_list_vip),
    "4": ("포인트로 검색", menu_search_point),
    "5": ("연락처 수정", menu_update_contact),
    "6": ("포인트 적립", menu_earn_point),
    "7": ("고객 삭제", menu_remove),
}


# ============================================================
# 진입점
# ============================================================
def main():
    crm = CRMManager()

    while True:
        print(MENU)
        choice = input("메뉴 선택 : ").strip()

        if choice == "0":
            print("프로그램을 종료합니다.")
            break

        entry = MENU_ACTIONS.get(choice)
        if entry is None:
            print("---> 잘못된 메뉴입니다. 0~7 중에서 선택하세요.")
            continue

        title, action = entry                 # 튜플 언패킹
        print(f"\n[{title}]")

        try:
            action(crm)                       # 선택한 메뉴 함수 실행

        # 자식(구체적) 예외 먼저, 부모(넓은) 예외 나중
        except CancelInput:
            print("---> 취소하고 메뉴로 돌아갑니다.")
        except DuplicateContactError as e:
            print(f"[등록 실패] {e}")
        except CustomerNotFoundError as e:
            print(f"[조회 실패] {e}")
        except (InvalidContactError, InvalidNameError, InvalidAmountError, EmptyInputError) as e:
            print(f"[입력 오류] {e}")
        except ValueError as e:
            print(f"[입력 오류] {e}")
        except EOFError:
            raise                             # 바깥에서 종료 처리
        except Exception as e:
            print(f"[알 수 없는 오류] {e}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 종료합니다.")
