from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserActivityLogViewSet,
    SessionRecommendationViewSet,
    ModuleRecommendationViewSet,
)

router = DefaultRouter()
router.register(r'activity', UserActivityLogViewSet, basename='user-activity')
router.register(r'sessions', SessionRecommendationViewSet, basename='session-recommendation')
router.register(r'modules', ModuleRecommendationViewSet, basename='module-recommendation')

urlpatterns = [
    path('', include(router.urls)),
]

