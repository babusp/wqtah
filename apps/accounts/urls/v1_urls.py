"""
urls file
"""
# third party imports
from rest_framework import routers
from django.urls import path, include
from apps.accounts import views




# local imports

from apps.accounts.views.auth import LoginView, RegisterView


urlpatterns = [
    path("signup/", RegisterView.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name='login'),

    # path('reset-password', ResetPasswordView.as_view(), name='reset-password'),

    # path('verify-email/<int:id>/<str:token>', EmailVerificationView.as_view(), name='verify_email'),




]
