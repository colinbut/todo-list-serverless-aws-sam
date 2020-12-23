import json
import boto3
import uuid
import logging
from datetime import datetime
from aws_lambda_powertools import Tracer, Logger

tracer = Tracer()
logger = Logger()

logger.setLevel(logging.INFO)

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    logger.debug("event: {}".format(event))
    logger.debug("context: {}".format(context))

    logger.info("Inserting todo: {} into database".format(event))

    body = json.loads(event.get('body'))

    client = boto3.resource('dynamodb')
    table = client.Table('Todos')
    table.put_item(
        Item={
            'item_id': str(uuid.uuid1()),
            'title': body.get('title'),
            'content': body.get('content'),
            'created_date': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            'updated_date': None,
            'is_archived': False,
            'is_deleted': False,
            'is_done': False
        }
    )

    logger.info("Inserted todo: {} into database".format(event))

    return {"statusCode": 201}
