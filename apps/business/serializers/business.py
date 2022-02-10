from rest_framework import serializers
from apps.business.models.business import BusinessProfile, User
from apps.business.models.business import BusinessProfileAmenities
from apps.business.serializers.amenities import BusinessProfileAmenitySerilizer


class BusinessSerializer(serializers.ModelSerializer):
    amenities = serializers.SerializerMethodField(
        method_name="get_amenities", read_only=True
    )

    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="id")

    class Meta:
        model = BusinessProfile
        fields = "__all__"

    def get_amenities(self, obj):
        qs = BusinessProfileAmenities.objects.filter(business_profile=obj)
        serializer = BusinessProfileAmenitySerilizer(qs, many=True)
        return serializer.data
