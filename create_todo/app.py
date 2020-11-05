import json
import boto3

def lambda_handler(event, context):
    print(event)
    print(context)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
        }),
    }
