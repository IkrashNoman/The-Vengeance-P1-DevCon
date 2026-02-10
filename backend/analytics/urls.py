from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EventAnalyticsViewSet,
    ModuleAnalyticsViewSet,
    SportAnalyticsViewSet,
)

router = DefaultRouter()
router.register(r'events', EventAnalyticsViewSet, basename='event-analytics')
router.register(r'modules', ModuleAnalyticsViewSet, basename='module-analytics')
router.register(r'sports', SportAnalyticsViewSet, basename='sport-analytics')

urlpatterns = [
    path('', include(router.urls)),
]

