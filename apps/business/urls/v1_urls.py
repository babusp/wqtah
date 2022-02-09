"""
urls file
"""
from apps.business.views.business import (
    BusinessDetailViewSet,
    BusinessViewSet,
    AmeniyViewSet,
)

# third party imports
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r"business", BusinessViewSet, basename="business")
router.register(r"business", BusinessDetailViewSet, basename="business")
router.register(r"amenity", AmeniyViewSet, basename="amenities")


# local imports

urlpatterns = [] + router.urls
