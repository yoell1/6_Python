from models import (
    EBook,
    PaperBook,
    DuplicateIsbnError,
    BookNotFoundError,
    AlreadyBorrowedError,
    NotBorrowedError,
)
from library import Library

MENU = """
1. 등록  2. 전체조회  3. 대출가능 조회  4. 저자 목록
5. 대출  6. 반납  7. 삭제  0. 종료"""


def print_books(books):
    if not books:
        print("조회된 도서가 없습니다")
        return
    for book in books:
        print(book)


def main():
    library = Library()

    while True:
        print(MENU)
        choice = input("선택 : ").strip()

        if choice == "0":
            break

        elif choice == "1":
            isbn = input("ISBN : ").strip()
            title = input("제목 : ").strip()
            author = input("저자 : ").strip()

            if not isbn or not title or not author:
                print("[입력 오류] ISBN, 제목, 저자는 비울 수 없습니다")
                continue

            kind = input("전자책인가요? (y/n) : ").strip().lower()

            try:
                if kind == "y":
                    file_format = input("파일 포맷 (PDF/EPUB) : ").strip()
                    file_size = int(input("용량(MB) : "))
                    book = EBook(isbn, title, author, file_format, file_size)
                elif kind == "n":
                    location = input("보관 위치 : ").strip()
                    book = PaperBook(isbn, title, author, location)
                else:
                    print("[입력 오류] y 또는 n 만 입력하세요")
                    continue
            except ValueError:
                print("[입력 오류] 숫자를 입력하세요")
                continue

            try:
                library.add_book(book)
                print("등록 완료")
            except DuplicateIsbnError as e:
                print(f"[등록 실패] {e}")

        elif choice == "2":
            print_books(library.get_all())

        elif choice == "3":
            print_books(library.get_available())

        elif choice == "4":
            authors = library.get_authors()
            if not authors:
                print("등록된 저자가 없습니다")
            else:
                print(", ".join(authors))

        elif choice == "5":
            isbn = input("대출할 ISBN : ").strip()
            try:
                book = library.borrow_book(isbn)
                print(f"대출 완료: {book.title}")
            except (BookNotFoundError, AlreadyBorrowedError) as e:
                print(f"[대출 실패] {e}")

        elif choice == "6":
            isbn = input("반납할 ISBN : ").strip()
            try:
                book = library.return_book(isbn)
                print(f"반납 완료: {book.title}")
            except (BookNotFoundError, NotBorrowedError) as e:
                print(f"[반납 실패] {e}")

        elif choice == "7":
            isbn = input("삭제할 ISBN : ").strip()
            try:
                book = library.remove_book(isbn)
                print(f"삭제 완료: {book.title}")
            except BookNotFoundError as e:
                print(f"[삭제 실패] {e}")

        else:
            print("잘못된 메뉴")


main()
