"""
urls file
"""
# third party imports
from rest_framework import routers
from django.urls import path
from apps.accounts.models import business
from apps.accounts.views.auth import (
    LoginViewSet,
    VerifyOTPEndpoint,
    SendOTPViewSet,
    RegistrationViewSet,
)
from apps.accounts.views.business import BusinessViewSet, BusinessDetailViewSet

router = routers.DefaultRouter()
# register router for send otp in user
router.register(r"send-otp", SendOTPViewSet, basename="send_otp")
router.register(r"signup", RegistrationViewSet, basename="signup")
router.register(r"login", LoginViewSet, basename="login"),
router.register(r"business", BusinessViewSet, basename="business")
router.register(r"business", BusinessDetailViewSet, basename="business")


# local imports

urlpatterns = [
    path("verify/otp/", VerifyOTPEndpoint.as_view(), name="otp-verification"),
] + router.urls
