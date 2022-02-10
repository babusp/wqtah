"""
urls file
"""

# third party imports
from rest_framework import routers
from apps.business.views import ServiceViewSet
router = routers.DefaultRouter()
router.register(r"service", ServiceViewSet, basename="service"),

from apps.business.views.business import (
    AmenityViewSet,
    BusinessViewSet,
    BusinessProfileAmenityViewSet,
)


router = routers.SimpleRouter()

router.register(r"business", BusinessViewSet, basename="business")
router.register(r"amenities", AmenityViewSet, basename="amenities")
router.register(
    r"business-profile-amenities",
    BusinessProfileAmenityViewSet,
    basename="business-profile-amenities",
)

# local imports

urlpatterns = []
urlpatterns += router.urls
