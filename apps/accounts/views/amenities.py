from rest_framework import status
from rest_framework.response import Response
from apps.accounts.serializers.amenities import AmenitySerilizer

from apps.utility.viewsets import (
    CustomModelPostListViewSet,
)
from apps.utility.common import CustomResponse
from apps.business.models.extras import Amenities


# local imports
from apps.accounts.messages import SUCCESS_CODE, ERROR_CODE


class AmeniyViewSet(CustomModelPostListViewSet):
    """View set class to register user"""

    serializer_class = AmenitySerilizer
    queryset = Amenities.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return CustomResponse(
            status=status.HTTP_200_OK, detail=SUCCESS_CODE["2000"]
        ).success_response(data=serializer.data)
