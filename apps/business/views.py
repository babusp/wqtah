""" Service views """

# Create your views here.
# django imports
from django.contrib.auth import get_user_model
from rest_framework import status

# local imports
from apps.utility.viewsets import (
    CustomModelPostListViewSet,
)
from apps.utility.common import CustomResponse
from apps.business.serializers import ServiceSerializer
from apps.accounts.messages import SUCCESS_CODE


class ServiceViewSet(CustomModelPostListViewSet):
    """View set class to register user"""

    serializer_class = ServiceSerializer

    def create(self, request, *args, **kwargs):
        """overriding for custom response"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        a = serializer.save()
        return CustomResponse(
            status=status.HTTP_200_OK, detail=SUCCESS_CODE["2008"]
        ).success_response(data=serializer.data)

    def list(self, request, *args, **kwargs):
        """overriding for custom response"""
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return CustomResponse(
            status=status.HTTP_200_OK, detail=SUCCESS_CODE["2000"]
        ).success_response(data=serializer.data)
