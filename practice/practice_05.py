"""
    Video Game Sales 연습문제 (practice_05)

    데이터 : vgsales.csv   (16598, 11)
    열     : Rank, Name, Platform, Year, Genre, Publisher,
             NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales
"""
import pandas as pd

pd.set_option('display.width', 130)

df = pd.read_csv('vgsales.csv')


# =====================================================================
# 문제 1. 데이터 구조 파악
#   - 데이터의 행 수, 열 수를 출력
#   - 결측치가 있는 컬럼을 찾아 개수를 함께 출력
# =====================================================================
print('----- 1번 답 -----')
print(f"행 : {df.shape[0]}")
print(f"열 : {df.shape[1]}")

na = df.isna().sum()
print("결측치 개수")
print(na[na > 0])

print('-' * 60)


# =====================================================================
# 문제 2. 연도(Year) 컬럼 정리
#   - Year 의 최소값, 최대값, 가장 많이 등장하는 연도
#   - 출시 연도가 없는 데이터를 제거한 새로운 DataFrame 만들기
# =====================================================================
print('----- 2번 답 -----')
print(f"최소값 : {df['Year'].min()}")
print(f"최대값 : {df['Year'].max()}")
print(f"최빈값 : {df['Year'].mode().tolist()}")

clean = df.dropna(subset=['Year'])
print(f"제거후 : {clean.shape}")

print('-' * 60)


# =====================================================================
# 문제 3. 주요 컬럼의 고유값 탐색
#   - Platform, Genre, Publisher 각각 고유값 목록 출력
#   - Genre 는 총 몇 종류인지
# =====================================================================
print('----- 3번 답 -----')
print(f"Platform 고유값 목록 : {df['Platform'].unique().tolist()}")
print(f"Genre 고유값 목록 : {df['Genre'].unique().tolist()}")
print(f"Publisher 고유값 목록 : {df['Publisher'].unique().tolist()}")

print(f"Genre 의 종류 : {df['Genre'].nunique()}")

print('-' * 60)


# =====================================================================
# 문제 4. 연도별 게임 출시 수
#   - 연도별 게임 출시 갯수를 구하고, 연도 오름차순으로 정렬
# =====================================================================
print('----- 4번 답 -----')
print(df.groupby('Year').size().sort_index())

print('-' * 60)


# =====================================================================
# 문제 5. 플랫폼별 전 세계 판매량
#   - Platform 별로 Global_Sales 합산, 판매량 높은 순 TOP 10
# =====================================================================
print('----- 5번 답 -----')
print(df.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False).head(10))

print('-' * 60)


# =====================================================================
# 문제 6. 가장 많이 판매된 장르
#   - Genre 별 Global_Sales 총합을 구해 가장 높은 장르 찾기
# =====================================================================
print('----- 6번 답 -----')
# idxmax() : 최댓값을 가진 인덱스(이름)를 반환
print(df.groupby('Genre')['Global_Sales'].sum().idxmax())
print(df.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False).head(1))

print('-' * 60)


# =====================================================================
# 문제 7. Publisher 별 평균 판매량
#   - Publisher 별 평균 Global_Sales, 상위 10개만 출력
# =====================================================================
print('----- 7번 답 -----')
print(df.groupby('Publisher')['Global_Sales'].mean().sort_values(ascending=False).head(10))

print('-' * 60)


# =====================================================================
# 문제 8. Publisher 별 가장 많이 발매한 장르
#   - 각 Publisher 가 가장 많이 만든 장르
#     (Publisher 별로 Genre count 의 최대값 찾기)
#
#   [hint] groupby(['Publisher', 'Genre']).size().reset_index()
# =====================================================================
print('----- 8번 답 -----')
# 기준열 두 개 -> 인덱스가 두 겹(MultiIndex)이 됨
#   level=0 : 바깥쪽(Publisher) / level=1 : 안쪽(Genre)
s = df.groupby(['Publisher', 'Genre']).size()
print(s.groupby(level=0).idxmax())

print('-' * 60)


# =====================================================================
# 문제 9. 국가별로 인기 있는 장르
#   - NA / EU / JP 각각 판매량이 가장 높은 장르
# =====================================================================
print('----- 9번 답 -----')
print(f"NA : {df.groupby('Genre')['NA_Sales'].sum().idxmax()}")
print(f"EU : {df.groupby('Genre')['EU_Sales'].sum().idxmax()}")
print(f"JP : {df.groupby('Genre')['JP_Sales'].sum().idxmax()}")

print('-' * 60)