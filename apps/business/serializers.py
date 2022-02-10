"""
auth serializer file
"""
# django imports
from django.contrib.auth import get_user_model
from rest_framework import serializers

# local imports
from apps.business.models import BusinessService, TimeSlotService, ServiceAmenities
USER = get_user_model()


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


class AmenitiesSerializer(serializers.ModelSerializer):
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
    amenities = AmenitiesSerializer(many=True)

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
