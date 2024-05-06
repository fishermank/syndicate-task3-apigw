import json
import os
import uuid
from datetime import datetime

import boto3
from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('UuidGenerator-handler')


def get_datetime():
    now = datetime.now()
    iso_format = now.isoformat()
    return iso_format[:23] + 'Z'


class UuidGenerator(AbstractLambda):

    def validate_request(self, event) -> dict:
        pass

    def handle_request(self, event, context):
        """Explain incoming event here"""
        _LOG.info(f'Event: {event}')

        bucket_name = os.environ['S3_BUCKET_NAME']
        _LOG.info(f'S3_BUCKET_NAME: {bucket_name}')

        s3 = boto3.client('s3')
        file_name = get_datetime()
        _LOG.info(f'file_name: {file_name}')

        contents = {'ids': [str(uuid.uuid4()) for _ in range(10)]}
        contents_serialized = json.dumps(contents)

        _LOG.info(f'uuid_data: {contents}')
        s3.put_object(Body=contents_serialized, Bucket=bucket_name, Key=file_name)

        return 200


HANDLER = UuidGenerator()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
