import os
import datetime
import time
import boto3 
from typing import Dict, Union
from massive import RESTClient 
from decimal import Decimal

# Load environment variables (set via Lambda console or Terraform)
MASSIVE_API_KEY = os.getenv("MASSIVE_API_KEY")
TABLE_NAME = os.getenv("TABLE_NAME")

# Initialize Massive client
client: RESTClient = RESTClient(api_key=MASSIVE_API_KEY)

# Initialize DynamoDB resource
dynamodb = boto3.resource("dynamodb") 
table: boto3.resource("dynamodb").Table = dynamodb.Table(TABLE_NAME) # type: ignore


def fetch_stock_price(stock: str, date: str): 
    retries = 8 
    for attempt in range(retries): 
        try: aggs = list(client.list_aggs( ticker=stock, multiplier=1, timespan="day", from_=date, to=date, limit=1 )) 
        except Exception as e: 
            if "429" in str(e):
                wait = 1 + attempt 
                print(f"429 for {stock} on {date}. Retrying in {wait}s...") 
                time.sleep(wait) 
                continue 
            raise 
        if not aggs: 
            raise ValueError(f"No data returned for {stock} on {date}") 
        bar = aggs[0] 
        return {"open": bar.open, "close": bar.close} # type: ignore
    raise ValueError(f"Failed after retries for {stock} on {date}")

def write_to_db(record: dict[str, float | str]):
    """
    Writes the top mover record to DynamoDB.
    record should include: date, ticker, percent_change, closing_price
    """
    table.put_item(Item=record)  
    print(f"Written to DynamoDB: {record}")


def lambda_handler(event: Dict[str, object], context: Dict[str, object]) -> Dict[str, Union[int, str]]:
    """
    AWS Lambda handler that ingests stock price data and identifies the stock with the largest percentage change.
    
    This function fetches stock prices for a predefined watchlist of stocks for the previous trading day,
    calculates the percentage change from open to close, and stores the stock with the largest absolute
    percentage change to DynamoDB.
    
    Args:
        event (Dict[str, object]): Lambda event object (unused in this implementation).
        context (Dict[str, object]): Lambda context object (unused in this implementation).
    
    Returns:
        Dict[str, Union[int, str]]: A response dictionary containing:
            - statusCode (int): HTTP status code (200 for success, 500 for failure).
            - body (str): Response message describing the ingestion result or error.
    
    Raises:
        Exception: Exceptions from fetch_stock_price are caught and logged individually;
                   write_to_db exceptions will propagate to the caller.
    
    Side Effects:
        - Prints stock price data and percentages changes to stdout.
        - Writes the stock with the largest price change to DynamoDB via write_to_db.
    """
    watchlist = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA"]
    yesterday = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    ingested_data: dict[str, dict[str, float]] = {}

    largest_percent_change = 0
    largest_stock_change = ""

    # Fetch prices for each stock and calculate % change
    for stock in watchlist:
        try:
            prices = fetch_stock_price(stock, yesterday)
        except Exception as e:
            print(f"Error fetching {stock}: {e}")
            continue

        ingested_data[stock] = prices # type: ignore
        percent_change = ((prices['close'] - prices['open']) / prices['open']) * 100 # type: ignore
        print(f"{stock}: Open={prices['open']} Close={prices['close']} Change={percent_change:.2f}%")

        if abs(percent_change) > abs(largest_percent_change):
            largest_percent_change = percent_change
            largest_stock_change = stock

    if not largest_stock_change:
        return {"statusCode": 500, "body": "No stock data could be fetched today."}

    # Prepare record for DynamoDB
    record = {
    "date": yesterday,
    "ticker": largest_stock_change,
    "percent_change": Decimal(str(round(largest_percent_change, 2))),
    "closing_price": Decimal(str(ingested_data[largest_stock_change]['close']))
    }

    write_to_db(record)

    return {
        "statusCode": 200,
        "body": f"Ingestion completed. Largest change: {largest_stock_change} with {largest_percent_change:.2f}% change."
    }