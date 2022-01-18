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
from rest_framework.decorators import action
from datetime import datetime
from django.views.generic import TemplateView



# local imports
from apps.accounts.serializers.auth import LoginSerializer

USER = get_user_model()


# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class LoginViewSet(GenericViewSet, mixins.CreateModelMixin):
    """
    used to login the user and return the token info
        POST  /login/
        request body: {"email": "example@email.com", "password": "my-password"}
        content-type: Application/json
    """
    serializer_class = LoginSerializer