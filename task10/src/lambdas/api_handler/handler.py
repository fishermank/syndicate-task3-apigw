import os
import re

import boto3
from commons.log_helper import get_logger
from commons.abstract_lambda import AbstractLambda

_LOG = get_logger('ApiHandler-handler')


def validate_email(email):
    # Regular expression for email validation
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(pattern, email):
        _LOG.info('Bad email')
        raise Exception('Bad email')


def validate_password(password):
    # Regular expression for password validation
    pattern = r'^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[^\w\s]).{12,}$'
    if not re.match(pattern, password):
        _LOG.info('Bad password')
        raise Exception('Bad password')


def write_to_dynamo(table_name: str, item: dict):
    dynamodb = boto3.resource('dynamodb')

    _LOG.info(f'TARGET_TABLE: {table_name}')
    table = dynamodb.Table(table_name)
    # item = json.loads(json.dumps(item), parse_float=Decimal)
    table.put_item(Item=item)


def sign_up(sing_up_request: dict):
    _LOG.info('Sign up request')
    client = boto3.client('cognito-idp')

    user_pool_name = os.environ['USER_POOL']
    _LOG.info(f'user_pool_name: {user_pool_name}')

    response = client.list_user_pools(MaxResults=60)

    user_pool_id = None
    for user_pool in response['UserPools']:
        if user_pool['Name'] == user_pool_name:
            user_pool_id = user_pool['Id']
            _LOG.info(f'user_pool_id: {user_pool_id}')
            break

    username = sing_up_request['email']
    password = sing_up_request['password']
    given_name = sing_up_request['firstName']
    family_name = sing_up_request['lastName']

    validate_email(username)
    validate_password(password)

    # Create the user
    response = client.admin_create_user(
        UserPoolId=user_pool_id,
        Username=username,
        UserAttributes=[
            {
                'Name': 'email',
                'Value': username
            },
            {
                'Name': 'given_name',
                'Value': given_name
            },
            {
                'Name': 'family_name',
                'Value': family_name
            },
        ],
        TemporaryPassword=password,
        MessageAction='SUPPRESS'
    )

    _LOG.info(f'Cognito sign up response: {response}')


def sign_in(sing_in_request):
    _LOG.info('Sign in request')
    client = boto3.client('cognito-idp')

    user_pool_name = os.environ['USER_POOL']
    _LOG.info(f'user_pool_name: {user_pool_name}')

    response = client.list_user_pools(MaxResults=60)

    user_pool_id = None
    for user_pool in response['UserPools']:
        if user_pool['Name'] == user_pool_name:
            user_pool_id = user_pool['Id']
            _LOG.info(f'user_pool_id: {user_pool_id}')
            break

    username = sing_in_request['email']
    password = sing_in_request['password']

    validate_email(username)
    validate_password(password)

    app_client_id = 'YourAppClientId'

    response = client.initiate_auth(
        ClientId=app_client_id,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password
        }
    )

    _LOG.info(f'Cognito sign in response: {response}')


class ApiHandler(AbstractLambda):
        
    def handle_request(self, event, context):
        _LOG.info(f'Event: {event}')

        tables_table = os.environ['TABLES_TABLE']
        reservation_table = os.environ['RESERVATION_TABLE']

        try:
            if set(event.keys()) == {'email', 'lastName', 'password', 'firstName'}:
                sign_up(event)
            elif set(event.keys()) == {'email', 'password'}:
                sign_in(event)
            else:
                _LOG.info('Unsupported request type for my task10 app')
        except Exception as error:
            _LOG.info('Invalid request')
            _LOG.info(f'Error: {error}')
            return {
                'statusCode': 400,
                'body': {
                    'error': 'Bad request',
                    'message': f'{error}'
                }
            }

        item_table = {'id': 100}
        item_reserv = {'id': 'rrrr'}

        write_to_dynamo(tables_table, item_table)
        write_to_dynamo(reservation_table, item_reserv)

        return {
            'statusCode': 200,
            'server response': 'Success'
        }


HANDLER = ApiHandler()


def lambda_handler(event, context):
    return HANDLER.lambda_handler(event=event, context=context)
