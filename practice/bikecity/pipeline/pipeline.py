import os
import logging

from extract import extract
from transform import transform
from validate import validate
from load import load

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pipeline.log")


def setup_logger():
    """화면 + 파일(pipeline.log) 동시 기록"""
    logger = logging.getLogger("bikecity")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")

    for h in (logging.StreamHandler(), logging.FileHandler(LOG_PATH, encoding="utf-8")):
        h.setFormatter(fmt)
        logger.addHandler(h)
    return logger


def run(run_no: int = 1):
    logger = setup_logger()
    logger.info(f"===== 파이프라인 시작 ({run_no}회차) =====")

    # E : 추출
    stations, bikes, rentals = extract()
    logger.info(f"[E] stations {len(stations)} / bikes {len(bikes)} / rentals {len(rentals):,}")

    # T : 변환
    final, report = transform(stations, bikes, rentals)
    for k, v in report.items():
        logger.info(f"[T] {k} : {v}")

    # V : 검증 (통과 못 하면 적재 안 함)
    if not validate(final):
        logger.error("검증 실패 → 적재하지 않고 중단")
        return

    # L : 적재
    load(final, run_no)

    logger.info("===== 파이프라인 완료 =====")

if __name__ == "__main__":
    run(1)
    run(2)   # 재실행 검증 : 2회차는 신규 0건이어야 함