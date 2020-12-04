import json
import pytest
import boto3
from moto import mock_dynamodb2

from create_todo import app

@mock_dynamodb2
def test_lambda_handler():

    event = {
                'body': """{
                    "title": "Todo Title",
                    "content": "Todo Content"
                }"""
            }

    conn = boto3.resource("dynamodb")
    conn.create_table(
        TableName="Todos",
        KeySchema=[{"AttributeName": "item_id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "item_id", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )

    ret = app.lambda_handler(event, "")
    print(ret)

    assert ret["statusCode"] == 201

