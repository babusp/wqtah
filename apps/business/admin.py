""" Business admin """
from django.contrib import admin

from apps.business.models.extras import Categories, SubCategory, Amenities
# Register your models here.


admin.site.register(Categories)
admin.site.register(SubCategory)
