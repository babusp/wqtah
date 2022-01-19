"""
auth views
"""
# django imports
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from rest_framework import status
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework import (viewsets, status, mixins)


# local imports

from apps.accounts.forms.reset_password import ResetPasswordForm
from apps.accounts.models.auth import User
from apps.accounts.messages import SUCCESS_CODE, ERROR_CODE
from apps.accounts.serializers.auth import (LoginSerializer, RegisterSerializer
                                            )


USER = get_user_model()


# Create your views here.



class LoginViewSet(GenericViewSet, mixins.CreateModelMixin):
    """
    used to login the user and return the token info
        POST  /login/
        request body: {"email": "example@email.com", "password": "my-password"}
        content-type: Application/json
    """

    serializer_class = LoginSerializer


class RegisterViewSet(GenericViewSet, mixins.CreateModelMixin):
    """
    used to register the user and return the token info
    POST  /signup/
        request body: {
                          "first_name": "string",
                          "email": "user@example.com",
                          "password": "string"
                        }
        content-type: Application/json
    """
    serializer_class = RegisterSerializer

