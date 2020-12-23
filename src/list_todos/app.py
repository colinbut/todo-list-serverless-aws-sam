import json
import boto3
import json
import logging
from aws_lambda_powertools import Tracer, Logger

tracer = Tracer()
logger = Logger()

logger.setLevel(logging.INFO)

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    logger.info("Event:{}".format(event))
    logger.info("Fetching all todos")
    client = boto3.resource('dynamodb')
    table = client.Table('Todos')

    # TODO: scanning is expensive; revisit business requirements
    results = table.scan()

    logger.info("results: {}".format(results))
    return {
        "statusCode": 200,
        "body": str(json.dumps(results))
    }

