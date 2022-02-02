"""
auth serializer file
"""
# django imports
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

# local imports
from apps.accounts.messages import ERROR_CODE

from apps.accounts.models.auth import User

USER = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    """ used to register the user """

    class Meta:
        model = USER
        fields = ('first_name', 'last_name',"email", 'country_code', 'phone_no', 'password')



