import matplotlib.pyplot as plt
import pandas as pd
import platform
import seaborn as sns

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

[분석 포인트 힌트]
- 결측치는 컬럼별로 몇 개/몇 %인지 확인하세요. (df.isnull().sum())
- 수치형 컬럼의 describe()를 보고, 최댓값/최솟값이 상식적인 범위인지
  의심해보세요. (특히 unit_price, return_rate)
- 매출(revenue) = unit_price * units_sold 로 새 컬럼을 만드세요.
- 카테고리(category)별로 매출을 합산(groupby + sum)한 뒤,
  막대 차트로 내림차순 정렬해서 그려보세요.
"""

# TODO 1-1: 컬럼별 결측치 개수를 확인하세요.
# missing_counts = ...
# print(missing_counts)

missing_counts = df.isnull().sum()
print(missing_counts)

# TODO 1-2: 수치형 컬럼 기술통계를 확인하고, 이상치로 의심되는 값을 찾아보세요.
# print(df.describe())

print(df.describe())

# TODO 1-3: revenue(매출) 컬럼을 새로 만드세요. (unit_price * units_sold)
# df["revenue"] = ...

df["revenue"] = df["unit_price"] * df["units_sold"]
print(df[["unit_price", "units_sold", "revenue"]].head())

# TODO 1-4: category별 총매출을 집계하고 내림차순 정렬하세요.
# category_revenue = df.groupby(...)[...].sum().sort_values(ascending=False)

category_revenue = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
print(category_revenue)

# TODO 1-5: category_revenue를 막대 차트(bar chart)로 그리세요.
# plt.figure(figsize=(8, 5))
# ...
# plt.title("카테고리별 총매출")
# plt.ylabel("매출(원)")
# plt.xlabel("카테고리")
# plt.tight_layout()
# plt.show()

plt.subplots(figsize=(8,5))
plt.bar(category_revenue.index, category_revenue.values)
plt.title("카테고리별 총매출")
plt.xlabel("카테고리")
plt.ylabel("매출(원)")
plt.tight_layout()
plt.savefig("과제1_카테고리별매출.png")
plt.close()

# ==================================================================
# [과제 2] 단가 vs 반품률 — 의심스러운 패턴이 있는가? (Scatter Plot)
# ==================================================================
"""
[비즈니스 문제 의도]
"단가가 비쌀수록 반품률도 높아지는가? 그렇다면 어떤 채널에서 그런
현상이 두드러지는가?"는 품질/CS 정책을 재검토할 때 자주 나오는
질문입니다. 두 연속형 지표(unit_price, return_rate) 사이의 관계를
산점도로 확인하고, 이상치가 어디에 몰려 있는지 짚어보세요.

[분석 포인트 힌트]
- 산점도를 그리기 전에 결측치가 있는 행은 제외하세요. (dropna)
- x축은 unit_price, y축은 return_rate로 두세요.
- hue 옵션에 channel(또는 category)을 지정하면, 어느 채널/카테고리에서
  이상 패턴이 나타나는지 색으로 구분해서 볼 수 있습니다.
- 산점도 위에서 유독 튀어 보이는 점(이상치)이 있다면, 그 행을 따로
  필터링해서 실제 값을 출력해보세요.
"""

# TODO 2-1: unit_price, return_rate에 결측치가 없는 데이터만 추출하세요.
# scatter_df = df.dropna(subset=[...])

scatter_df = df.dropna(subset=["unit_price","return_rate"])
print(f"원본 행 수: {len(df)}, 정제 후 행 수: {len(scatter_df)}")

# TODO 2-2: seaborn의 scatterplot을 이용해 unit_price(x) vs return_rate(y)를
#           channel(hue)로 색 구분해서 그리세요.
# plt.figure(figsize=(8, 6))
# sns.scatterplot(data=scatter_df, x=..., y=..., hue=...)
# plt.title("단가 대비 반품률 (채널별)")
# plt.tight_layout()
# plt.show()

plt.figure(figsize=(8,6))
sns.scatterplot(data=scatter_df, x="unit_price", y="return_rate", hue="channel")
plt.title("단가 대비 반품률(채널별)")
plt.tight_layout()
plt.savefig("과제2_단가반품률산점도.png")
plt.close()

# TODO 2-3: return_rate가 특정 임계값(예: 20%)을 넘는 행만 따로 조회해서
#           어떤 카테고리/채널에서 발생했는지 확인하세요.
# suspicious = scatter_df[scatter_df["return_rate"] > 20]
# print(suspicious)

suspicious = scatter_df[scatter_df["return_rate"] > 20]
print(suspicious)


# ==================================================================
# [과제 3] 채널별 리뷰 점수 분포 비교 (Box Plot / Violin Plot)
# ==================================================================
"""
[비즈니스 문제 의도]
"채널마다 리뷰 점수의 평균과 편차가 다른가? 특정 채널이 유독 낮은
평점, 혹은 들쭉날쭉한 평점을 받고 있는가?"는 채널 운영 품질을 진단할
때 쓰는 질문입니다. 평균만 보면 놓치는 분포(퍼짐 정도, 이상치)를
Box Plot 또는 Violin Plot으로 확인하세요.

[분석 포인트 힌트]
- x축에 channel, y축에 review_score를 두는 구조입니다.
- review_score의 결측치는 제외하고 그리세요.
- Box Plot은 중앙값/사분위수/이상치를 보기 좋고, Violin Plot은 분포의
  모양(밀도)까지 보여줍니다. 둘 중 하나를 선택해 그려보고, 왜 그
  채널이 그런 분포를 보이는지 한 문장으로 해석해보세요.
"""

# TODO 3-1: review_score 결측치를 제외한 데이터를 만드세요.
# box_df = df.dropna(subset=[...])

box_df = df.dropna(subset=["review_score"])

# TODO 3-2: channel별 review_score 분포를 Box Plot(또는 Violin Plot)으로
#           그리세요.
# plt.figure(figsize=(8, 6))
# sns.boxplot(data=box_df, x=..., y=...)   # 또는 sns.violinplot(...)
# plt.title("채널별 리뷰 점수 분포")
# plt.tight_layout()
# plt.show()

plt.figure(figsize=(8, 6))
sns.boxplot(data=box_df, x="channel", y="review_score")
plt.title("채널별 리뷰 점수 분포")
plt.tight_layout()
plt.savefig("과제3_채널별리뷰점수.png")
plt.close()

# TODO 3-3: channel별 review_score 평균과 표준편차를 표로도 확인하세요.
# print(box_df.groupby(...)["review_score"].agg(["mean", "std"]))
print(box_df.groupby("channel")["review_score"].agg(["mean", "std"]))

# ==================================================================
# [과제 4] 카테고리 x 채널 매출 히트맵 (또는 월별 매출 추세선)
# ==================================================================
"""
[비즈니스 문제 의도]
"어떤 카테고리가 어떤 채널에서 특히 잘 팔리는가?"는 채널별 상품 큐레이션,
프로모션 배치를 결정할 때 필요한 다차원 비교입니다. 두 범주형 축을
동시에 비교하려면 피벗 테이블 + 히트맵이 유용합니다. (시간에 따른
추세가 더 궁금하다면, 월별 매출 추세선으로 대체해도 좋습니다.)

[분석 포인트 힌트]
- 과제 1에서 만든 revenue 컬럼을 재사용하세요.
- pivot_table(index=category, columns=channel, values=revenue,
  aggfunc='sum')로 카테고리 x 채널 매출 표를 만드세요.
- sns.heatmap()으로 시각화하고, annot=True로 실제 값을 셀 안에
  표시해보세요.
- (선택) order_date에서 월(month)을 추출해 월별 카테고리 매출 추세를
  선 그래프(line plot)로 그려도 좋습니다.
"""

# TODO 4-1: category(행) x channel(열) 기준으로 revenue 합계 피벗 테이블을
#           만드세요.
# pivot = df.pivot_table(index=..., columns=..., values="revenue", aggfunc="sum")

pivot = df.pivot_table(index="category", columns="channel", values="revenue", aggfunc="sum")
print(pivot)

# TODO 4-2: 히트맵으로 시각화하세요. (annot=True로 값 표시)
# plt.figure(figsize=(9, 6))
# sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd")
# plt.title("카테고리 x 채널 매출 히트맵")
# plt.tight_layout()
# plt.show()

plt.figure(figsize=(9,6))
sns.heatmap(pivot,annot=True,fmt=".0f",cmap="YlOrRd")
plt.title("카테고리 x 채널 매출 히트맵")
plt.tight_layout()
plt.savefig("과제4_카테고리채널히트맵.png")
plt.close()

# TODO 4-3 (선택): order_date에서 월을 추출해 월별 카테고리 매출 추세선을
#           그려보세요.
# df["month"] = df["order_date"].dt.month
# monthly = df.groupby(["month", "category"])["revenue"].sum().unstack()
# monthly.plot(figsize=(10, 6))
# plt.title("월별 카테고리 매출 추세")
# plt.xlabel("월")
# plt.ylabel("매출(원)")
# plt.tight_layout()
# plt.show()
df["month"] =df["order_date"].dt.month
print(df[["order_date", "month"]].head())
monthly = df.groupby(["month","category"])["revenue"].sum().unstack()
monthly.plot(figsize=(10,6))
plt.title("월별 카테고리 매출 추세")
plt.xlabel("월")
plt.ylabel("매출(원)")
plt.tight_layout()
plt.savefig("과제4_ 월별_카테고리채널히트맵.png")
plt.close()