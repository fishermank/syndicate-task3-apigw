import datetime
import os
import uuid

import boto3

from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('AuditProducer-handler')


class AuditProducer(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass
        
    def handle_request(self, event, context):
        """Explain incoming event here"""
        _LOG.info(event)

        dynamodb = boto3.resource('dynamodb')
        conf_table_name = os.environ['GONFIGURATION_TABLE']
        audit_table_name = os.environ['AUDIT_TABLE']
        _LOG.info(f'GONFIGURATION_TABLE: {conf_table_name}')
        _LOG.info(f'AUDIT_TABLE: {audit_table_name}')
        table = dynamodb.Table(audit_table_name)

        now = datetime.datetime.now()
        iso_format = now.isoformat()

        if event['Records'][0]['eventName'] == 'INSERT':
            item = {
                "id": str(uuid.uuid4()),
                "itemKey": event['Records'][0]['dynamodb']['Keys']['key']['S'],
                "modificationTime": iso_format,
                "newValue": {
                    "key": event['Records'][0]['dynamodb']['NewImage']['key']['S'],
                    "value": event['Records'][0]['dynamodb']['NewImage']['value']['N']
                }
            }
        elif event['Records'][0]['eventName'] == 'MODIFY':
            item = {
                "id": str(uuid.uuid4()),
                "itemKey": event['Records'][0]['dynamodb']['Keys']['key']['S'],
                "modificationTime": iso_format,
                "updatedAttribute": event['Records'][0]['dynamodb']['NewImage']['key']['S'],
                "oldValue": event['Records'][0]['dynamodb']['OldImage']['value']['N'],
                "newValue": event['Records'][0]['dynamodb']['NewImage']['value']['N']
            }

        response = table.put_item(Item=item)

        return {
            'message': 'Successfully added Audit record',
            'response': response
        }


HANDLER = AuditProducer()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
