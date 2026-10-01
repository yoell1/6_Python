"""
    Load. 데이터를 DB에 적재(저장)

    - 하지않는것: 정제(가공)
    - UPSERT를 사용하여 데이터가 있으면 UPDATE, 없으면 INSERT.
    - 대용량을 한 번에 처리하지 않고, CHUNK_SIZE 단위로 나누어서 처리함.
"""

import time

from config import connect,CHUNK_SIZE

# DB에 저장할 컬럼 순서
COLS = ["code","date","open","high","low","close","volume","change","changeRate"]

def _quote(c):
    """
        컬럼명을 큰따옴표로 감싸서 반환
        - date, change, changeRate 
    """
    return f'"{c}"' if c in ("date","change","changeRate") else c