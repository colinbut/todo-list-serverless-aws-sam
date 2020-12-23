import boto3
import logging
import json
from datetime import datetime
from aws_lambda_powertools import Tracer, Logger

tracer = Tracer()
logger = Logger()

logger.setLevel(logging.INFO)


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    logger.info("Event:{}".format(event))

    client = boto3.resource('dynamodb')
    table = client.Table('Todos')

    path_param = event.get('pathParameters')
    item_id = path_param.get('item_id')

    response = table.update_item(
        Key={
            'item_id': item_id
        },
        UpdateExpression="set is_done=:d, updated_date=:p",
        ExpressionAttributeValues={
            ':d': True,
            ':p': datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        },
        ReturnValues="ALL_NEW"
    )

    logger.info("Updated DynamoDB Table: {}".format(response))
    
    return {
        'statusCode': 204
    }    