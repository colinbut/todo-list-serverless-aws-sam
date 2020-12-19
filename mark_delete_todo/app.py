import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Event:{}".format(event))
    path_param = event.get('pathParameters')
    item_id = path_param.get('item_id')
    logger.info("Requesting to delete item: {} from todo list".format(item_id))
    
    ssm_client = boto3.client('ssm')
    sqs_client = boto3.client('sqs')

    # Get the queue by the name e.g. queue = sqs.get_queue_by_name(QueueName='test')
    # Then this doesn't require to have SSM Parameters
    delete_queue_url_param = ssm_client.get_parameter(Name='/todolist/deletequeue/url', WithDecryption=False)
    logger.debug("Delete Queue SSM Parameter: {}".format(delete_queue_url_param))
    delete_queue_url = delete_queue_url_param['Parameter']['Value']
    logger.debug("Delete Queue URL: {}".format(delete_queue_url))

    logger.debug("Sending request delete message to queue: {}".format(delete_queue_url))

    response = sqs_client.send_message(
        QueueUrl=delete_queue_url,
        DelaySeconds=10,
        MessageBody=json.dumps(item_id)
    )

    logger.info("Sent message: {} to SQS: {}".format(response.get('MessageId'), delete_queue_url))

    return {
        'statusCode': 204,
        'body': '{ "message": "delete requested" }'
    }
