from abc import abstractmethod

from commons import ApplicationException, build_response
from commons.log_helper import get_logger

_LOG = get_logger('abstract-lambda')


class AbstractLambda:

    @abstractmethod
    def validate_request(self, event) -> dict:
        """
        Validates event attributes
        :param event: lambda incoming event
        :return: dict with attribute_name in key and error_message in value
        """
        pass

    @abstractmethod
    def handle_request(self, event, context):
        """
        Inherited lambda function code
        :param event: lambda event
        :param context: lambda context
        :return:
        """
        pass

    def lambda_handler(self, event, context):
        execution_result = self.handle_request(event=event, context=context)
        return execution_result
