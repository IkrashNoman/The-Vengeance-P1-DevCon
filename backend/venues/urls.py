from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VenueViewSet, VenueSpaceViewSet

router = DefaultRouter()
router.register(r'', VenueViewSet, basename='venue')
router.register(r'spaces', VenueSpaceViewSet, basename='venue-space')

urlpatterns = [
    path('', include(router.urls)),
]

