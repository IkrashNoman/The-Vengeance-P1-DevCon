from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SportViewSet, SportMatchViewSet

router = DefaultRouter()
router.register(r'', SportViewSet, basename='sport')
router.register(r'matches', SportMatchViewSet, basename='sport-match')

urlpatterns = [
    path('', include(router.urls)),
]

