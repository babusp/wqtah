"""
urls file
"""
# third party imports

from rest_framework import routers
from django.urls import path
from apps.accounts.views.auth import (
    LoginViewSet,
    SendOTPViewSet,
    RegistrationViewSet,
    LogoutView,
    ProfileViewSet,
)

from apps.business.views.business import (
    AmenityViewSet,
    BusinessViewSet,
    BusinessProfileAmenityViewSet,
)


router = routers.DefaultRouter()
# register router for send otp in user
router.register(r"send-otp", SendOTPViewSet, basename="send_otp")
router.register(r"signup", RegistrationViewSet, basename="signup")
router.register(r"login", LoginViewSet, basename="login"),
router.register(r"profile", ProfileViewSet, basename="login"),
router.register(r"business", BusinessViewSet, basename="business")
router.register(r"amenities", AmenityViewSet, basename="amenities")
router.register(
    r"business-profile-amenities",
    BusinessProfileAmenityViewSet,
    basename="business-profile-amenities",
)


# local imports

urlpatterns = [
    path("logout/", LogoutView.as_view(), name="logout"),
] + router.urls
