from rest_framework import serializers
from apps.accounts.models import BusinessDetail
from apps.business.models.extras import Amenities
from .amenities import AmenitySerilizer


class BusinessSerializer(serializers.ModelSerializer):
    amenities = serializers.SerializerMethodField(
        method_name="get_amenities", read_only=True
    )

    class Meta:
        model = BusinessDetail
        fields = "__all__"

    def get_amenities(self, obj):
        qs = Amenities.objects.filter(business=obj)
        serializer = AmenitySerilizer(qs, many=True)
        return serializer.data
