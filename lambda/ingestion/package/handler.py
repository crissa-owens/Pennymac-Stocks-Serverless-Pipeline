import os
import datetime
import boto3 # type: ignore
from typing import Dict, Union
from massive import RESTClient  # type: ignore

# Load environment variables (set via Lambda console or Terraform)
MASSIVE_API_KEY = os.getenv("MASSIVE_API_KEY")
TABLE_NAME = os.getenv("TABLE_NAME")

# Initialize Massive client
client: RESTClient = RESTClient(api_key=MASSIVE_API_KEY)

# Initialize DynamoDB resource
dynamodb = boto3.resource("dynamodb") # type: ignore
table: boto3.resource("dynamodb").Table = dynamodb.Table(TABLE_NAME) # type: ignore


def fetch_stock_price(stock: str, date: str) -> dict[str, float]:
    """
    Fetch daily open and close prices for a given stock on a specific date.
    Returns a dict: {"open": float, "close": float}
    """
    aggs: list[dict[str, float]] = list(client.list_aggs(  # type: ignore
        ticker=stock,
        multiplier=1,
        timespan="day",
        from_=date,
        to=date,
        limit=1
    ))

    if not aggs:
        raise ValueError(f"No data returned for {stock} on {date}")

    bar: dict[str, float] = aggs[0]  # latest daily bar
    return {"open": bar["o"], "close": bar["c"]}


def write_to_db(record: dict[str, float | str]):
    """
    Writes the top mover record to DynamoDB.
    record should include: date, ticker, percent_change, closing_price
    """
    table.put_item(Item=record)  # type: ignore
    print(f"Written to DynamoDB: {record}")


def lambda_handler(event: Dict[str, object], context: Dict[str, object]) -> Dict[str, Union[int, str]]:
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

        ingested_data[stock] = prices
        percent_change = ((prices['close'] - prices['open']) / prices['open']) * 100
        print(f"{stock}: Open={prices['open']} Close={prices['close']} Change={percent_change:.2f}%")

        if abs(percent_change) > abs(largest_percent_change):
            largest_percent_change = percent_change
            largest_stock_change = stock

    if not largest_stock_change:
        return {"statusCode": 500, "body": "No stock data could be fetched today."}

    # Prepare record for DynamoDB
    record: dict[str, float | str] = {
        "date": yesterday,
        "ticker": largest_stock_change,
        "percent_change": round(largest_percent_change, 2),
        "closing_price": ingested_data[largest_stock_change]['close']
    }

    write_to_db(record)

    return {
        "statusCode": 200,
        "body": f"Ingestion completed. Largest change: {largest_stock_change} with {largest_percent_change:.2f}% change."
    }