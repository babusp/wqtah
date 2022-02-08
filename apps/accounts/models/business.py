from distutils.command.upload import upload
from django.db import models
from apps.utility.models import BaseModel
from ckeditor.fields import RichTextField


class BusinessDetail(BaseModel):
    """Business model class"""

    level_choices = ((1, 1), (2, 2), (3, 3))

    title = models.CharField(max_length=256)
    email = models.EmailField(max_length=256)
    identity_proof = models.FileField(upload_to="media")
    location = models.CharField(max_length=256)
    lat = models.CharField(max_length=256)
    lng = models.CharField(max_length=256)
    description = RichTextField()
    level = models.IntegerField(choices=level_choices, null=True, blank=True)
    company_name = models.CharField(max_length=256, null=True, blank=True)
    company_email = models.CharField(max_length=256, null=True, blank=True)
    license = models.CharField(max_length=256, null=True, blank=True)
    company_phone = models.CharField(max_length=256, null=True, blank=True)
    company_polices = RichTextField(null=True, blank=True)
