""" amenities serializer
"""
from rest_framework import serializers
from apps.business.models.business import BusinessProfileAmenities
from apps.business.models.extras import Amenities, Categories


class BusinessProfileAmenitySerilizer(serializers.ModelSerializer):

    amenities = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BusinessProfileAmenities
        fields = "__all__"


class AmenitySerializer(serializers.ModelSerializer):
    """ Amenities serializer """
    class Meta:
        model = Amenities
        fields = ("name", "id", "icons")


class CategoriesSerializer(serializers.ModelSerializer):
    """ Categories serializer """
    class Meta:
        model = Categories
        fields = ("name", "id")


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ("id", "name")
