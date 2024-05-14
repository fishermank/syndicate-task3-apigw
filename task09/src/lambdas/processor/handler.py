import json
import os
import uuid
from decimal import Decimal

import boto3
import requests
from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('Processor-handler')


def write_to_dynamo(api_response: dict):
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ['TARGET_TABLE']
    _LOG.info(f'TARGET_TABLE: {table_name}')
    table = dynamodb.Table(table_name)

    item = {
        'id': str(uuid.uuid4()),
        "forecast": {
            "elevation": api_response['elevation'],
            "generationtime_ms": api_response['generationtime_ms'],
            "hourly": {
                "temperature_2m": api_response['hourly']['temperature_2m'],
                "time": api_response['hourly']['time']
            },
            "hourly_units": {
                "temperature_2m": api_response['hourly_units']['temperature_2m'],
                "time": api_response['hourly_units']['time']
            },
            "latitude": api_response['latitude'],
            "longitude": api_response['longitude'],
            "timezone": api_response['timezone'],
            "timezone_abbreviation": api_response['timezone_abbreviation'],
            "utc_offset_seconds": api_response['utc_offset_seconds']
        }
    }

    item = json.loads(json.dumps(item), parse_float=Decimal)

    table.put_item(Item=item)


class Processor(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        url = 'https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=' \
              'temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m'
        response = requests.get(url)

        print(response.json())
        print(response.status_code)

        write_to_dynamo(response.json())

        return response.text
    

HANDLER = Processor()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
