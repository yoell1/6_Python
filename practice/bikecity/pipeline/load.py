import os
import time
import logging
from decimal import Decimal

import oracledb
import pandas as pd
from dotenv import load_dotenv

# 6_Python/10_database/.env  (pipeline → bikecity → practice → 6_Python)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
load_dotenv(os.path.join(ROOT, "10_database", ".env"))   # 접속 정보는 .env 에서만

logger = logging.getLogger("bikecity")   # 설정은 pipeline.py 에서

COLS = ["rental_id", "bike_id", "user_id", "rent_time", "return_time", "duration_min",
        "distance_km", "fee", "payment_method", "bike_type", "station_id", "station_name", "district"]
KEY = "rental_id"
CHUNK_SIZE = 2000

DDL = """
CREATE TABLE rental_log (
    rental_id       VARCHAR2(10)        NOT NULL,
    bike_id         VARCHAR2(10)        NOT NULL,
    user_id         VARCHAR2(10)        NOT NULL,
    rent_time       DATE                NOT NULL,
    return_time     DATE                NOT NULL,
    duration_min    NUMBER(5)           NOT NULL,
    distance_km     NUMBER(5,1)         NOT NULL,
    fee             NUMBER(8)           NOT NULL,
    payment_method  VARCHAR2(20)        NOT NULL,
    bike_type       VARCHAR2(10 CHAR)   NOT NULL,
    station_id      VARCHAR2(10),
    station_name    VARCHAR2(100 CHAR),
    district        VARCHAR2(30 CHAR),
    CONSTRAINT pk_rental_log PRIMARY KEY (rental_id)
)"""

_others = [c for c in COLS if c != KEY]
UPSERT = f"""
MERGE INTO rental_log dst
USING (SELECT {", ".join(f":{i+1} AS {c}" for i, c in enumerate(COLS))} FROM dual) src
ON (dst.{KEY} = src.{KEY})
WHEN MATCHED THEN
    UPDATE SET {", ".join(f"dst.{c} = src.{c}" for c in _others)}
    WHERE {" OR ".join(f"DECODE(dst.{c}, src.{c}, 0, 1) = 1" for c in _others)}
WHEN NOT MATCHED THEN
    INSERT ({", ".join(COLS)})
    VALUES ({", ".join("src." + c for c in COLS)})
"""


def connect():
    return oracledb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dsn=f'{os.getenv("DB_HOST", "127.0.0.1")}:{os.getenv("DB_PORT", "1521")}/{os.getenv("DB_NAME")}',
    )


def create_table(conn):
    """rental_log 생성 (이미 있으면 그대로 사용)"""
    with conn.cursor() as cur:
        try:
            cur.execute(DDL)
            logger.info("rental_log 테이블 생성")
        except oracledb.DatabaseError as e:
            if "ORA-00955" in str(e):
                logger.info("rental_log 테이블이 이미 있음 → 그대로 사용")
            else:
                raise


def prepare_rows(df: pd.DataFrame):
    """DataFrame → list[tuple]. DB 타입에 맞추고 NaN → None"""
    data = df[COLS].copy()
    data["duration_min"] = data["duration_min"].round().astype(int)
    data["fee"] = data["fee"].round().astype(int)
    data = data.astype(object).where(data.notna(), None)
    data["distance_km"] = [Decimal(str(round(v, 1))) for v in data["distance_km"]]
    return [tuple(v.to_pydatetime() if isinstance(v, pd.Timestamp) else v for v in r)
            for r in data.itertuples(index=False)]


def row_count(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM rental_log")
        return cur.fetchone()[0]


def load(df: pd.DataFrame, run_no: int = 1):
    """청크 단위 UPSERT. (신규, 갱신, 최종 행 수) 반환"""
    rows = prepare_rows(df)
    conn = connect()
    try:
        create_table(conn)
        before = row_count(conn)
        affected = 0
        start = time.perf_counter()

        for i in range(0, len(rows), CHUNK_SIZE):
            part = rows[i:i + CHUNK_SIZE]
            with conn.cursor() as cur:
                cur.executemany(UPSERT, part)
                affected += cur.rowcount
            conn.commit()                                 # 청크 단위 커밋
            logger.info(f"  [{run_no}회차] 청크 {i:>5} ~ {i + len(part) - 1:>5} 커밋")

        after = row_count(conn)
    except Exception:
        conn.rollback()
        logger.exception(f"[{run_no}회차] 적재 실패")
        raise
    finally:
        conn.close()

    inserted = after - before
    updated = affected - inserted
    logger.info(f"[{run_no}회차] 신규 {inserted}건 / 갱신 {updated}건 / 최종 {after}행 "
                f"({time.perf_counter() - start:.1f}초)")
    return inserted, updated, after