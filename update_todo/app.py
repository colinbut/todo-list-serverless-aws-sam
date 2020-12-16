import boto3
import logging

def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
    table = client.Table('Todos')
    return {}
