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

    s3_client = boto3.resource('s3')
    archive_bucket = s3_client.Bucket('todo-list-archive-bucket-cb')

    archives = []
    for archive_item in archive_bucket.objects.all():
        archives.append(archive_item.key)
        logger.info("{}".format(archive_item))

    logger.info("Archives: {}".format(archives))

    return {
        'statusCode': 200,
        'body': json.dumps(archives)
    }