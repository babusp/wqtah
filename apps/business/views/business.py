# django imports
from multiprocessing import context
from rest_framework import status, serializers, permissions
from rest_framework.response import Response
from apps.accounts.models.auth import User
from apps.business.models.extras import Amenities
from apps.business.serializers.amenities import (
    AmenitySerializer,
    BusinessProfileAmenitySerilizer,
)

from apps.utility.viewsets import CustomModelPostListViewSet, CustomModelUpdateViewSet
from apps.utility.common import CustomResponse
from apps.business.models.business import BusinessProfile, BusinessProfileAmenities
from apps.business.serializers import BusinessGetsSerializer, BusinessSerializer
from apps.accounts.messages import SUCCESS_CODE

# local imports


class BusinessViewSet(CustomModelPostListViewSet):
    """View set class to register user"""

    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = BusinessSerializer
    queryset = BusinessProfile.objects.all()

    def create(self, request, *args, **kwargs):
        """overriding for custom response"""
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse(
            status=status.HTTP_200_OK, detail=SUCCESS_CODE["2001"]
        ).success_response(data=serializer.data)

    def list(self, request, *args, **kwargs):
        self.serializer_class = BusinessGetsSerializer
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return CustomResponse(
            status=status.HTTP_200_OK, detail=SUCCESS_CODE["2000"]
        ).success_response(data=serializer.data)

    def get_object(self, pk):
        try:
            queryset = BusinessProfile.objects.get(pk=pk)
            return queryset
        except BusinessProfile.DoesNotExist:
            raise serializers.ValidationError({"message": "business id not found."})

    def retrieve(self, request, pk):
        instance = self.get_object(pk)
        serializer = BusinessGetsSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk):
        queryset = self.get_object(pk)
        serializer = BusinessSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AmenityViewSet(CustomModelPostListViewSet):
    """View set class to register user"""

    serializer_class = AmenitySerializer
    queryset = Amenities.objects.all()

    def create(self, request, *args, **kwargs):
        """overriding for custom response"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse(
            status=status.HTTP_200_OK, detail=SUCCESS_CODE["2001"]
        ).success_response(data=serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return CustomResponse(
            status=status.HTTP_200_OK, detail=SUCCESS_CODE["2000"]
        ).success_response(data=serializer.data)


class BusinessProfileAmenityViewSet(CustomModelPostListViewSet):
    """View set class to register user"""

    serializer_class = BusinessProfileAmenitySerilizer
    queryset = BusinessProfileAmenities.objects.all()

    def create(self, request, *args, **kwargs):
        """overriding for custom response"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse(
            status=status.HTTP_200_OK, detail=SUCCESS_CODE["2001"]
        ).success_response(data=serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return CustomResponse(
            status=status.HTTP_200_OK, detail=SUCCESS_CODE["2000"]
        ).success_response(data=serializer.data)
