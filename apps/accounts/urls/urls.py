"""
main urls
"""
# third party imports
from django.urls import path, include
from  django.urls import views



urlpatterns = [
    path('v1/', include(('apps.accounts.urls.v1_urls', 'v1'), namespace='v1')),
]
