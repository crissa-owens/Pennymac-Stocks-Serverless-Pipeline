import json
import os
import datetime
import boto3 
from typing import Dict
from decimal import Decimal

TABLE_NAME = os.getenv("TABLE_NAME")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME) # type: ignore

def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    if isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        return float(obj)
    return obj

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

    cleaned = convert_decimals(filtered)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET"
        },
        "body": json.dumps(cleaned)
    }