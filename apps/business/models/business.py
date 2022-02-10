from apps.accounts.models.auth import User
from apps.business.choices import LEVEL_CHOICES
from apps.business.models.extras import Amenities, Categories, SubCategory

""" business model """
# third party import
from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

# local imports
from apps.utility.models import BaseModel, Attachments

USER = get_user_model()


class BusinessProfile(BaseModel):
    """Business Profile model class"""

    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    email = models.EmailField(max_length=256)
    identity_proof = models.FileField(upload_to="media")
    location = models.CharField(max_length=256, null=True, blank=True)
    lat = models.CharField(max_length=256, null=True, blank=True)
    lng = models.CharField(max_length=256, null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    level = models.IntegerField(choices=LEVEL_CHOICES, null=True, blank=True)
    company_name = models.CharField(max_length=256, null=True, blank=True)
    company_email = models.CharField(max_length=256, null=True, blank=True)
    license = models.CharField(max_length=256, null=True, blank=True)
    company_phone = models.CharField(max_length=256, null=True, blank=True)
    company_policies = RichTextField(null=True, blank=True)
    is_admin_verified = models.BooleanField(default=False)


class BusinessProfileAmenities(BaseModel):
    """
    sub Business Profile Amenities model
    """

    amenities = models.ForeignKey(Amenities, on_delete=models.CASCADE)
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class BusinessProfileMediaMapping(Attachments):
    """
    sub Business Profile Media Mapping model
    """

    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class BusinessService(BaseModel):
    """
    sub BusinessService model
    """

    name = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, null=True, blank=True)
    lat = models.CharField(max_length=256, null=True, blank=True)
    lng = models.CharField(max_length=256, null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


class ServiceMediaMapping(Attachments):
    """
    sub ServiceMediaMapping model
    """

    service = models.ForeignKey(BusinessService, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class TimeSlotService(BaseModel):
    """
    sub TimeSlotService model
    """

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    service = models.ForeignKey(BusinessService, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class ServiceAmenities(BaseModel):
    """
    sub ServiceAmenities model
    """

    amenities = models.ForeignKey(Amenities, on_delete=models.CASCADE)
    service = models.ForeignKey(BusinessService, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
