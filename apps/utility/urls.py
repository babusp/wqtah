"""
utils Urls
"""
# django and third party response
from rest_framework import routers

# local import
from apps.utility.views import LoadFixturesViewSet


router = routers.SimpleRouter()
router.register(r'load-fixtures', LoadFixturesViewSet, basename='load-fixtures')

urlpatterns = [
]
urlpatterns += router.urls
