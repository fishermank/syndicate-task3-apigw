import os

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

        item = {
            'id': 'safsdfas',
            'param': 'pampam'
        }

        response = table.put_item(Item=item)

        return {
            'Test': 'test1'
        }


HANDLER = AuditProducer()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
