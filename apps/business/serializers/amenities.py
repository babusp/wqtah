from rest_framework import serializers
from apps.business.models.extras import Amenities


class AmenitySerilizer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = "__all__"
