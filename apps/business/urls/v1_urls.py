"""
urls file
"""
from apps.business.views.business import BusinessViewSet
# third party imports
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r"business", BusinessViewSet, basename="business")


# local imports

urlpatterns = [] + router.urls
