"""
auth views
"""
# django imports
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework import (viewsets, status, mixins)
from rest_framework.response import Response
from rest_framework.decorators import action




# local imports

from apps.accounts.forms.reset_password import ResetPasswordForm
from apps.accounts.models.auth import User
from apps.accounts.messages import SUCCESS_CODE, ERROR_CODE
from apps.accounts.serializers.auth import (LoginSerializer, RegisterSerializer, SendPhoneOTPSerializer,
                                            ValidatePhoneOTPSerializer
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


class PhoneVerificationAPIViewSet(viewsets.GenericViewSet):
    """
    Phone verification API
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.phone_verification_set.filter(is_active=True)

    @action(detail=False, methods=['POST'], url_path='send-otp', serializer_class=SendPhoneOTPSerializer)
    def send_otp(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request, 'user': request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'], url_path='verify-otp', serializer_class=ValidatePhoneOTPSerializer)
    def verify_otp(self, request, pk):
        print("inside view PhoneVerificationAPIViewSet....................................")

        instance = self.get_object()
        # instance = request.data.get("otp")
        print("inside instance view PhoneVerificationAPIViewSet instance.......................", instance.data)

        serializer = self.get_serializer(instance=instance, data=request.data)
        print("inside serializer view PhoneVerificationAPIViewSet serializer.......................", serializer)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Phone is verified successfully.'}, status=status.HTTP_200_OK)
        return Response(data={'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        # return Response({'message': 'Phone is verified failed......'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='get-contact')
    def get_contact(self, request):
        phone_set = request.user.phone_verification_set.filter(is_active=True)
        if phone_set:
            obj = phone_set[0]
            return Response({'id': obj.id,
                             'country_code': obj.country_code,
                             'phone_no': obj.phone_no}, status=status.HTTP_200_OK)
        return Response({'message': 'Not found'}, status=status.HTTP_400_BAD_REQUEST)
