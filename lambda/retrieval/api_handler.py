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
    Returns the last 7 market days of winning stocks from DynamoDB.
    """
    response = table.scan()
    items = response.get("Items", [])

    # Sort by date descending
    items.sort(key=lambda x: x['date'], reverse=True)

    # Take the most recent 7 market days
    last_seven = items[:7]

    cleaned = convert_decimals(last_seven)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET"
        },
        "body": json.dumps(cleaned)
    }
