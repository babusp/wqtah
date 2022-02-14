""" business extra views """
# django imports
from rest_framework import status, permissions
# local imports
from apps.accounts.messages import SUCCESS_CODE
from apps.business.models import Amenities, Categories, SubCategory
from apps.business.models.business import BusinessProfileMediaMapping, ServiceMediaMapping
from apps.business.serializers import AmenitySerializer, CategoriesSerializer, SubCategorySerializer
from apps.business.serializers.extra_serializer import (BusinessProfileAttachmentListSerializer,
                                                        AddBusinessProfileAttachmentSerializer,
                                                        ServiceAttachmentListSerializer, AddServiceAttachmentSerializer)
from apps.utility.viewsets import CustomModelViewSet, CustomModelListViewSet, get_object_or_404
from apps.utility.common import CustomResponse


class AddAttachmentView(CustomModelViewSet):
    """
    View for adding the new documents.
    """
    queryset = BusinessProfileMediaMapping
    serializer_class = BusinessProfileAttachmentListSerializer
    http_method_names = ['post', 'delete']
    permission_classes = [permissions.IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        """ add attachment override """
        serialized = AddBusinessProfileAttachmentSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        response = serialized.save()
        return CustomResponse(
            status=status.HTTP_200_OK, detail=SUCCESS_CODE["2000"]
        ).success_response(data=BusinessProfileAttachmentListSerializer(response).data)

    def destroy(self, request, *args, **kwargs):
        """ overriding delete attachment from business profile"""
        instance = get_object_or_404(BusinessProfileMediaMapping, pk=kwargs['pk'])
        try:
            instance.file.storage.delete(instance.file.name)
            instance.delete()
            return CustomResponse(status=status.HTTP_200_OK, detail=SUCCESS_CODE["2011"]).success_response()
        except Exception as e:
            return CustomResponse(status=status.HTTP_400_BAD_REQUEST, detail=str(e)).success_response()


class AmenityViewSet(CustomModelListViewSet):
    """View set class to amenities list"""

    serializer_class = AmenitySerializer
    queryset = Amenities.objects.all()


class CategoryViewSet(CustomModelListViewSet):
    """View set class to category list"""

    serializer_class = CategoriesSerializer
    queryset = Categories.objects.all()


class SubCategoryViewSet(CustomModelListViewSet):
    """View set class to category list"""

    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()


class AddServiceAttachmentView(CustomModelViewSet):
    """
    View for adding the new documents to service.
    """
    queryset = ServiceMediaMapping
    serializer_class = ServiceAttachmentListSerializer
    http_method_names = ['post', 'delete']
    permission_classes = [permissions.IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        """ add service attachment override """
        serialized = AddServiceAttachmentSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        response = serialized.save()
        return CustomResponse(
            status=status.HTTP_200_OK, detail=SUCCESS_CODE["2000"]
        ).success_response(data=ServiceAttachmentListSerializer(response).data)

    def destroy(self, request, *args, **kwargs):
        """ overriding delete attachment from service """
        instance = get_object_or_404(ServiceMediaMapping, pk=kwargs['pk'])
        try:
            instance.file.storage.delete(instance.file.name)
            instance.delete()
            return CustomResponse(status=status.HTTP_200_OK, detail=SUCCESS_CODE["2012"]).success_response()
        except Exception as e:
            return CustomResponse(status=status.HTTP_400_BAD_REQUEST, detail=str(e)).success_response()
