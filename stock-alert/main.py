import requests
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla"
STOCK_API_KEY = os.environ.get("STOCK_API_KEY")  # Uses API from https://www.alphavantage.co to get stock information
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")  # Uses API from https://newsapi.org to get stock news
PERCENT_CHANGE = 5

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}
stock_response = requests.get("https://www.alphavantage.co/query", params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]
stock_keys = list(stock_data.keys())
stock_one_day_before = float(stock_data[stock_keys[1]]["4. close"])
stock_two_day_before = float(stock_data[stock_keys[2]]["4. close"])
stock_change_percent = ((stock_one_day_before - stock_two_day_before)/stock_one_day_before) * 100

rounded_change = abs(round(stock_change_percent))
if stock_change_percent > 0:
    arrow = "🔺"
else:
    arrow = "🔻"

if abs(stock_change_percent) >= PERCENT_CHANGE:
    news_parameters = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME
    }
    news_response = requests.get("https://newsapi.org/v2/top-headlines", params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]

    print(news_data)
