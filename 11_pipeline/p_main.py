"""
    Main / Run : 파이프라인 전체를 묶어서 실행
    (⚠️ 예측 코드 - 아직 실제 수업에서 안 다룬 내용. 수업 코드와 비교용)

    - Extract → Transform → Load 순서로 실행
    - 중간에 실패하면 로그 남기고 중단
"""
import extract
import transform
import load

from config import SOURCE
from logger import setup


def run():
    """
        파이프라인 전체를 실행

        [처리 순서]
        1. 로거 준비
        2. Extract (api/csv 분기)
        3. Transform (정제 -> 검증)
        4. Load (적재 -> 검증)
        5. 완료/실패 로그
    """
    # 1. 로거 준비
    logger = setup()

    try:
        # 2. Extract
        if SOURCE == "api":
            records, failed = extract.from_api(logger)
        else:
            records, failed = extract.from_csv(logger)

        # 3. Transform
        df = transform.clean_prices(records, logger)
        transform.validate(df, logger)

        # 4. Load
        inserted, updated, t = load.to_db(df, logger)
        load.verify(df, logger)

        # 5. 완료
        logger.info(f"파이프라인 완료 - 신규 {inserted}건, 갱신 {updated}건")

    except Exception as e:
        logger.error(f"파이프라인 실패: {e}")
        raise


if __name__ == "__main__":
    run()