import boto3
from botocore.exceptions import ClientError
import json
import logging
from datetime import datetime
from aws_lambda_powertools import Tracer, Logger

tracer = Tracer()
logger = Logger()

logger.setLevel(logging.DEBUG)


@tracer.capture_method
def prep_archive_content(item_id, response):
    with open('/tmp/{}.csv'.format(item_id), 'w') as archive:
        # write csv header
        archive.write("Item Id,Title,Content,Created,Updated,Archived,Deleted,Complete,Archived Date\n")
        item = response['Item']
        entry = "{},{},{},{},{},{},{},{},{}\n".format(
                    item_id,item['title'],item['content'],item['created_date'],item['updated_date'],
                    "True",item['is_deleted'],item['is_done'],
                    datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        archive.write(entry)


@tracer.capture_method
def mark_item_archived(item_id, dynamodb_table):
    response = dynamodb_table.update_item(
        Key={
            'item_id': item_id
        },
        UpdateExpression="set is_archived=:a, updated_date=:u",
        ExpressionAttributeValues={
            ':a': True,
            ':u': datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    logger.info("Event:{}".format(event))

    path_param = event.get('pathParameters')
    item_id = path_param.get('item_id')
    logger.info("Requesting to archive item: {} from todo list".format(item_id))

    s3_client = boto3.client('s3')
    dynamodb_client = boto3.resource('dynamodb')
    dynamodb_table = dynamodb_client.Table('Todos')

    try:
        # fetching todo item from dynamodb table first
        response = dynamodb_table.get_item(Key={'item_id': item_id})
        logger.info("Fetched item: {} from DynamoDB table".format(response))

        prep_archive_content(item_id, response)

        # upload file to S3
        try:
            s3_client.upload_file('/tmp/{}.csv'.format(item_id), "todo-list-archive-bucket-cb", "{}.csv".format(item_id))
        except ClientError as ex:
            logger.error(ex)
            return {'statusCode': 502, 'body': '{ message: "Error archiving todo: " + ex }'}

        # mark todo as archived
        try:
            db_response = mark_item_archived(item_id, dynamodb_table)
            logger.debug("dynamodb response: {}".format(db_response))
        except ClientError as ex:
            logger.error(ex)
            return {'statusCode': 502, 'body': '{ message: "Error archiving todo: " + ex }'}

        response_message = { "message": "successfully archived item: {}".format(item_id) }
        logger.debug(response_message)

        return {
            'statusCode': 200,
            'body': json.dumps(response_message)
        }

    except ClientError as e:
        logger.error(e)
        
        return { 'statusCode': 502, 'body': "Error: {}".format(e) }