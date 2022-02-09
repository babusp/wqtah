""" Business admin """
from django.contrib import admin
from apps.business.models import Categories, SubCategory, Amenities
# Register your models here.


admin.site.register(Categories)
admin.site.register(SubCategory)
admin.site.register(Amenities)
