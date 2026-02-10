from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EventAttendanceViewSet, EventSessionViewSet

router = DefaultRouter()
router.register(r'', EventViewSet, basename='event')
router.register(r'attendance', EventAttendanceViewSet, basename='event-attendance')
router.register(r'sessions', EventSessionViewSet, basename='event-session')

urlpatterns = [
    path('', include(router.urls)),
]

