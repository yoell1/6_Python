"""
    데이터 로드, 피처 생성 등 기능 모아두는 모듈
"""
import numpy as np
import pandas as pd

from _config import path, prices_path, ENCODING

SEED = 42


def load_merged():
    """ prices, companies, sectors를 결합하여 반환 """
    prices = pd.read_csv(prices_path(),
                         encoding=ENCODING,
                         parse_dates=["date"])
    companies = pd.read_csv(path("companies.csv"),
                            encoding=ENCODING)
    sectors = (pd.read_csv(path("sectors.csv"),
                           encoding=ENCODING)
               .rename(columns={"code": "sectorCode", "name": "sectorName"}))

    df = (prices
          .merge(companies[["code", "name", "sectorCode", "market"]],
                 how="left", on="code", validate="many_to_one")
          .merge(sectors[["sectorCode", "sectorName"]],
                 how="left", on="sectorCode", validate="many_to_one"))

    return df.sort_values(["code", "date"]).reset_index(drop=True)


# ----------------------------------------
# 피처 생성 (입력 데이터)
# ----------------------------------------
FEATURES = [
    "ret_1d",          # 전일 수익률
    "ret_5d",          # 5일 수익률
    "ma5_ratio",       # 5일 이동 평균 대비 비율
    "ma20_ratio",      # 20일 이동 평균 대비 비율
    "vol20",           # 20일 변동성
    "volume_ratio",    # 거래량 20일 평균 대비 배수
    "range_pct",       # 당일 변동폭
]


def add_features(df, shift_features=True):
    """
        피처를 생성하여 반환

        Args:
            df : 데이터셋
            shift_features : 모든 피처를 한 칸씩 밀지 여부
                - True  : "어제까지의 정보로 오늘을 예측". 모든 피처를 한 칸씩 밀어 줌
                - False : 그대로 사용. 오늘 종가로 만든 피처가 포함됨 → 데이터 누수

        Returns:
            df (피처가 추가된 데이터셋)
    """
    df = df.sort_values(["code", "date"]).copy()

    g = df.groupby("code")     # 종목코드별로 그룹화하여 계산하기 위함

    # 수익률
    df["ret_1d"] = g["close"].transform(lambda s: s.pct_change())
    df["ret_5d"] = g["close"].transform(lambda s: s.pct_change(5))

    # 이동평균 대비 비율
    df["ma5_ratio"] = df["close"] / g["close"].transform(lambda s: s.rolling(5).mean())
    df["ma20_ratio"] = df["close"] / g["close"].transform(lambda s: s.rolling(20).mean())

    # 20일 변동성 (수익률의 표준편차)
    df["vol20"] = g["close"].transform(lambda s: s.pct_change().rolling(20).std())

    # 거래량 20일 평균 대비 배수
    df["volume_ratio"] = df["volume"] / g["volume"].transform(lambda s: s.rolling(20).mean())

    # 당일 변동폭 (고가 - 저가) / 저가
    df["range_pct"] = (df["high"] - df["low"]) / df["low"] * 100

    # 데이터 누수 방지: 모든 피처를 종목별로 한 칸씩 밀기
    if shift_features:
        for col in FEATURES:
            df[col] = df.groupby("code")[col].shift(1)

    return df


# ----------------------------------------
# 정답 생성 (타깃)
# ----------------------------------------
def add_target(df):
    """
        정답 데이터 생성

        - 예측 대상: 오늘의 수익률
          * target_ret = 오늘 종가 / 어제 종가 - 1
          * target_up  = 올랐는지 여부 (0/1)
    """
    df = df.sort_values(["code", "date"]).copy()

    df["target_ret"] = df.groupby("code")["close"].pct_change()
    df["target_up"] = (df["target_ret"] > 0).astype("int8")

    return df


# ----------------------------------------
# 학습용 데이터셋 완성
# ----------------------------------------
def build_dataset(shift_features=True):
    """
        피처와 정답이 준비된 데이터를 반환
    """
    df = load_merged()

    df = add_features(df, shift_features=shift_features)
    df = add_target(df)

    # 피처나 정답이 비어 있는 행 제거 (=> 학습에 사용하기 어려움!)
    df = df.dropna(subset=FEATURES + ["target_ret", "target_up"]).reset_index(drop=True)

    # 지정한 피처의 유효하지 않은 값(무한대)도 정리
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=FEATURES).reset_index(drop=True)

    return df

def time_split(df, test_size=0.2):
    """ 시계열 데이터를 학습용, 테스트용으로 분리하여 반환 
        Args.
            df : 시계열 데이터 프레임 (날짜타입 열을 포함한 df)
            test_size : 테스트용 데이터 비율 (0.2-> 학습용: 8  테스트용: 2)
        Return. 
            분리된_학습용_데이터, 분리된_테스트용_데이터, 분리기준값     
    """
    cutoff = df["date"].quantile(1 - test_size)

    train = df[df["date"] <= cutoff].reset_index(drop=True)
    test = df[df["date"] > cutoff].reset_index(drop=True)

    return train, test, cutoff
    