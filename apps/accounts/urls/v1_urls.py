"""
urls file
"""
# third party imports
from rest_framework import routers
from apps.accounts.views.auth import (
    LoginViewSet,
    SendOTPViewSet,
    RegistrationViewSet,
    ProfileViewSet,
)


router = routers.DefaultRouter()
# register router for send otp in user
router.register(r"send-otp", SendOTPViewSet, basename="send_otp")
router.register(r"signup", RegistrationViewSet, basename="signup")
router.register(r"login", LoginViewSet, basename="login"),
router.register(r"profile", ProfileViewSet, basename="login"),


# local imports

urlpatterns = [] + router.urls
