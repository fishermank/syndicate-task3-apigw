import datetime
import json
import os
import uuid

import boto3

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('ApiHandler-handler')


class ApiHandler(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """
        Explain incoming event here
        """
        _LOG.info(f'Event: {event}')

        # Create a DynamoDB resource object
        dynamodb = boto3.resource('dynamodb')

        # Get the DynamoDB table
        # table = dynamodb.Table('cmtr-20cb4162-Events')
        table_name = os.environ['TARGET_TABLE']
        _LOG.info(f'TARGET_TABLE: {table_name}')
        table = dynamodb.Table(table_name)

        body = event['body']
        # Deserialize the JSON data
        data = json.loads(body)

        now = datetime.datetime.now()
        iso_format = now.isoformat()

        item = {
            "id": str(uuid.uuid4()),
            "principalId": data['principalId'],
            "createdAt": iso_format,
            "body": data
        }

        # Write the item to the table
        response = table.put_item(Item=item)

        return {
            "statusCode": 201,
            "event": event,
        }


HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
