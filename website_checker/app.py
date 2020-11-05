import json
import requests
import logging

def lambda_handler(event, context):
    try:
        response = requests.get("http://checkip.amazonaws.com/")
        print(response)
    except requests.RequestException as e:
        print(e)

    return {
        "statusCode": response.status_code,
        "body": json.dumps({
            "location": response.text.replace("\n", "")
        }),
    }
