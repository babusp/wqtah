"""
urls file
"""
# third party imports
from rest_framework import routers
from django.urls import path, include
from apps.accounts import views




# local imports
from apps.accounts.views.auth import (LoginViewSet, RegisterViewSet
                                      )

router = routers.SimpleRouter()

router.register('login', LoginViewSet, basename='login')
router.register('signup', RegisterViewSet, basename='signup')


urlpatterns = [
    # path('reset-password', ResetPasswordView.as_view(), name='reset-password'),
    # path('verify-email/<int:id>/<str:token>', EmailVerificationView.as_view(), name='verify_email'),


] + router.urls




