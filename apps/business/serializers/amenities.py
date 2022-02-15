""" amenities serializer
"""
from rest_framework import serializers
from apps.business.models.business import BusinessProfileAmenities
from apps.business.models.extras import Amenities, Categories


class BusinessProfileAmenitySerilizer(serializers.ModelSerializer):
    """business profile amenities serializer"""

    amenities = serializers.StringRelatedField(read_only=True)

    class Meta:
        """meta class"""

        model = BusinessProfileAmenities
        fields = "__all__"


class AmenitySerializer(serializers.ModelSerializer):
    """Amenities serializer"""

    class Meta:
        """meta class"""

        model = Amenities
        fields = ("name", "id", "icons")


class CategoriesSerializer(serializers.ModelSerializer):
    """Categories serializer"""

    class Meta:
        """meta class"""

        model = Categories
        fields = ("name", "id")


class SubCategorySerializer(serializers.ModelSerializer):
    """sub category serializer"""

    class Meta:
        """meta class"""

        model = Categories
        fields = ("id", "name")
