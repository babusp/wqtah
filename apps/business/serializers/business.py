from rest_framework import serializers

from apps.business.models import Amenities
from apps.business.models.business import BusinessProfile, User
from apps.business.models.business import BusinessProfileAmenities
from apps.business.serializers.amenities import BusinessProfileAmenitySerilizer, AmenitySerializer


class BusinessProfileSerializer(serializers.ModelSerializer):
    """ business profile list serializer """
    amenities = serializers.SerializerMethodField(
        method_name="get_amenities", read_only=True
    )

    class Meta:
        """ meta class """
        model = BusinessProfile
        fields = "__all__"

    def get_amenities(self, obj):
        """ get amenities """
        qs = BusinessProfileAmenities.objects.filter(business_profile=obj)
        serializer = BusinessProfileAmenitySerilizer(qs, many=True)
        return serializer.data


class BusinessProfileCreateSerializer(serializers.ModelSerializer):
    """ business profile creation """
    amenities = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="id", many=True)
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="id")

    class Meta:
        """ meta class """
        model = BusinessProfile
        fields = ("amenities", "user", "title", "email", "location", "lat", "lng", "description", "level",
                  "company_name", "company_email", "license", "company_phone", "company_policies", "identity_proof")

    def to_representation(self, instance):
        """override to return user serialized data"""
        return BusinessProfileSerializer(instance).data

    def create(self, validated_data):
        """ overriding create business profile serializer """
        amenities_li = validated_data.pop('amenities')
        instance = super(BusinessProfileCreateSerializer).create(validated_data)
        for amenities in amenities_li:
            BusinessProfileAmenities.objects.update_or_create(business_profile=instance, amenities=amenities)
        return instance
