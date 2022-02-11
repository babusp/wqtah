"""
custom exception handler
"""
import logging
# third party imports
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.exceptions import APIException
exception_logger = logging.getLogger()


def dict_list_exception_handler(error_message, response):
    """
    handle dict, list type error response
    :param error_message:
    :param response:
    :return:
    """

    if isinstance(response, dict):
        response_key = list(response.keys())[0]
        if isinstance(response[response_key], list):
            error_message.update({'detail': response[response_key][0]})
        elif isinstance(response[response_key], dict):
            error_message.update({'detail': response[response_key][list(response[response_key].keys())[0]][0]})
        else:
            error_message.update({'detail': response[response_key]})

    elif isinstance(response, list):
        error_message.update({'detail': response[0]})

    return error_message


def custom_exception_handler(exc, context):
    """
    Call REST framework's default exception handler first,
    to get the standard error response.
    :param exc: exception object
    :param context:
    :return:
    """

    response = exception_handler(exc, context)
    error_message = {}
    if response:
        exception = {'errors': response.data}
        if str(response.status_code) in ['401', '403', '404', '405']:
            error_message.update(**response.data)
        error_message = dict_list_exception_handler(error_message, response.data)
        # add the error_message in response data
        exception.update(error_message)
        response.data = exception
    return response


class ValidationError(APIException):
    """
    custom validation error for the project to provide dict
    fields as defined
    raises API exceptions with custom messages and custom status codes
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'error'

    def __init__(self, detail, status_code=None):
        """initialize status_code if passed with exception
        otherwise pass default"""
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code
