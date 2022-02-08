"""
urls file
"""
# third party imports
from rest_framework import routers
from django.urls import path
from apps.accounts.views.auth import (
    LoginViewSet,
    VerifyOTPEndpoint,
    SendOTPViewSet,
    RegistrationViewSet,
    LogoutView,
)

router = routers.DefaultRouter()
# register router for send otp in user
router.register(r"send-otp", SendOTPViewSet, basename="send_otp")
router.register(r"signup", RegistrationViewSet, basename="signup")
router.register(r"login", LoginViewSet, basename="login"),


# local imports

urlpatterns = [
    path("verify/otp/", VerifyOTPEndpoint.as_view(), name="otp-verification"),
    path('logout/', LogoutView.as_view(), name="logout"),
] + router.urls
