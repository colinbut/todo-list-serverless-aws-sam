import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Fetching all todos")
    client = boto3.resource('dynamodb')
    table = client.Table('Todos')

    # TODO: scanning is expensive; revisit business requirements
    results = table.scan()

    logger.info("results: {}".format(results))
    return event

