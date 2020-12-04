import json
import boto3
import uuid
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
            'item_title': body.get('title'),
            'item_content': body.get('content')
        }
    )

    logger.info("Inserted todo: {} into database".format(event))

    return {"statusCode": 201}
