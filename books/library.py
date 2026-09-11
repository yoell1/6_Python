from models import DuplicateIsbnError, BookNotFoundError


class Library:
    def __init__(self):
        self.books = []

    def _find(self, isbn):
        """ ISBN 으로 책을 찾아서 반환. 없으면 예외 """
        for book in self.books:
            if book.isbn == isbn:
                return book
        raise BookNotFoundError(isbn)

    def add_book(self, book):
        for b in self.books:
            if b.isbn == book.isbn:
                raise DuplicateIsbnError(book.isbn)
        self.books.append(book)

    def get_all(self):
        return self.books

    def get_available(self):
        """ 대출 가능한 책만 """
        return [book for book in self.books if not book.is_borrowed]

    def get_authors(self):
        """ 저자 목록 (중복 없이) """
        return sorted({book.author for book in self.books})

    def borrow_book(self, isbn):
        book = self._find(isbn)
        book.borrow()
        return book

    def return_book(self, isbn):
        book = self._find(isbn)
        book.return_book()
        return book

    def remove_book(self, isbn):
        book = self._find(isbn)
        self.books.remove(book)
        return book
