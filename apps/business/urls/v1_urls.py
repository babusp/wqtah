"""
urls file
"""

# third party imports
from rest_framework import routers
router = routers.DefaultRouter()
from apps.business.views.business import (
    AmenityViewSet,
    BusinessViewSet,
    BusinessProfileAmenityViewSet,
    ServiceViewSet,
)

router.register(r"business", BusinessViewSet, basename="business")
router.register(r"amenities", AmenityViewSet, basename="amenities")
router.register(r"service", ServiceViewSet, basename="service"),
router.register(
    r"business-profile-amenities",
    BusinessProfileAmenityViewSet,
    basename="business-profile-amenities",
)

# local imports

urlpatterns = []
urlpatterns += router.urls
