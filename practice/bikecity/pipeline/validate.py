import logging
import pandas as pd

logger = logging.getLogger("bikecity")


def validate(df: pd.DataFrame) -> bool:
    """적재 전 검사. 모두 통과하면 True"""
    checks = {
        "rental_id 중복 없음":       df["rental_id"].is_unique,
        "반납 > 대여":               (df["duration_min"] > 0).all(),
        "요금 0 이상":               (df["fee"] >= 0).all(),
        "속도 50km/h 이하":          (df["distance_km"] / (df["duration_min"] / 60) <= 50).all(),
        "거리·요금 결측 없음":        df[["distance_km", "fee"]].notna().all().all(),
        "결제수단 3종":               set(df["payment_method"]) <= {"APP", "CARD", "MEMBERSHIP"},
        "자전거 타입 2종":            set(df["bike_type"]) <= {"일반", "전동"},
    }

    for name, ok in checks.items():
        logger.info(f"  [검증] {'OK  ' if ok else 'FAIL'} {name}")

    return all(checks.values())     # 전부 True 여야 True