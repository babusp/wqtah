from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.utility.models import BaseModel
from apps.business.views import business

# Create your models here.

# Create your models here.


class Categories(BaseModel):
    """
    Category model
    """

    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


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

    business = models.ForeignKey(
        BusinessDetail, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
