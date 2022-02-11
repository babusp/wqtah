""" business extra views """
# django imports
from rest_framework import status, permissions
# local imports
from apps.accounts.messages import SUCCESS_CODE
from apps.business.models import Amenities, Categories, SubCategory
from apps.business.models.business import BusinessProfileMediaMapping
from apps.business.serializers import AmenitySerializer, CategoriesSerializer, SubCategorySerializer
from apps.business.serializers.extra_serializer import (BusinessProfileAttachmentListSerializer,
                                                        AddBusinessProfileAttachmentSerializer)
from apps.utility.viewsets import CustomModelViewSet, CustomModelListViewSet
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
