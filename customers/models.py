"""
    도메인 클래스 정의

    Customer (부모)  ->  VIPCustomer (자식)
"""


# ------------------------------------------------------------
# 사용자 정의 예외
# ------------------------------------------------------------
class DuplicateContactError(Exception):
    """ 연락처가 이미 등록되어 있을 때 발생 """
    def __init__(self, contact):
        self.contact = contact
        super().__init__(f"이미 등록된 연락처입니다: {contact}")


class CustomerNotFoundError(Exception):
    """ 고객 ID를 찾을 수 없을 때 발생 """
    def __init__(self, customer_id):
        self.customer_id = customer_id
        super().__init__(f"존재하지 않는 고객 ID입니다: {customer_id}")


class InvalidContactError(ValueError):
    """ 연락처 형식이 잘못된 경우 발생 (010-0000-0000) """
    def __init__(self, contact):
        self.contact = contact
        super().__init__(f"연락처 형식이 올바르지 않습니다: {contact} (예: 010-1234-5678)")


class InvalidNameError(ValueError):
    """ 이름 형식이 잘못된 경우 발생 (문자 종류, 길이) """
    def __init__(self, name, reason="은 한글 또는 영문만 가능합니다"):
        self.name = name
        super().__init__(f"이름{reason}: {name}")


class InvalidAmountError(ValueError):
    """ 구매 금액이 잘못된 경우 발생 """


class EmptyInputError(ValueError):
    """ 필수 입력값이 비어 있을 때 발생 """
    def __init__(self, field):
        self.field = field
        super().__init__(f"{field}은(는) 비워둘 수 없습니다.")


# ------------------------------------------------------------
# 고객 클래스
# ------------------------------------------------------------
class Customer:
    """ 일반 고객 """

    RATE = 0.01          # 적립률 1%  (클래스 변수)

    def __init__(self, customer_id, name, contact, point=0):
        self.customer_id = customer_id
        self.name = name
        self.contact = contact
        self.point = point

    def add_point(self, amount):
        """ 구매 금액을 받아 등급별 포인트를 적립하고, 적립된 포인트를 반환 """
        if amount <= 0:
            raise InvalidAmountError("구매 금액은 0보다 커야 합니다.")

        earned = int(amount * self.RATE)
        self.point += earned
        return earned

    @property
    def grade(self):
        return "일반"

    @property
    def masked_contact(self):
        """ 개인정보 보호: 가운데 4자리를 * 로 가림  010-1234-5678 -> 010-****-5678 """
        parts = self.contact.split("-")
        return f"{parts[0]}-****-{parts[2]}"

    def __str__(self):
        return (f"ID: {self.customer_id} | 이름: {self.name} "
                f"| 연락처: {self.masked_contact} | 포인트: {self.point:,}P | 등급: {self.grade}")


class VIPCustomer(Customer):
    """ VIP 고객 — 적립률 5%, 전담 매니저 보유 """

    RATE = 0.05          # 부모의 RATE 를 덮어씀

    def __init__(self, customer_id, name, contact, point=0, manager=""):
        super().__init__(customer_id, name, contact, point)
        self.manager = manager

    @property
    def grade(self):
        return "VIP"

    def __str__(self):
        return f"{super().__str__()} | 담당: {self.manager}"
