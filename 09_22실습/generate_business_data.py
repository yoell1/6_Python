import numpy as np
import pandas as pd

np.random.seed(40)  # Warhammer 40K 오마주 시드

N = 260  # 전체 행 수

categories = ["미니어처", "도료&도구", "룰북&코덱스", "테레인", "악세서리"]
category_probs = [0.30, 0.20, 0.15, 0.15, 0.20]

category_price_range = {
    "미니어처": (15000, 120000),
    "도료&도구": (3000, 25000),
    "룰북&코덱스": (20000, 60000),
    "테레인": (10000, 90000),
    "악세서리": (5000, 30000),
}

category_sales_lambda = {
    "미니어처": 18,
    "도료&도구": 35,
    "룰북&코덱스": 8,
    "테레인": 6,
    "악세서리": 20,
}

factions = ["스페이스 마린", "카오스", "오크", "네크론", "타이라니드", "아엘다리"]

channels = ["공식 온라인몰", "오픈마켓", "오프라인 매장", "해외 직구"]
channel_probs = [0.25, 0.42, 0.20, 0.13]

category_arr = np.random.choice(categories, size=N, p=category_probs)
faction_arr = np.random.choice(factions, size=N)
channel_arr = np.random.choice(channels, size=N, p=channel_probs)

order_dates = pd.to_datetime("2025-01-01") + pd.to_timedelta(
    np.random.randint(0, 365, size=N), unit="D"
)

unit_price = np.array(
    [np.random.randint(*category_price_range[c]) for c in category_arr]
)

units_sold = np.array(
    [max(1, np.random.poisson(category_sales_lambda[c])) for c in category_arr]
)

review_score = np.clip(np.random.normal(4.2, 0.6, size=N), 1.0, 5.0).round(1)

return_rate = np.clip(np.random.normal(4.0, 2.5, size=N), 0, None).round(1)

df = pd.DataFrame(
    {
        "order_date": order_dates,
        "category": category_arr,
        "faction": faction_arr,
        "channel": channel_arr,
        "unit_price": unit_price,
        "units_sold": units_sold,
        "review_score": review_score,
        "return_rate": return_rate,
    }
)

outlier_idx1 = df[df["category"] == "미니어처"].sample(2, random_state=1).index
df.loc[outlier_idx1, "unit_price"] = [580000, 650000]

remaining_idx = df.index.difference(outlier_idx1)
outlier_idx2 = np.random.choice(remaining_idx, size=2, replace=False)
df.loc[outlier_idx2, "return_rate"] = [42.0, 55.5]

for col, frac in [("review_score", 0.06), ("return_rate", 0.05)]:
    na_idx = np.random.choice(df.index, size=int(N * frac), replace=False)
    df.loc[na_idx, col] = np.nan

df.to_csv("business_data.csv", index=False, encoding="utf-8-sig")

print(f"데이터셋 크기: {df.shape}")
print(df.head())
print()
print("컬럼별 결측치 개수:")
print(df.isnull().sum())
print()
print("business_data.csv 저장 완료!")