from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NetworkProfileViewSet, ConnectionViewSet, RecommendedConnectionViewSet

router = DefaultRouter()
router.register(r'profiles', NetworkProfileViewSet, basename='network-profile')
router.register(r'connections', ConnectionViewSet, basename='connection')
router.register(r'recommended', RecommendedConnectionViewSet, basename='recommended-connection')

urlpatterns = [
    path('', include(router.urls)),
]

