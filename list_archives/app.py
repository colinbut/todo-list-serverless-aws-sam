import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


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