""" business extra model """
from django.db import models
from apps.utility.models import BaseModel

# Create your models here.


class Categories(BaseModel):
    """
    Category model
    """
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class SubCategory(BaseModel):
    """
    sub category model
    """
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CategorySubMapping(BaseModel):
    """
    sub category mapping model
    """
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)


class Amenities(BaseModel):
    """
    Amenities model
    """
    name = models.CharField(max_length=100)
    icons = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{}, {}".format(self.name, self.icons)
