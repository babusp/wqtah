# django imports
from rest_framework import status, permissions
from apps.utility.viewsets import CustomModelPostListViewSet, CustomModelViewSet
from apps.utility.common import CustomResponse
from apps.business.models.business import BusinessProfile
from apps.business.serializers import BusinessProfileSerializer, BusinessProfileCreateSerializer, ServiceSerializer
from apps.accounts.messages import SUCCESS_CODE

# local imports


class BusinessProfileViewSet(CustomModelViewSet):
    """View set class for business profile """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BusinessProfileSerializer
    queryset = BusinessProfile.objects.all()
    http_method_names = ('post', 'get', 'patch')

    def get_serializer_class(self):
        """ overriding serializer class for dynamic serializer according to request """
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return BusinessProfileCreateSerializer
        return BusinessProfileSerializer

    def create(self, request, *args, **kwargs):
        """overriding for custom response"""
        serializer = self.get_serializer_class()(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse(
            status=status.HTTP_200_OK, detail=SUCCESS_CODE["2009"]
        ).success_response(data=serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return CustomResponse(
            status=status.HTTP_200_OK, detail=SUCCESS_CODE["2000"]
        ).success_response(data=serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """overriding for custom response"""
        instance = self.get_object()
        serializer = self.get_serializer_class()(
            instance, data=request.data, context={"user": request.user}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return CustomResponse(
            status=status.HTTP_200_OK, detail=SUCCESS_CODE["2010"]
        ).success_response(data=serializer.data)


class ServiceViewSet(CustomModelPostListViewSet):
    """View set class to register user"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ServiceSerializer

    def create(self, request, *args, **kwargs):
        """overriding for custom response"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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
