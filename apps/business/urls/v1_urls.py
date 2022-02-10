"""
urls file
"""
# third party imports
from rest_framework import routers
from apps.business.views import ServiceViewSet
router = routers.DefaultRouter()
router.register(r"service", ServiceViewSet, basename="service"),

# local imports

urlpatterns = [
] + router.urls
