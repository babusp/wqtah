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
from apps.accounts.forms.reset_password import ResetPasswordForm
from apps.accounts.models.auth import User
from apps.accounts.messages import SUCCESS_CODE, ERROR_CODE
from apps.accounts.serializers.auth import (LoginSerializer, LogoutSerializer, RegisterSerializer
                                            )
from apps.accounts.tasks.auth import logout

USER = get_user_model()


# Create your views here.

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.serializers.auth import (SendPhoneOTPSerializer, ValidatePhoneOTPSerializer,
                                            SendEmailVerificationLinkSerializer,
                                            ValidateEmailVerificationLinkSerializer,
                                            SendEmailOTPSerializer, ValidateEmailOTPSerializer)


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


class LogoutViewSet(GenericViewSet, mixins.CreateModelMixin):
    """
     Logout view is used for user logout.
     """
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def create(self, request, *args, **kwargs):
        """
        :param request: request user
        :param args: argument list
        :param kwargs: keyword argument object
        :return: logout a user
        """
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        logout.delay(request.user.id, request.META['HTTP_AUTHORIZATION'].split(" ")[1])
        return Response({'message': SUCCESS_CODE["2000"], 'data': None},
                        status=status.HTTP_200_OK)


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
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Phone is verified successfully.'}, status=status.HTTP_200_OK)
        return Response(data={'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='get-contact')
    def get_contact(self, request):
        phone_set = request.user.phone_verification_set.filter(is_active=True)
        if phone_set:
            obj = phone_set[0]
            return Response({'id': obj.id,
                             'country_code': obj.country_code,
                             'phone': obj.phone}, status=status.HTTP_200_OK)
        return Response({'message': 'Not found'}, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationAPIViewSet(viewsets.GenericViewSet):
    """
    Phone verification API
    """

    def get_queryset(self):
        return self.request.user.email_verification_set.filter(is_active=True)

    @action(detail=False, methods=['POST'], url_path='send-link', serializer_class=SendEmailVerificationLinkSerializer)
    def send_link(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'],
            url_path='verify-link',
            serializer_class=ValidateEmailVerificationLinkSerializer)
    def verify_link(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Email is verified successfully.'}, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], url_path='send-otp',
            serializer_class=SendEmailOTPSerializer,
            permission_classes=[IsAuthenticated])
    def send_otp(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request, 'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'], url_path='verify-otp',
            serializer_class=ValidateEmailOTPSerializer,
            permission_classes=[IsAuthenticated])
    def verify_otp(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Email is verified successfully.'}, status=status.HTTP_200_OK)
        return Response(data={'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class EmailVerificationView(TemplateView):
    """
    OTP Verification View
    """
    template_name = 'email_verification.html'

    def get_object(self):
        kwargs = self.kwargs
        obj = UserEmailVerification.objects.filter(id=kwargs['id'],
                                                   token=kwargs['token'],
                                                   is_active=True,
                                                   expired_at__gte=datetime.now())
        if obj:
            return obj[0]
        return None

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.is_active = False
            instance.is_verified = True
            instance.save()
            # User
            user = instance.user
            profile = user.profile
            if not profile.is_corporate:
                user.is_active = True
                user.save()
            profile.is_email_verified = True
            profile.save()

        context = self.get_context_data(instance=instance, **kwargs)
        return self.render_to_response(context)



# class ProfileViewSet(GenericViewSet, mixins.RetrieveModelMixin):
#     """
#     used to get the user details
#     POST  /profile/{user-id}
#     content-type: Application/json
#     """
#     serializer_class = UserDetailSerializer
#     permission_classes = [IsAuthenticated]
#     queryset = USER.objects.filter(is_active=True)


# class ForgotPasswordViewSet(GenericViewSet, mixins.CreateModelMixin):
#     """
#     forgot password
#     """
#     serializer_class = ForgotPasswordSerializer
#
#     def create(self, request):
#         forgot_password_serializer = self.serializer_class(data=request.data)
#         forgot_password_serializer.is_valid(raise_exception=True)
#         forgot_password_serializer.save()
#         return Response({'detail': SUCCESS_CODE["2000"], 'data': None},
#                         status=status.HTTP_400_BAD_REQUEST)


# class ResetPasswordView(View):
#     """ used to reset the user's forgot password """
#     form_class = ResetPasswordForm
#
#     def get(self, request):
#         """ used to render the reset-password html """
#         return render(request, 'auth/reset-password.html')
#
#     def post(self, request):
#         """ used to reset the user password """
#         form = ResetPasswordForm(data=request.POST)
#         if form.is_valid():
#             if request.POST['new_password'] != request.POST['confirm_password']:
#                 messages.error(request, ERROR_CODE['4006'])
#                 return redirect(reverse('account:v1:reset-password') + "?token={}&email={}".format(
#                     request.POST.get('token', ''), request.POST.get('email', '')))
#             user = USER.objects.filter(email__iexact=request.POST['email'].lower(),
#                                        forgot_pass_token=request.POST['token']).first()
#             if not user:
#                 messages.error(request, ERROR_CODE['4007'])
#                 return redirect(reverse('account:v1:reset-password') + "?token={}&email={}".format(
#                     request.POST.get('token', ''), request.POST.get('email', '')))
#
#             user.set_password(request.POST['new_password'])
#             user.forgot_pass_token = ""
#             user.forgot_pass_token_created_at = None
#             user.save()
#             messages.success(request, SUCCESS_CODE['2003'])
#             return render(request, 'auth/reset-success.html', {'front_end_url': settings.FRONT_END_URL})
#         messages.error(request, ERROR_CODE['4007'])
#         return redirect(reverse('account:v1:reset-password') + "?token={}&email={}".format(
#             request.POST.get('token', ''), request.POST.get('email', '')))
