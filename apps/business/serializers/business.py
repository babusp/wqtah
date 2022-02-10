from rest_framework import serializers
from apps.business.models.business import BusinessProfile, User
from apps.business.models.business import BusinessProfileAmenities
from apps.business.serializers.amenities import BusinessProfileAmenitySerilizer
from apps.business.models.extras import Amenities


class BusinessSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="id")

    class Meta:
        model = BusinessProfile
        fields = "__all__"

    def create(self, validated_data):
        c = validated_data.pop("amenities")
        a = BusinessProfile.objects.create(**validated_data)
        for i in c:
            amenity = Amenities.objects.get(id=i["amenities"])
            BusinessProfileAmenities.objects.create(
                business_profile=a, amenities=amenity
            )
        return a

    def get_amenities(self, obj):
        qs = BusinessProfileAmenities.objects.filter(business_profile=obj)
        serializer = BusinessProfileAmenitySerilizer(qs, many=True)
        return serializer.data


class BusinessGetsSerializer(serializers.ModelSerializer):
    amenities = serializers.SerializerMethodField(method_name="get_amenities")
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="id")

    class Meta:
        model = BusinessProfile
        fields = "__all__"

    def get_amenities(self, obj):
        qs = BusinessProfileAmenities.objects.filter(business_profile=obj)
        serializer = BusinessProfileAmenitySerilizer(qs, many=True)
        return serializer.data
