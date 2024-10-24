import requests
from twilio.rest import Client
import os

STOCKS = ["TSLA", "MSFT", "AAPL", "META", "AMZN", "NVDA", "IBM", "GOOG", "NFLX", "WMT"]
COMPANY_NAMES = ["Tesla", "Microsoft", "Apple", "Meta", "Amazon", "NVIDIA", "IBM", "Alphabet", "Netflix", "Walmart"]
STOCK_API_KEY = os.environ.get("STOCK_API_KEY")  # Uses API from https://www.alphavantage.co to get stock information
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")  # Uses API from https://newsapi.org to get stock news
FROM_PHONE_NO = os.environ.get("FROM_PHONE_NO")  # The next 4 use Twilio API to send SMS
TO_PHONE_NO = os.environ.get("TO_PHONE_NO")
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
PERCENT_CHANGE = 5
NUM_NEWS = 1  # Change this to the number of headlines you want per company

for i in range(len(STOCKS)):
    stock_parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCKS[i],
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
            "q": COMPANY_NAMES[i]
        }
        news_response = requests.get("https://newsapi.org/v2/top-headlines", params=news_parameters)
        news_response.raise_for_status()
        news_data = news_response.json()["articles"]
        for j in range(NUM_NEWS):
            headline = news_data[j]["title"]
            brief = " ".join(news_data[j]["content"].split()[:-2])

            content = f"{STOCKS[i]}: {arrow}{rounded_change}\nHeadline: {headline}\nBrief: {brief}"
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            message = client.messages.create(body=content, from_=FROM_PHONE_NO, to=TO_PHONE_NO)
            print(message.status)
