"""
admin
"""
from django.contrib import admin

from apps.accounts.models import User, BusinessDetail


admin.site.register(User)
admin.site.register(BusinessDetail)
