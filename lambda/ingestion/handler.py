import datetime
import json
import boto3
from dotenv import load_dotenv
import os
from massive import RESTClient

load_dotenv()  # reads .env
MASSIVE_API_KEY = os.getenv("MASSIVE_API_KEY")
client = RESTClient(api_key=MASSIVE_API_KEY)
today = datetime.datetime.utcnow().strftime("%Y-%m-%d")

def fetch_stock_price(stock):
    # fetch daily aggregates for today
    aggs = list(client.list_aggs(
        ticker=stock,
        multiplier=1,
        timespan="day",
        from_=today,
        to=today,
        limit=1
    ))
    bar = aggs[0]  # most recent daily bar
    return {"open": bar.o, "close": bar.c}
    

def write_to_db(data):
    # Simulate writing to a database (e.g., store ingested data in DynamoDB)
    print("Writing to database:", data)

def lambda_handler(event, context):
    watchlist = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA"]
    ingested_data = {}
    largest_percent_change = 0
    largest_stock_change = ""
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    
    for stock in watchlist:
        prices = fetch_stock_price(stock)  # returns {'open': x, 'close': y}
        ingested_data[stock] = prices
        percent_change = ((prices['close'] - prices['open']) / prices['open']) * 100
        print(f"{stock}: {prices['open']} → {prices['close']} ({percent_change:.2f}%)")  # debug
        if abs(percent_change) > abs(largest_percent_change):
            largest_percent_change = percent_change
            largest_stock_change = stock

    # Currently just prints, later write to DynamoDB
    write_to_db({
        'date': today,
        'ticker': largest_stock_change,
        'percent_change': largest_percent_change,
        'closing_price': ingested_data[largest_stock_change]['close']
    })

    return {
        'statusCode': 200,
        'body': f'Ingestion completed. Largest change: {largest_stock_change} with {largest_percent_change:.2f}% change.'
    }