"""
serializer file
"""
from django.db.models import F
from rest_framework import serializers
# local imports
from apps.accounts.messages import ERROR_CODE
from apps.business.models import Amenities
from apps.business.models.business import BusinessProfile, User, TimeSlotService, ServiceAmenities, BusinessService
from apps.business.models.business import BusinessProfileAmenities
from apps.business.serializers.amenities import BusinessProfileAmenitySerilizer
from apps.utility.viewsets import validation_error


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
    amenities = serializers.SlugRelatedField(queryset=Amenities.objects.all(), slug_field="id", many=True)
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="id")
    location = serializers.CharField(required=True)

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
        bus_profile_obj = BusinessProfile.objects.filter(email=validated_data['email'])
        if bus_profile_obj.exists():
            raise validation_error(ERROR_CODE['4014'])
        instance = BusinessProfile.objects.create(**validated_data)
        for amenities in amenities_li:
            BusinessProfileAmenities.objects.update_or_create(business_profile=instance, amenities=amenities)
        return instance

    def update(self, instance, validated_data):
        """ overriding business profile update serializer """
        amenities_li = validated_data.pop('amenities', None)
        if amenities_li:
            BusinessProfileAmenities.objects.filter(business_profile=instance).delete()
            for amenities in amenities_li:
                BusinessProfileAmenities.objects.update_or_create(business_profile=instance, amenities=amenities)
        return instance


class TimeSlotServiceSerializer(serializers.ModelSerializer):
    """
    used to add time slot
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
    used to services list
    """
    amenities = serializers.SerializerMethodField(
        method_name="get_amenities", read_only=True
    )
    timeslot = serializers.SerializerMethodField(
        method_name="get_timeslot", read_only=True
    )

    class Meta:
        """
        Meta class defining BusinessService model and including field
        """
        model = BusinessService
        fields = "__all__"

    def get_timeslot(self, obj):
        """
        used to time slot list
        """
        time_slot = TimeSlotService.objects.filter(service=obj)
        serializer = TimeSlotServiceSerializer(time_slot, many=True)
        return serializer.data

    def get_amenities(self, obj):
        """
        used to amenities list
        """
        amenities = ServiceAmenities.objects.filter(service=obj)
        serializer = ServiceAmenitiesSerializer(amenities, many=True)
        return serializer.data


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
