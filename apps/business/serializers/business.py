"""
serializer file
"""
from rest_framework import serializers
from apps.business.models.business import BusinessProfile, User, TimeSlotService, ServiceAmenities, BusinessService
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


class TimeSlotServiceSerializer(serializers.ModelSerializer):
    """
    used to add Categories
    """
    class Meta:
        """
        Meta class defining TimeSlotService model and including field
        """
        model = TimeSlotService
        fields = ('id', 'start_time', 'end_time', 'price')


class ServiceAmenitiesSerializer(serializers.ModelSerializer):
    """
    used to add Amenities
    """
    class Meta:
        """
        Meta class defining ServiceAmenities model and including field
        """
        model = ServiceAmenities
        fields = ('id', 'amenities')


class ServiceListSerializer(serializers.ModelSerializer):
    """
    used to add services
    """
    class Meta:
        """
        Meta class defining BusinessService model and including field
        """
        model = BusinessService
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    """
    used to add services
    """
    timeslot = TimeSlotServiceSerializer(many=True)
    amenities = ServiceAmenitiesSerializer(many=True)

    class Meta:
        """
        Meta class defining BusinessService model and including field
        """
        model = BusinessService
        fields = "__all__"

    def to_representation(self, instance):
        """override to return user serialized data"""
        return ServiceListSerializer(instance).data

    def create(self, validated_data):
        """
        overriding create
        """
        time_data = validated_data.pop('timeslot')
        amenities_data = validated_data.pop('amenities')

        business = BusinessService.objects.create(**validated_data)
        for i in time_data:
            TimeSlotService.objects.create(service=business, start_time=i["start_time"], end_time=i["start_time"],
                                           price=i["price"])
        for i in amenities_data:
            ServiceAmenities.objects.create(service=business, amenities=i["amenities"])
        return business
