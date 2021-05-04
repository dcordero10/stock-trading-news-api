import requests
from datetime import datetime, timedelta
from twilio.rest import Client
import os

apikey = os.environ["API_KEY"]
account_sid = os.environ["ACCOUNT_SID"]
auth_token = os.environ["AUTH_TOKEN"]
phone = os.environ["PHONE"]

stock_params = {
    "apikey": apikey,
    "symbol": "AAPL",
    "function": "TIME_SERIES_DAILY",
}

stock_response = requests.get(url="https://www.alphavantage.co/query?", params=stock_params)
stock_response.raise_for_status()
stock_data = stock_response.json()





today = datetime.today().strftime('%Y-%m-%d')
yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
day_before_yesterday = (datetime.now() - timedelta(2)).strftime('%Y-%m-%d')


day_before_yesterday_stock_close = float(stock_data["Time Series (Daily)"][f"{day_before_yesterday}"]["4. close"])
yesterday_stock_open = float(stock_data["Time Series (Daily)"][f"{yesterday}"]["1. open"])
yesterday_stock_close = float(stock_data["Time Series (Daily)"][f"{yesterday}"]["4. close"])
stock_delta = abs(float(yesterday_stock_close) - float(day_before_yesterday_stock_close))
print(stock_delta)

    #TODO


if stock_delta > 10000.0:
    news_params = {
        "apiKey": apikey,
        "country": "us",
        "category": "business",
        "totalResults": "1",
        "q": "Apple",
    }
    news_response = requests.get(url="https://newsapi.org/v2/top-headlines?", params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()

    news_article_title = news_data["articles"][0]["title"]
    news_article_link = news_data["articles"][0]["url"]
    print(news_article_link)
    print(news_article_title)



    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=f"AAPL stock fluctuated today.\n\n {news_article_title}\n{news_article_link}",
        from_=phone,
        to=phone
    )





