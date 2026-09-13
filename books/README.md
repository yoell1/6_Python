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

- `Book` : ISBN, 제목, 저자, 대출여부. 대출 상태는 `borrow()` / `return_book()` 으로만 변경 (`__is_borrowed` 네임 맹글링 + 읽기 전용 `@property is_borrowed`)
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
- 조회 결과가 비어 있으면 안내문 출력 (전체조회 / 대출가능 조회 / 저자 목록)

## 역할 분담

**직접 작성 (전체 코드)**
- `Book` / `EBook` / `PaperBook` 클래스, `borrow()` / `return_book()`, 읽기 전용 `@property is_borrowed`
- 예외 클래스 4개 (`DuplicateIsbnError`, `BookNotFoundError`, `AlreadyBorrowedError`, `NotBorrowedError`)
- `Library` — `_find()` 공통화, `get_available()` / `get_authors()` 컴프리헨션, 대출·반납·삭제
- `main.py` 메뉴 0~7 전체, 입력 검증 (빈칸·y/n·숫자)
- 한 파일로 만든 뒤 `models.py` / `library.py` / `main.py` 로 분리

**AI(Claude) 의 역할**
- 요구사항을 TODO 목록으로 정리해 작성 순서 안내
- 개념 설명 (`_find` 로 공통 부분 빼기, 컴프리헨션, `except (A, B)`)
- 작성한 코드 검토 — 들여쓰기·오타·빠진 부분 지적, 실행 테스트
- 1차 버전에서 대출/반납 부분을 AI 가 작성했으나, 이후 그 부분을 지우고 요구사항만 보고 직접 다시 작성함 (커밋 이력 참고)

**테스트**
- 등록 → 중복 등록(거부) → 대출 → 재대출(거부) → 대출가능 조회 → 저자 목록 → 반납 → 재반납(거부) → 없는 ISBN 삭제(거부) → 삭제
- 테스트 중 직접 발견한 버그: y/n 외 값 통과, 빈칸 통과, 삭제 시 공백 미처리 → 수정

## 피드백 반영

- 대출 상태 필드 `_is_borrowed` → `__is_borrowed` 로 변경 (캡슐화 의도를 명확히 하라는 피드백). `_` 하나는 "건드리지 말자" 는 약속이고, `__` 두 개는 이름이 `_Book__is_borrowed` 로 바뀌어 바깥에서 직접 접근이 막힘
