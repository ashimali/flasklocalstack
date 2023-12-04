import json
import datetime
import requests


def handler(event, context):
    for record in event["Records"]:
        body = json.loads(record["body"])
        message_content = body.get("content")
        result = f"Processed: {message_content} at {datetime.datetime.now()}"
        webhook_url = "http://app:5000/result"
        headers = {"Content-Type": "application/json"}
        data = {"result": result}
        response = requests.post(webhook_url, json=data, headers=headers)
        return {"statusCode": response.status_code}
