class Book:
    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author
        self._is_borrowed = False

    def borrow(self):
        if self._is_borrowed:
            raise AlreadyBorrowedError(self.isbn)
        self._is_borrowed = True

    @property
    def is_borrowed(self):
        return self._is_borrowed

    def return_book(self):
        if not self._is_borrowed:
            raise NotBorrowedError(self.isbn)
        self._is_borrowed = False    

    def __str__(self):
        status = "대출중" if self._is_borrowed else "대출가능"
        return f"[{self.isbn}] {self.title} - {self.author} ({status})"


class EBook(Book):
    def __init__(self, isbn, title, author,file_format ,file_size):
        super().__init__(isbn, title, author)
        self.file_format = file_format
        self.file_size = file_size

    def __str__(self):
        return f"{super().__str__()} | {self.file_format} {self.file_size}MB"


class PaperBook(Book):
    def __init__(self, isbn, title, author, location):
        super().__init__(isbn, title, author)
        self.location = location

    def __str__(self):
        return f"{super().__str__()} | 위치 {self.location}"


class DuplicateIsbnError(Exception):
    def __init__(self, isbn):
        self.isbn = isbn
        super().__init__(f"이미 등록된 ISBN 입니다: {isbn}")


class BookNotFoundError(Exception):
    def __init__(self, isbn):
        self.isbn = isbn
        super().__init__(f"존재하지 않는 ISBN 입니다: {isbn}")

class AlreadyBorrowedError(Exception):
    def __init__(self, isbn):
        self.isbn = isbn
        super().__init__(f"이미 대출 중인 도서입니다. ISBN: {isbn}") 

class NotBorrowedError(Exception):
    def __init__(self, isbn):
        self.isbn = isbn
        super().__init__(f"대출 중이 아닌 도서입니다. ISBN: {isbn}")    