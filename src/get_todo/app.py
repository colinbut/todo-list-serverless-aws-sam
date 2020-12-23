import json
import boto3
import logging
from aws_lambda_powertools import Tracer, Logger

logger = Logger()
tracer = Tracer()

logger.setLevel(logging.INFO)


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    logger.info("Event:{}".format(event))
    
    path_param = event.get('pathParameters')
    item_id = path_param.get('item_id')
    logger.info("Fetching todo item: {}".format(item_id))

    client = boto3.resource('dynamodb')
    table = client.Table('Todos')

    db_response = table.get_item(Key={'item_id': item_id})
    logger.info("Fetched item: {} from DynamoDB table".format(db_response))

    item = db_response['Item']

    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }