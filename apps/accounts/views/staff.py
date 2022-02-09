from apps.accounts.models.staff import StaffDetail

from apps.utility.viewsets import (
    CustomModelPostListViewSet,
    CustomModelRetrieveViewSet,
    CustomModelUpdateViewSet,
    CustomModelDestroyViewSet,
)
from apps.accounts.serializers.staff import StaffSerilizer


# local imports
from apps.accounts.messages import SUCCESS_CODE, ERROR_CODE


class StaffViewSet(
    CustomModelPostListViewSet,
    CustomModelRetrieveViewSet,
    CustomModelUpdateViewSet,
    CustomModelDestroyViewSet,
):
    """View set class to register user"""

    serializer_class = StaffSerilizer
    queryset = StaffDetail.objects.all()

    def create(self, request, *args, **kwargs):
        return super(StaffViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super(StaffViewSet, self).list(request, *args, **kwargs)
