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
    AWS Lambda handler for retrieving market movers data.

    This function handles GET requests to the /movers endpoint and returns
    the last 7 market days of winning stocks from DynamoDB.

    Args:
        event (Dict[str, object]): Lambda event object containing request data.
        context (Dict[str, object]): Lambda context object with runtime information.

    Returns:
        Dict: HTTP response containing:
            - statusCode (int): HTTP status code (200 for success)
            - headers (Dict): Response headers including CORS configuration
            - body (str): JSON-encoded list of cleaned stock items sorted by date (descending)

    Raises:
        None explicitly, but may raise exceptions from DynamoDB operations or JSON serialization.

    Note:
        - Results are sorted by date in descending order
        - Decimal values from DynamoDB are converted to standard Python types
        - CORS headers are included to allow cross-origin requests
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
