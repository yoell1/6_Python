"""
    고객 목록 관리 클래스 (등록 · 조회 · 수정 · 삭제)
"""

from models import (
    Customer,
    VIPCustomer,
    DuplicateContactError,
    CustomerNotFoundError,
    InvalidContactError,
    InvalidNameError,
    EmptyInputError,
)


class CRMManager:
    NAME_MAX_LENGTH = 20         # 이름·매니저 최대 글자 수

    def __init__(self):
        self.customers = []      # 고객 객체를 담는 리스트
        self._next_id = 1        # 다음에 부여할 고객 번호 (자동 채번)

    # --------------------------------------------------
    # 내부 도우미 (검사 전용)
    # --------------------------------------------------
    def _find_by_id(self, customer_id):
        """ ID로 고객을 찾아 반환. 없으면 예외 """
        for c in self.customers:
            if c.customer_id == customer_id:
                return c
        raise CustomerNotFoundError(customer_id)

    def _check_contact(self, contact):
        """ 연락처가 이미 있으면 예외 """
        for c in self.customers:
            if c.contact == contact:
                raise DuplicateContactError(contact)

    @staticmethod
    def _is_ascii_digits(text, length):
        """ 0~9 만으로 이루어진 length 자리 문자열인지 (전각 숫자 １２３ 는 거부) """
        return len(text) == length and all(ch in "0123456789" for ch in text)

    def _check_contact_format(self, contact):
        """ 연락처 형식 검사: 010-0000-0000 """
        parts = contact.split("-")
        valid = (
            len(parts) == 3
            and parts[0] == "010"
            and self._is_ascii_digits(parts[1], 4)
            and self._is_ascii_digits(parts[2], 4)
        )
        if not valid:
            raise InvalidContactError(contact)

    def _check_name_format(self, name):
        """ 이름은 완성형 한글(가~힣)·영문(과 사이 공백)만 허용. ㅏ, ㄱ 같은 자모는 불가 """
        if len(name) > self.NAME_MAX_LENGTH:
            raise InvalidNameError(name, f"은 {self.NAME_MAX_LENGTH}자 이하여야 합니다")
        for ch in name.replace(" ", ""):
            is_hangul = "가" <= ch <= "힣"
            is_alpha = ("a" <= ch <= "z") or ("A" <= ch <= "Z")
            if not (is_hangul or is_alpha):
                raise InvalidNameError(name)

    def _check_empty(self, value, field):
        """ 빈 문자열이면 예외 """
        if not value.strip():
            raise EmptyInputError(field)

    # --------------------------------------------------
    # 공개 검증 메소드 (main.py 에서 항목별 즉시 검사에 사용)
    # --------------------------------------------------
    def validate_name(self, name):
        """ 이름 검사: 비어있지 않고, 한글·영문만 """
        self._check_empty(name, "이름")
        self._check_name_format(name)

    def validate_contact(self, contact):
        """ 연락처 검사: 비어있지 않고, 형식이 맞고, 중복이 아니어야 함 """
        self._check_empty(contact, "연락처")
        self._check_contact_format(contact)
        self._check_contact(contact)

    def validate_manager(self, manager):
        """ VIP 전담 매니저 검사: 비어있지 않고, 한글·영문만 """
        self._check_empty(manager, "전담 매니저")
        self._check_name_format(manager)

    def exists(self, customer_id):
        """ 고객 ID 존재 여부 확인. 없으면 CustomerNotFoundError """
        return self._find_by_id(customer_id)

    # --------------------------------------------------
    # 등록
    # --------------------------------------------------
    def add_customer(self, name, contact, is_vip=False, manager=""):
        self.validate_name(name)
        self.validate_contact(contact)
        if is_vip:
            self.validate_manager(manager)

        customer_id = f"C{self._next_id:03d}"    # C001, C002, ... 자동 부여
        self._next_id += 1

        if is_vip:
            customer = VIPCustomer(customer_id, name, contact, manager=manager)
        else:
            customer = Customer(customer_id, name, contact)

        self.customers.append(customer)
        return customer

    # --------------------------------------------------
    # 조회
    # --------------------------------------------------
    def get_all(self):
        return self.customers

    def get_vips(self):
        return [c for c in self.customers if isinstance(c, VIPCustomer)]

    def search_by_point(self, min_point):
        """ min_point 이상 보유 고객을 포인트 높은 순으로 반환 """
        found = [c for c in self.customers if c.point >= min_point]
        return sorted(found, key=lambda c: c.point, reverse=True)

    # --------------------------------------------------
    # 수정
    # --------------------------------------------------
    def update_contact(self, customer_id, new_contact):
        customer = self._find_by_id(customer_id)
        self.validate_contact(new_contact)

        customer.contact = new_contact
        return customer

    def earn_point(self, customer_id, amount):
        customer = self._find_by_id(customer_id)
        earned = customer.add_point(amount)
        return customer, earned

    # --------------------------------------------------
    # 삭제
    # --------------------------------------------------
    def remove_customer(self, customer_id):
        customer = self._find_by_id(customer_id)
        self.customers.remove(customer)
        return customer
