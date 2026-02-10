from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminEventsView,
    AdminNotificationsView,
    AdminAttendanceView,
    AdminRevenueView,
    AdminEventDetailViewSet,
    AdminSessionViewSet,
    AdminSessionAttendeeViewSet,
)

router = DefaultRouter()
router.register(r'events', AdminEventDetailViewSet, basename='admin-event-detail')

urlpatterns = [
    # Enhanced list endpoints (APIView-based) - includes nested sessions
    path('events', AdminEventsView.as_view(), name='admin-events-list'),
    path('notifications', AdminNotificationsView.as_view(), name='admin-notifications'),
    path('attendance', AdminAttendanceView.as_view(), name='admin-attendance'),
    path('revenue', AdminRevenueView.as_view(), name='admin-revenue'),
    
    # Session management (nested under events)
    path('events/<int:event_id>/sessions', AdminSessionViewSet.as_view({'post': 'create'}), name='create-session'),
    path('events/<int:event_id>/sessions/<int:pk>', AdminSessionViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='session-detail'),
    path('events/<int:event_id>/sessions/<int:session_id>/attendees', AdminSessionAttendeeViewSet.as_view({'get': 'list'}), name='session-attendees'),
    
    # Event CRUD endpoints (ViewSet-based)
    path('', include(router.urls)),
]
