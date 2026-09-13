from models import DuplicateIsbnError, BookNotFoundError


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        for b in self.books:
            if b.isbn == book.isbn:
                raise DuplicateIsbnError(book.isbn)
        self.books.append(book)

    def get_all(self):
        return self.books

    def get_available(self):
        return [book for book in self.books if not book.is_borrowed] 

    def get_authors(self):
        return sorted({book.author for book in self.books})       

    def remove_book(self, isbn):
        book = self._find(isbn)
        self.books.remove(book)
        return book

    def borrow_book(self, isbn):
        book = self._find(isbn)
        book.borrow()
        return book   

    def return_book(self, isbn):
        book = self._find(isbn)
        book.return_book()
        return book    

    def _find(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        raise BookNotFoundError(isbn)