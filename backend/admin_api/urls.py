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
    QRCheckInView,
    TicketsView,
    TicketDetailView,
    TicketExportView,
)
from .organizer_views import (
    OrganizerDashboardView,
    OrganizerEventsView,
    OrganizerEventDetailView,
    OrganizerCheckInView,
)

router = DefaultRouter()
router.register(r'events', AdminEventDetailViewSet, basename='admin-event-detail')

urlpatterns = [
    # Organizer Dashboard & Event Management
    path('organizer/dashboard', OrganizerDashboardView.as_view(), name='organizer-dashboard'),
    path('organizer/events', OrganizerEventsView.as_view(), name='organizer-events'),
    path('organizer/events/<int:event_id>', OrganizerEventDetailView.as_view(), name='organizer-event-detail'),
    path('organizer/events/<int:event_id>/attendees/<int:attendee_id>/checkin', OrganizerCheckInView.as_view(), name='organizer-checkin'),
    
    # Enhanced list endpoints (APIView-based) - includes nested sessions
    path('events', AdminEventsView.as_view(), name='admin-events-list'),
    path('notifications', AdminNotificationsView.as_view(), name='admin-notifications'),
    path('attendance', AdminAttendanceView.as_view(), name='admin-attendance'),
    path('revenue', AdminRevenueView.as_view(), name='admin-revenue'),
    
    # Session management (nested under events)
    path('events/<int:event_id>/sessions', AdminSessionViewSet.as_view({'post': 'create'}), name='create-session'),
    path('events/<int:event_id>/sessions/<int:pk>', AdminSessionViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='session-detail'),
    path('events/<int:event_id>/sessions/<int:session_id>/attendees', AdminSessionAttendeeViewSet.as_view({'get': 'list'}), name='session-attendees'),
    
    # QR Check-in endpoint
    path('events/<int:event_id>/attendees/<int:attendee_id>/checkin', QRCheckInView.as_view(), name='qr-checkin'),
    
    # Tickets endpoints
    path('events/<int:event_id>/tickets', TicketsView.as_view(), name='event-tickets'),
    path('events/<int:event_id>/tickets/<int:ticket_id>', TicketDetailView.as_view(), name='ticket-detail'),
    path('events/<int:event_id>/tickets/export', TicketExportView.as_view(), name='tickets-export'),
    
    # Event CRUD endpoints (ViewSet-based)
    path('', include(router.urls)),
]
