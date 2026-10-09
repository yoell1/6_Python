import unicodedata
import pandas as pd


# ───── STEP 2. 자전거 마스터 정제 ─────
def clean_bikes(bikes: pd.DataFrame) -> pd.DataFrame:
    df = bikes.copy()

    # 전각 문자 → 반각 (예: "３단" → "3단", 전각 공백 제거)
    for col in df.columns:
        df[col] = df[col].map(lambda s: unicodedata.normalize("NFKC", s).strip())

    # station_id : 대문자, 빈 값은 결측
    df["station_id"] = df["station_id"].str.upper().replace("", pd.NA)

    # bike_type : 일반 / 전동 두 가지로 통일
    df["bike_type"] = (df["bike_type"]
                       .str.replace(r"\s+", "", regex=True)
                       .replace({"일반형": "일반", "electric": "전동", "Electric": "전동", "ELECTRIC": "전동"}))

    # 숫자 컬럼 : 쉼표, "단" 제거 후 숫자로 (실패는 결측)
    for col in ["gear_count", "daily_fee", "manufacture_year"]:
        df[col] = pd.to_numeric(df[col].str.replace(r"[,단]", "", regex=True), errors="coerce")

    # bike_id 기준 중복 제거
    df = df.drop_duplicates(subset=["bike_id"], keep="first")

    return df.reset_index(drop=True)

# ───── STEP 3. 대여 기록 정제 ─────
def clean_rentals(rentals: pd.DataFrame) -> pd.DataFrame:
    df = rentals.copy()

    # distance_km, fee : 쉼표 먼저 지우고 숫자로 (실패는 결측)
    for col in ["distance_km", "fee"]:
        df[col] = pd.to_numeric(df[col].str.replace(",", "", regex=False), errors="coerce")

    # rent_time, return_time : 형식 3종 혼재 → datetime
    for col in ["rent_time", "return_time"]:
        df[col] = pd.to_datetime(df[col].str.strip(), format="mixed", errors="coerce")

    # payment_method : 공백 제거 + 대문자
    df["payment_method"] = df["payment_method"].str.strip().str.upper()

    # rental_id 기준 중복 제거
    df = df.drop_duplicates(subset=["rental_id"], keep="first")

    return df.reset_index(drop=True)

# ───── STEP 4. 결합 ─────
def merge_all(rentals: pd.DataFrame, bikes: pd.DataFrame, stations: pd.DataFrame):
    # 대여 + 자전거 (매칭 확인용 _merge 컬럼 생성)
    df = rentals.merge(bikes, on="bike_id", how="left",
                       validate="many_to_one", indicator=True)

    # 매칭 실패 = 자전거 마스터에 없는 bike_id
    fail = df[df["_merge"] != "both"]

    # 매칭 성공만 남기고 _merge 컬럼 삭제
    df = df[df["_merge"] == "both"].drop(columns="_merge")

    # + 대여소 (B043은 station_id가 없어 자치구 결측으로 남음)
    df = df.merge(stations, on="station_id", how="left", validate="many_to_one")

    return df.reset_index(drop=True), fail

# ───── STEP 5. 이상치 · 논리 검사 ─────
def remove_outliers(df: pd.DataFrame):
    df = df.copy()

    # 파생 : 대여 시간(분)
    df["duration_min"] = (df["return_time"] - df["rent_time"]).dt.total_seconds() / 60

    rule1 = df["duration_min"] <= 0                          # ① 반납 ≤ 대여
    rule2 = df["fee"] < 0                                     # ② 요금 음수
    speed = df["distance_km"] / (df["duration_min"] / 60)    # km/h
    rule3 = (speed > 50) & ~rule1                             # ③ 속도 > 50km/h (시간 역전은 ①에서 처리)

    bad = rule1 | rule2 | rule3                               # 하나라도 걸리면 True

    counts = {"①": int(rule1.sum()), "②": int(rule2.sum()),
              "③": int(rule3.sum()), "합계": int(bad.sum())}

    df = df[~bad]                                             # 이상치가 아닌 행만 남김

    return df.reset_index(drop=True), counts

# ───── STEP 6. 결측 처리 ─────
def handle_missing(df: pd.DataFrame):
    df = df.copy()

    # fee 결측 → 복원 : 대여 시간(분) × 분당요금(자전거 타입별 중앙값)
    fee_na = df["fee"].isna()
    per_min = (df["fee"] / df["duration_min"]).groupby(df["bike_type"]).median()
    df.loc[fee_na, "fee"] = df.loc[fee_na, "duration_min"] * df.loc[fee_na, "bike_type"].map(per_min)

    # distance_km 결측 → 복원 근거가 없으므로 제외
    dist_na = df["distance_km"].isna()
    df = df.dropna(subset=["distance_km"])

    counts = {"요금 복원": int(fee_na.sum()), "거리 결측 제거": int(dist_na.sum())}

    return df.reset_index(drop=True), counts


# ───── STEP 2~6 한 번에 ─────
def transform(stations, bikes, rentals):
    b = clean_bikes(bikes)
    r = clean_rentals(rentals)
    m, fail = merge_all(r, b, stations)
    o, outlier_counts = remove_outliers(m)
    final, missing_counts = handle_missing(o)

    report = {
        "자전거": len(b),
        "대여(중복 제거)": len(r),
        "매칭 실패": len(fail),
        "결합 후": len(m),
        "이상치": outlier_counts,
        "결측": missing_counts,
        "최종": len(final),
    }
    return final, report

if __name__ == "__main__":
    from extract import extract

    stations, bikes, rentals = extract()

    b = clean_bikes(bikes)
    print("[STEP 2] 자전거")
    print(f"  행 수 : {len(b)}, bike_type : {b['bike_type'].unique().tolist()}")
    print(f"  station_id : {b['station_id'].nunique()}종 + 결측 {b['station_id'].isna().sum()}건")
    print(f"  gear_count : {b['gear_count'].min()} ~ {b['gear_count'].max()}, daily_fee : {b['daily_fee'].min():,} ~ {b['daily_fee'].max():,}")

    r = clean_rentals(rentals)
    print("[STEP 3] 대여")
    print(f"  행 수 : {len(r):,}")
    print(f"  distance_km 결측 : {r['distance_km'].isna().sum()}, fee 결측 : {r['fee'].isna().sum()}")
    print(f"  payment_method : {sorted(r['payment_method'].unique())}")

    m, fail = merge_all(r, b, stations)
    print("[STEP 4] 결합")
    print(f"  결합 전 : {len(r):,}행 → 매칭 실패 {len(fail)}건 {fail['bike_id'].unique().tolist()} → 제외 후 {len(m):,}행")
    print(f"  자치구 결측 : {m['district'].isna().sum()}건")

    final, report = transform(stations, bikes, rentals)
    print("[transform() 한 번에]")
    for k, v in report.items():
        print(f"  {k} : {v}")