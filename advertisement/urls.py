from django.urls import include, path
from rest_framework.routers import DefaultRouter

from advertisement.views import AdvertisementViewSet

router = DefaultRouter()
router.register(r'', AdvertisementViewSet, basename='advertisement')

urlpatterns = [
    path('', include(router.urls)),
]