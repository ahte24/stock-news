from email import message
import requests
from twilio.rest import Client


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
stock_api_key = ""

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_api_key = ""

TWILIO_SID = ""
TWILIO_AUTH_TOKEN = ""

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_api_key,
}


response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [values for (key, values) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_brfore_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_brfore_yesterday_closing_price)

difference = abs(float(yesterday_closing_price) - float(day_brfore_yesterday_closing_price))
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)


if abs(diff_percent) > .5:
    news_params = {
        "apiKey": news_api_key,
        "q": COMPANY_NAME
    }

    response = requests.get(NEWS_ENDPOINT, params=news_params)
    response.raise_for_status()
    articles = response.json()["articles"]
    print(articles)

    three_articles = articles[:3]
    print(three_articles)
    # STEP 3: Use twilio.com/docs/sms/quickstart/python
    # to send a separate message with each article's title and description to your phone number.

    formated_articles = [f"{STOCK_NAME}: {up_down} {diff_percent}% \nHeadline: {article['title']}, \n{article['description']}" for article in three_articles]

    # TODO 9. - Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    # Optional TODO: Format the message like this:
    for article in formated_articles:
        message = client.messages.create(
            body=article,
            from_="",
            to=""
        )
    print("message sent successfully")
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
