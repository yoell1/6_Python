-- BikeCity 대여 기록 적재 테이블 (Oracle)
-- 설계 기준
--   * 금액·거리: NUMBER (FLOAT 사용 안 함 → 소수점 오차 방지)
--   * 날짜·시각: DATE (문자열로 저장하지 않음)
--   * ID: VARCHAR2 (계산하지 않는 값)
--   * rental_id: PRIMARY KEY (= 유니크 제약) → 재실행 안전성의 출발점
--   * 한글 컬럼은 CHAR 단위 길이 (UTF-8에서 한글 1자 = 3바이트)

CREATE TABLE rental_log (
    rental_id       VARCHAR2(10)        NOT NULL,
    bike_id         VARCHAR2(10)        NOT NULL,
    user_id         VARCHAR2(10)        NOT NULL,
    rent_time       DATE                NOT NULL,
    return_time     DATE                NOT NULL,
    duration_min    NUMBER(5)           NOT NULL,   -- 대여 시간(분)
    distance_km     NUMBER(5,1)         NOT NULL,   -- 이동 거리(km), 소수 1자리
    fee             NUMBER(8)           NOT NULL,   -- 요금(원)
    payment_method  VARCHAR2(20)        NOT NULL,   -- APP / CARD / MEMBERSHIP
    bike_type       VARCHAR2(10 CHAR)   NOT NULL,   -- 일반 / 전동
    station_id      VARCHAR2(10),                   -- B043 은 원본에 대여소 정보 없음 → NULL 허용
    station_name    VARCHAR2(100 CHAR),
    district        VARCHAR2(30 CHAR),
    CONSTRAINT pk_rental_log PRIMARY KEY (rental_id)
);

-- UPSERT (MySQL 의 ON DUPLICATE KEY UPDATE 에 해당하는 Oracle 문법)
-- MERGE INTO rental_log dst
-- USING (SELECT :1 AS rental_id, ... FROM dual) src
-- ON (dst.rental_id = src.rental_id)
-- WHEN MATCHED THEN UPDATE SET ...  WHERE (값이 바뀐 경우만)
-- WHEN NOT MATCHED THEN INSERT (...) VALUES (...);
