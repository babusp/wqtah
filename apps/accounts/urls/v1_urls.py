"""
urls file
"""
# third party imports
from rest_framework import routers
from django.urls import path, include
from apps.accounts import views
# from django.conf.urls import url



# local imports
from apps.accounts.views.auth import (LoginViewSet, RegisterViewSet, PhoneVerificationAPIViewSet,
                                      EmailVerificationAPIViewSet, EmailVerificationView,
                                      )

router = routers.SimpleRouter()

router.register('login', LoginViewSet, basename='login')
router.register('signup', RegisterViewSet, basename='signup')
# router.register('phone-verification', views.PhoneVerificationAPIViewSet, basename='phone_verification_api')
# router.register('email-verification', views.EmailVerificationAPIViewSet, basename='email_verification_api')


urlpatterns = [
    # path('reset-password', ResetPasswordView.as_view(), name='reset-password'),
    # path('verify-email/<int:id>/<str:token>', EmailVerificationView.as_view(), name='verify_email'),


] + router.urls

# urlpatterns = [
#     # Login
#     path('login/', views.auth.LoginViewSet.as_view()),
#
# ]



