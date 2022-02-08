""" Business admin """
from django.contrib import admin
from apps.business.models import Categories, SubCategory
# Register your models here.


admin.site.register(Categories)
admin.site.register(SubCategory)
