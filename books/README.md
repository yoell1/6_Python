# 도서 관리 CLI

콘솔에서 도서를 등록·조회·대출·반납·삭제하는 프로그램입니다.

## 실행

```
cd books
python main.py
```

## 기능

| 메뉴 | 기능 |
|---|---|
| 1 | 도서 등록 (일반 도서 / 전자책) |
| 2 | 전체 도서 목록 (ISBN, 제목, 저자, 대출여부) |
| 3 | 대출 가능한 도서만 조회 |
| 4 | 등록된 저자 목록 (중복 없이) |
| 5 | 대출 |
| 6 | 반납 |
| 7 | ISBN 으로 삭제 |
| 0 | 종료 |

## 구조

```
books/
  models.py    # Book, EBook, PaperBook, 예외 클래스
  library.py   # Library — 도서 목록 관리 (등록·조회·대출·반납·삭제)
  main.py      # 메뉴 루프 진입점
```

- `Book` : ISBN, 제목, 저자, 대출여부. 대출 상태는 `borrow()` / `return_book()` 으로만 변경 (`_is_borrowed` + 읽기 전용 `@property`)
- `PaperBook(Book)` : 보관 위치 추가
- `EBook(Book)` : 파일 포맷, 파일 용량(MB) 추가

## 예외

| 예외 | 발생 시점 |
|---|---|
| `DuplicateIsbnError` | 이미 등록된 ISBN 으로 등록 시 |
| `BookNotFoundError` | 존재하지 않는 ISBN 으로 대출·반납·삭제 시 |
| `AlreadyBorrowedError` | 이미 대출 중인 도서를 대출 시 |
| `NotBorrowedError` | 대출 중이 아닌 도서를 반납 시 |

## 입력 검증

- ISBN, 제목, 저자는 빈칸 불가 (앞뒤 공백 제거 후 검사)
- 전자책 여부는 `y` / `n` 만 허용
- 용량은 숫자만 허용 (`ValueError` 처리)

## 역할 분담

**직접 작성**
- 초기 버전 전체: `Book` / `EBook` / `PaperBook` 클래스, 예외 클래스 2개(`DuplicateIsbnError`, `BookNotFoundError`), 등록·전체조회·삭제 기능, 메뉴 루프
- 한 파일(`books.py`)로 만든 뒤 `models.py` / `book_manager.py` / `main.py` 세 파일로 분리
- 테스트 중 발견한 버그 수정: 전자책 여부에 `y`/`n` 외 값이 통과되던 문제, 빈칸 입력이 통과되던 문제, 삭제 시 ISBN 공백 미처리

**AI(Claude) 작성 — 요구사항 확정 후 추가된 부분**
- 대출여부 필드와 `borrow()` / `return_book()` 메소드, `AlreadyBorrowedError` / `NotBorrowedError`
- `Library._find()` 로 ISBN 검색 공통화, `get_available()` / `get_authors()` (컴프리헨션)
- `main.py` 의 대출·반납·대출가능 조회·저자 목록 메뉴
- 파일명 `book_manager.py` → `library.py` 변경은 교안 구조에 맞춰 직접 수행

AI 가 작성한 부분은 직접 실행하며 등록 → 대출 → 재대출(거부) → 반납 → 삭제 순서로 테스트했습니다.
