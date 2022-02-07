"""
File to load the fixtures
"""
from django.core.management import call_command
from django.http import HttpResponse

# Local imports
from django_filters import rest_framework as filters
from rest_framework.permissions import AllowAny

from apps.utility.constants import FIXTURES
from apps.utility.viewsets import CustomModelListViewSet


class FixtureFilter(filters.FilterSet):
    """
    FixtureFilter filter class
    """
    type = filters.CharFilter()

    class Meta:
        """fixture type metaclass"""
        fields = ('type', )


class LoadFixturesViewSet(CustomModelListViewSet):
    """
    Questions List ViewSet
    """
    serializer_class = None
    permission_classes = (AllowAny,)
    filterset_class = FixtureFilter
    filter_backends = (filters.DjangoFilterBackend,)

    def list(self, request, *args, **kwargs):
        """

        :param request: request
        :param args: args
        :param kwargs: kwargs
        :return:
        """
        fixture_type = request.GET.get('type', None)
        try:
            call_command('loaddata', FIXTURES[fixture_type])
        except (KeyError, TypeError) as exe:
            return HttpResponse(str(exe))
        return HttpResponse("success")
