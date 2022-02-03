"""
urls file
"""
# third party imports
from rest_framework import routers
from django.urls import path
from apps.accounts.views.auth import LoginView, VerifyOTPEndpoint, SendOTPViewSet, RegistrationViewSet
router = routers.DefaultRouter()
# register router for send otp in user
router.register(r'send-otp', SendOTPViewSet, basename='send_otp')
router.register(r'signup', RegistrationViewSet, basename='signup')

# local imports

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("verify/otp/", VerifyOTPEndpoint.as_view(), name="otp-verification"),
] + router.urls
