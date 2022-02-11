""" Business admin """
from django.contrib import admin
from apps.business.models import business, extras

# Register your models here.

admin.site.register(business.BusinessProfile)
admin.site.register(extras.Amenities)
admin.site.register(extras.Categories)
admin.site.register(extras.SubCategory)
