"""
admin
"""
from django.contrib import admin

from apps.accounts.models import User
from apps.business.models import BusinessProfile
from apps.business.models import Amenities


admin.site.register(User)
admin.site.register(BusinessProfile)
admin.site.register(Amenities)
