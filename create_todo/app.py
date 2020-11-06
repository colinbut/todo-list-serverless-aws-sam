import json
import boto3
import uuid

def lambda_handler(event, context):
    print("event: {}".format(event))
    print("context: {}".format(context))

    print("Inserting todo: {} into database".format(event))

    client = boto3.client('dynamodb')
    client.put_item(
        TableName='Todos',
        Item={
            "item_id": str(uuid.uuid1()),
            "item_title": event.title,
            "item_content": event.content
        }
    )

    print("Inserted todo: {} into database".format(event))

    return {"statusCode": 201}
