"""
admin
"""
from django.contrib import admin

from apps.accounts.models import User, BusinessDetail
from apps.business.models.extras import Amenities


admin.site.register(User)
admin.site.register(BusinessDetail)
admin.site.register(Amenities)
