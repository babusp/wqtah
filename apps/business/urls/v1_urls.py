"""
urls file
"""
# third party imports
from rest_framework import routers
from apps.business.views.extra_views import AmenityViewSet, CategoryViewSet, SubCategoryViewSet, AddAttachmentView
from apps.business.views.business import BusinessProfileViewSet, ServiceViewSet

router = routers.DefaultRouter()

router.register(r"business", BusinessProfileViewSet, basename="business")
router.register(r"amenities", AmenityViewSet, basename="amenities")
router.register(r"category", CategoryViewSet, basename="category")
router.register(r"sub-category", SubCategoryViewSet, basename="sub_category")
router.register(r"service", ServiceViewSet, basename="service")
router.register(r"business-attachments", AddAttachmentView, basename="attachments")

# local imports

urlpatterns = []
urlpatterns += router.urls
