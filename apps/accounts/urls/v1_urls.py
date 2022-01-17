"""
urls file
"""
# third party imports
from rest_framework import routers
from django.urls import path, include
from apps.accounts import views
# from django.conf.urls import url



# local imports
from apps.accounts.views.auth import LoginViewSet

router = routers.SimpleRouter()

router.register('login', LoginViewSet, basename='login')


urlpatterns = [
    # path('reset-password', ResetPasswordView.as_view(), name='reset-password'),


] + router.urls




