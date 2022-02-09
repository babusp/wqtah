"""
admin
"""
from django.contrib import admin

from apps.accounts.models import User
from apps.business.models import business, extras


admin.site.register(User)
admin.site.register(business.BusinessProfile)
admin.site.register(extras.Amenities)
