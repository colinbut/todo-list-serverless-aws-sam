import boto3
import json
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Event:{}".format(event))

    client = boto3.resource('dynamodb')
    table = client.Table('Todos')
    
    body = json.loads(event.get('body'))
    item_id = body.get('item_id')
    title = body.get('title')
    content = body.get('content')

    response = table.update_item(
        Key={
            'item_id': item_id
        },
        UpdateExpression="set title=:r, content=:p, updated_date=:a",
        ExpressionAttributeValues={
            ':r': title,
            ':p': content,
            ':a': datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        },
        ReturnValues="UPDATED_NEW"
    )

    logger.info("Updated DynamoDB Table: {}".format(response))
    
    return {
        "statusCode": 204,
        "body": "{}"
    }
