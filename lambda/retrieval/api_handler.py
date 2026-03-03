import os
import datetime
import boto3 
from typing import Dict

stock_movers = os.getenv("stock-movers")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(stock_movers) # type: ignore

def lambda_handler(event: Dict[str, object], context: Dict[str, object]):
    """
    GET /movers
    Returns last 7 days of winning stocks from DynamoDB.
    """
    today = datetime.datetime.now(datetime.timezone.utc)
    seven_days_ago = today - datetime.timedelta(days=7)
    
    response = table.scan()
    items = response.get("Items", [])

    # Filter items from the last 7 days
    filtered = [
        item for item in items 
        if 'date' in item and item['date'] >= seven_days_ago.strftime("%Y-%m-%d")
    ]

    # Sort by date descending
    filtered.sort(key=lambda x: x['date'], reverse=True)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"  # allows frontend to call it
        },
        "body": filtered
    }