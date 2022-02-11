""" amenities serializer
"""
from rest_framework import serializers
from apps.business.models.business import BusinessProfileAmenities
from apps.business.models.extras import Amenities


class BusinessProfileAmenitySerilizer(serializers.ModelSerializer):

    amenities = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BusinessProfileAmenities
        fields = "__all__"


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = "__all__"
