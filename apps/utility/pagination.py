"""
custom pagination controllers
"""
# third-party import
from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    """
    override LimitOffsetPagination
    """
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data),
            ('limit', self.get_limit(self.request)),
            ('offset', self.get_offset(self.request)),
        ]))

    def get_paginated_dict_response(self, data):
        """

        :param data: queryset to be paginated
        :return: return a simple dict obj
        """
        return {
            'count': self.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'data': data,
            'limit': self.get_limit(self.request),
            'offset': self.get_offset(self.request)
        }


class CustomPageNumberPagination(PageNumberPagination):
    """
    get_paginated_response: return OrderedDict with required attributes as last_page, next, previous links
    get_paginated_dict_response: return a dict object with the same values
    """

    def get_paginated_response(self, data):
        """

        :param data: queryset to be paginated
        :param current: current page
        :param total_records: record to be paginated
        :return: return a OrderedDict
        """
        return Response(OrderedDict([
            ('current', self.page.number),
            ('data', data),
            ('total_pages', self.page.paginator.num_pages),
            ('total', self.page.paginator.count),

        ]))

    def get_paginated_dict_response(self, data):
        """

        :param data: queryset to be paginated
        :return: return a simple dict obj
        """
        return {
            'current': self.page.number,
            'data': data,
            'total': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
        }
