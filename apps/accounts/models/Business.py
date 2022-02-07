from logging import _Level
from django.db import models
from django.forms import BaseModelForm
from auth import *


class BusinessDetail(BaseModelForm):
    """Business model class"""

    title = models.CharField(max_length=256)
    email = models.EmailField()
    identity_proof = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    description = models.TextField()
    lat = models.CharField(max_length=256)
    long = models.CharField(max_length=256)
    level = models.intField(max_length=256)
    company_name = models.CharField(max_length=256)
    company_email = models.CharField(max_length=256)
    license = models.CharField(max_length=256)
    company_phone = models.CharField(max_length=256)
    company_polices = models.TextField(max_length=256)
