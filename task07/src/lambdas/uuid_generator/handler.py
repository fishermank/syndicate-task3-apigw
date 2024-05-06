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

        bucket_name = os.environ['S3_BUCKET_NAME']
        _LOG.info(f'S3_BUCKET_NAME: {bucket_name}')

        s3 = boto3.client('s3')
        file_name = get_datetime()
        _LOG.info(f'file_name: {file_name}')
        uuid_data = str(uuid.uuid4())
        _LOG.info(f'uuid_data: {uuid_data}')
        s3.put_object(Body=uuid_data, Bucket=bucket_name, Key=file_name)

        return 200


HANDLER = UuidGenerator()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
