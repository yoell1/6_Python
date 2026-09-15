"""
    실습용 사이트에서
        종목 목록 페이지(CSR)의 전체 종목을 페이지를 넘겨가며 전부 수집
        - 자바스크립트로 데이터를 그리는 동적 페이지이므로 Playwright 사용
        - 한 페이지에 20개씩, 총 6페이지 (120종목)

    - 요청 주소: https://kh-lab.rockua.ai.kr/csr/stocks
"""
import json, csv
from parsers import parse_stocks
from config import BASE

from playwright.sync_api import sync_playwright



with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    context = browser.new_context(locale="ko-KR",
                                  viewport={"width":1280,"height":720})

    page = context.new_page()

    all_stocks = []

    page.goto(f"{BASE}/csr/stocks")
    page.wait_for_selector("tr.stock-row")

    for i in range(6):
        html = page.content()
        stocks = parse_stocks(html)
        print(f"{i+1} 페이지 개수 : {len(stocks)}")
        all_stocks.extend(stocks)

        if i < 5:
            page.click("button:has-text('Next')")
            page.wait_for_selector("tr.stock-row", state="detached")
            page.wait_for_selector("tr.stock-row")

    print(f"전체 : {len(all_stocks)}개")

    codes = {s['code'] for s in all_stocks}
    print(f"고유 종목코드 : {len(codes)}개")

def save_json(data, path):
    with open(path,"w",encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=3)

save_json(stocks,"it1_stocks.json") 

def save_csv(data, path):
    with open(path, "w", newline="", encoding="utf-8")as f:
        writer =csv.DictWriter(f, fieldnames =data[0].keys())

        writer.writeheader()
        writer.writerows(data)

save_csv(stocks,"it1_stocks.csv")