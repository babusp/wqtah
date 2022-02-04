""""
Common file: Used for class based
"""
import secrets
import string
from datetime import datetime
from rest_framework.response import Response


class CustomResponse:
    """
    To create class for success and error response
    """

    def __init__(self, status: int, detail=None):
        """
        To set status & detail
        """
        self.status = status
        self.detail = detail

    @staticmethod
    def _get_validate_error_string(errors):
        """
        To Get string for error list
        :param errors: list
        :return: string
        """
        detail_error = list(errors.values())[0]
        if isinstance(detail_error, list):
            detail_error = detail_error[0]
        if isinstance(detail_error, dict):
            detail_error = list(detail_error.values())[0]
        return detail_error

    def success_response(self, data=None, **kwargs):
        """
        function is used for getting same global response for all api
        :param data: data
        :return: Json response
        """
        response_data = {"detail": self.detail, "data": data}
        return Response(response_data, status=self.status, **kwargs)

    def success_list_response(self, data=None, **kwargs):
        """
        function is used for getting same global response for all api
        :param data: data
        :return: Json response
        """
        if data:
            data["server_date_time"] = datetime.now()
        return Response(data, status=self.status, **kwargs)

    def error_message(self, error, **kwargs):
        """
        To for show error
        """
        return Response(
            {"detail": self.detail, "error": error}, status=self.status, **kwargs
        )

    def error_response(self, **kwargs):
        """
        function is used for getting same global error response for all api
        :return: Json response
        """
        error = self.detail
        detail = error
        if isinstance(self.detail, str):
            error = None
        else:
            detail = self._get_validate_error_string(error)
        return Response(
            {"detail": detail, "error": error}, status=self.status, **kwargs
        )


def get_random_number(string_length):
    """
    :param string_length: int type
    :return: random string of given length
    """
    return int("".join(secrets.choice(string.digits) for _ in range(string_length)))
