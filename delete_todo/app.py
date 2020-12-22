import boto3
import json
import logging
from datetime import datetime
from aws_lambda_powertools import Tracer, Logger

tracer = Tracer()
logger = Logger()

logger.setLevel(logging.INFO)


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    
    ssm_client = boto3.client('ssm')
    sqs_client = boto3.client('sqs')
    dynamodb_client = boto3.resource('dynamodb')
    dynamodb_table = dynamodb_client.Table('Todos')

    # Get the queue by the name e.g. queue = sqs.get_queue_by_name(QueueName='test')
    # Then this doesn't require to have SSM Parameters
    delete_queue_url_param = ssm_client.get_parameter(Name='/todolist/deletequeue/url', WithDecryption=False)
    logger.debug("Delete Queue SSM Parameter: {}".format(delete_queue_url_param))
    delete_queue_url = delete_queue_url_param['Parameter']['Value']
    logger.debug("Delete Queue URL: {}".format(delete_queue_url))

    response = sqs_client.receive_message(
        QueueUrl=delete_queue_url
    )

    messages = response['Messages']
    logger.debug("Fetched messages {} from SQS Queue".format(messages))

    for message in messages:
        logger.info("Processing message: {}".format(message['MessageId']))
        receipt_handle = message['ReceiptHandle']

        item_id = message['Body']
        logger.info("Deleting item: {} from todo list".format(item_id))

        db_response = dynamodb_table.update_item(
            Key={
                'item_id': item_id
            },
            UpdateExpression="set is_deleted=:d, updated_date=:u",
            ExpressionAttributeValues={
                ':d': True,
                ':u': datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            },
            ReturnValues="UPDATED_NEW"
        )
        logger.debug("dynamodb response: {}".format(db_response))

        # delete the message once processed
        sqs_client.delete_message(
            QueueUrl=delete_queue_url,
            ReceiptHandle=receipt_handle
        )

    logger.info('Received and deleted message: %s' % message)