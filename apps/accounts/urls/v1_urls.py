"""
urls file
"""
# third party imports
from rest_framework import routers
from apps.accounts.views.amenities import AmeniyViewSet
from apps.accounts.views.auth import (
    LoginViewSet,
    SendOTPViewSet,
    RegistrationViewSet,
    ProfileViewSet,
)
from apps.accounts.views import BusinessDetailViewSet, BusinessViewSet

router = routers.DefaultRouter()
# register router for send otp in user
router.register(r"send-otp", SendOTPViewSet, basename="send_otp")
router.register(r"signup", RegistrationViewSet, basename="signup")
router.register(r"login", LoginViewSet, basename="login"),
# router.register(r"profile", ProfileViewSet, basename="login"),
router.register(r"business", BusinessViewSet, basename="business")
router.register(r"business", BusinessDetailViewSet, basename="business")
router.register(r"amenity", AmeniyViewSet, basename="amenities")
# local imports

urlpatterns = [] + router.urls
router.register(r"profile", ProfileViewSet, basename="login"),


# local imports

# urlpatterns = [
#     path("logout/", LogoutView.as_view(), name="logout"),
# ] + router.urls
