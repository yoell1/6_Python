"""
    실습용 사이트에서 
        종목 메뉴 페이지(SSR)의 섹터를 "IT 서비스"로 검색한 결과 데이터를 추출
    
    - 요청 주소: https://kh-lab.rockua.ai.kr/stocks?sector=S08&market=&q=
    TODO : 오늘 (09/15) 18시까지 이메일로 제출    
"""
import requests , json , csv

from bs4 import BeautifulSoup
from config import BASE , TIMEOUT, HEADERS
from parsers import parse_stocks

resp = requests.get(f"{BASE}/stocks",
                    params = {"sector": "S08"},
                    headers = HEADERS,
                    timeout = TIMEOUT)
resp.raise_for_status()

html = resp.text

stocks = parse_stocks(html)

print(f"stocks 개수 : {len(stocks)}")

print(f"{'코드':<8}{'종목명':<14}{'섹터':<10}{'현재가':>12}{'등락률':>9}")

for s in stocks:
    print(f"{s['code']:<8}{s['name']:<14}{s['sector']:<10}{s['price']:>12}{s['rate']:>9}")

#   추출한 
def save_json(data, path):
    with open(path,"w",encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=3)

save_json(stocks,"it_stocks.json") 

def save_csv(data, path):
    with open(path, "w", newline="", encoding="utf-8")as f:
        writer =csv.DictWriter(f, fieldnames =data[0].keys())

        writer.writeheader()
        writer.writerows(data)

save_csv(stocks,"it_stocks.csv")