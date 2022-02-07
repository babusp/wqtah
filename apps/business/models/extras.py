from django.db import models
# Create your models here.
from apps.utility.models import BaseModel


class Categories(BaseModel):
    """
    Category model
    """
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


class SubCategory(BaseModel):
    """
    sub category model
    """
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)


class Amenities(BaseModel):
    """
    Amenities model
    """
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
