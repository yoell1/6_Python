"""
[워해머 4K] 주간 경영진 비즈니스 리뷰 — 신입 분석가 실습 과제 (함수 버전)
================================================================
utils/chart_utils.py 의 out(), save_and_close() 함수를 사용합니다.
================================================================
"""

import matplotlib.pyplot as plt
import pandas as pd
import platform
import seaborn as sns

from utils.chart_utils import save_and_close

# ----------------------------------------------------------------
# 0. 한글 폰트 설정
# ----------------------------------------------------------------
if platform.system() == "Windows":
    plt.rcParams["font.family"] = "Malgun Gothic"
elif platform.system() == "Darwin":
    plt.rcParams["font.family"] = "AppleGothic"
else:
    plt.rcParams["font.family"] = "NanumGothic"

plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv("business_data.csv", parse_dates=["order_date"])


# ==================================================================
# [과제 1] 데이터 신뢰도 점검 + 카테고리별 핵심 지표 Bar Chart
# ==================================================================
"""
[비즈니스 문제 의도]
경영진 보고 전, "이 숫자를 그대로 믿고 보고해도 되는가?"를 먼저 검증해야
합니다. 결측치와 이상치를 확인하지 않고 만든 차트는 잘못된 의사결정으로
이어질 수 있습니다. 점검이 끝나면 "카테고리별 매출 규모에 쏠림이
발생하는가?"에 답하는 막대 차트를 그려주세요.
"""

# TODO 1-1: 컬럼별 결측치 개수를 확인하세요.
missing_counts =df.isnull().sum()
print(missing_counts)

# TODO 1-2: 수치형 컬럼 기술통계를 확인하고, 이상치로 의심되는 값을 찾아보세요.
print(df.describe())

# TODO 1-3: revenue(매출) 컬럼을 새로 만드세요. (unit_price * units_sold)
df["revenue"] = df["unit_price"] * df["units_sold"]
print(df[["unit_price","units_sold","revenue"]].head())

# TODO 1-4: category별 총매출을 집계하고 내림차순 정렬하세요.
category_revenue = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
print(category_revenue)

# TODO 1-5: category_revenue를 막대 차트로 그리세요.
#   plt.figure(figsize=(8, 5))
#   plt.bar(...)
#   plt.title(...)
#   plt.xlabel(...)
#   plt.ylabel(...)
#   save_and_close("과제1_카테고리별매출.png")   # <- 3줄 대신 이거 한 줄
plt.subplots(figsize=(8,5))
plt.bar(category_revenue.index,category_revenue.values)
plt.title("카테고리별 총매출")
plt.xlabel("카테고리")
plt.ylabel("매출(원)")
save_and_close("과제1_카테고리별매출.png")

# ==================================================================
# [과제 2] 단가 vs 반품률 — 의심스러운 패턴이 있는가? (Scatter Plot)
# ==================================================================
"""
[비즈니스 문제 의도]
"단가가 비쌀수록 반품률도 높아지는가? 그렇다면 어떤 채널에서 그런
현상이 두드러지는가?"는 품질/CS 정책을 재검토할 때 자주 나오는
질문입니다.
"""

# TODO 2-1: unit_price, return_rate에 결측치가 없는 데이터만 추출하세요.
scatter_df = df.dropna(subset=["unit_price","return_rate"])
print(f"원본 행 수: {len(df)}, 정제 후 행 수: {len(scatter_df)}")

# TODO 2-2: unit_price(x) vs return_rate(y)를 channel(hue)로 색 구분해서
#           산점도로 그리세요. save_and_close() 사용.
plt.figure(figsize=(8,6))
sns.scatterplot(data=scatter_df,x="unit_price",y="return_rate",hue="channel")
plt.title("단가 대비 반품률(채널별)")
save_and_close("과제2_단가반품률산점도.png")

# TODO 2-3: return_rate가 20%를 넘는 행만 따로 조회하세요.
suspicious = scatter_df[scatter_df["return_rate"] > 20]
print(suspicious)


# ==================================================================
# [과제 3] 채널별 리뷰 점수 분포 비교 (Box Plot)
# ==================================================================
"""
[비즈니스 문제 의도]
"채널마다 리뷰 점수의 평균과 편차가 다른가?"를 Box Plot으로 확인하세요.
"""

# TODO 3-1: review_score 결측치를 제외한 데이터를 만드세요.
box_df = df.dropna(subset=["review_score"])

# TODO 3-2: channel별 review_score 분포를 Box Plot으로 그리세요.
#           save_and_close() 사용.
plt.figure(figsize=(8,6))
sns.boxplot(data=box_df,x="channel",y="review_score")
plt.title("채널별 리뷰 점수 분포")
save_and_close("과제3_채널별리뷰점수.png")

# TODO 3-3: channel별 review_score 평균과 표준편차를 확인하세요.
print(box_df.groupby("channel")["review_score"].agg(["mean","std"]))



# ==================================================================
# [과제 4] 카테고리 x 채널 매출 히트맵 + 월별 추세선
# ==================================================================
"""
[비즈니스 문제 의도]
"어떤 카테고리가 어떤 채널에서 특히 잘 팔리는가?"를 히트맵으로,
"월별로 카테고리 매출 추세가 다른가?"를 선 그래프로 확인하세요.
"""

# TODO 4-1: category(행) x channel(열) 기준으로 revenue 합계 피벗 테이블을
#           만드세요.
pivot = df.pivot_table(index="category",columns="channel",values="revenue",aggfunc="sum")
print(pivot)

# TODO 4-2: 히트맵으로 시각화하세요. (annot=True) save_and_close() 사용.
plt.figure(figsize=(9,6))
sns.heatmap(pivot,annot=True,fmt=".0f",cmap="YlOrRd")

# TODO 4-3: order_date에서 월을 추출해 월별 카테고리 매출 추세선을
#           그리세요. save_and_close() 사용.
df["month"] = df["order_date"].dt.month
print(df[["order_date", "month"]].head())
monthly = df.groupby(["month","category"])["revenue"].sum().unstack()
monthly.plot(figsize=(10,6))
plt.title("월별 카테고리 매출 추세")
plt.xlabel("월")
plt.ylabel("매출(원)")
save_and_close("과제4_월별_카테고리채널히트맵.png")
