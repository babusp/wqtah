"""
auth views
"""
# django imports
import email
from urllib import request
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import (viewsets, status, mixins)
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView


# local imports

from apps.accounts.forms.reset_password import ResetPasswordForm
from apps.accounts.models.auth import User
from apps.accounts.messages import SUCCESS_CODE, ERROR_CODE
from apps.accounts.serializers.auth import (LoginSerializer, RegisterSerializer
                                            )
from rest_framework_simplejwt.tokens import RefreshToken


USER = get_user_model()


# Create your views here.


class LoginView(APIView):
    """
    used to login the user and return the token info
        POST  /login/
        request body: {"email": "example@email.com", "password": "my-password"}
        content-type: Application/json
    """
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = User.objects.get(email=email)
            print(user)
        except User.DoesNotExist:
            return Response({"error":"please check authentication credentils"})

        # check user is authenticater or not
        verified = user.check_password(password)
        if verified:
            jwt_token = user.get_token()
            return Response(jwt_token)
        else:
            return Response({"error":"please check authentication credentils"})


class RegisterView(APIView):
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
    def post(self, request):
        password = request.data.get("password")
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(password)
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)