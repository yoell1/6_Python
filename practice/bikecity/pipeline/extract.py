import os
import pandas as pd

# 이 파일(extract.py) 위치 기준으로 한 칸 위의 data 폴더
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def extract():
    """원본 CSV 3개를 문자열 그대로 읽어서 반환"""
    stations = pd.read_csv(os.path.join(DATA_DIR, "stations.csv"), dtype=str, keep_default_na=False)
    bikes = pd.read_csv(os.path.join(DATA_DIR, "raw-bikes.csv"), dtype=str, keep_default_na=False)
    rentals = pd.read_csv(os.path.join(DATA_DIR, "raw-rentals.csv"), dtype=str, keep_default_na=False)

    return stations, bikes, rentals

if __name__ == "__main__":
    stations, bikes, rentals = extract()
    print(f"stations : {stations.shape}")
    print(f"bikes    : {bikes.shape}")
    print(f"rentals  : {rentals.shape}")