"""
Comprehensive Organizer Dashboard and Event Management API
Handles all organizer endpoints including dashboard, events, and analytics
"""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.db.models import Q, Sum, Count, F, Avg
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta

from events.models import Event, EventAttendance, TicketType, EventSession
from registrations.models import Registration
from notifications.models import Notification
from networking.models import NetworkProfile, RecommendedConnection
from chatbot.models import ChatbotConversation


class OrganizerDashboardView(APIView):
    """
    GET /api/organizer/dashboard
    Returns comprehensive dashboard data for organizer
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get organizer dashboard data with metrics and analytics"""
        user = request.user
        
        # Get user's events
        events_qs = Event.objects.all()
        if not user.is_super_admin() and user.tenant:
            events_qs = events_qs.filter(tenant=user.tenant)
        
        # Calculate metrics
        total_events = events_qs.count()
        
        # Get all registrations for organizer's events
        registrations_qs = Registration.objects.filter(
            event__in=events_qs
        )
        total_registrations = registrations_qs.count()
        paid_registrations = registrations_qs.filter(payment_status='paid')
        total_revenue = paid_registrations.aggregate(
            total=Sum('amount_paid')
        )['total'] or 0
        
        # Count sessions
        total_sessions = EventSession.objects.filter(
            event__in=events_qs
        ).count()
        
        # Calculate engagement score (0-100)
        checked_in = EventAttendance.objects.filter(
            event__in=events_qs,
            status='checked_in'
        ).count()
        engagement_score = int((checked_in / total_registrations * 100)) if total_registrations > 0 else 0
        
        # Get registration trends (last 5 months)
        now = timezone.now()
        registrations_by_month = []
        labels = []
        for i in range(4, -1, -1):
            month_start = now - timedelta(days=30 * (i + 1))
            month_end = now - timedelta(days=30 * i)
            count = registrations_qs.filter(
                created_at__gte=month_start,
                created_at__lt=month_end
            ).count()
            registrations_by_month.append(count)
            labels.append(month_start.strftime("%b"))
        
        # Get ticket sales distribution
        ticket_types = TicketType.objects.filter(event__in=events_qs)
        ticket_labels = []
        ticket_data = []
        for ticket in ticket_types[:10]:
            ticket_labels.append(ticket.name)
            ticket_data.append(ticket.quantity_sold)
        
        # Get session attendance data (4x4 matrix)
        sessions = EventSession.objects.filter(event__in=events_qs)[:4]
        session_attendance = []
        for session in sessions:
            attendance_data = []
            for i in range(4):
                # Mock attendance distribution across time slots
                attendance = EventAttendance.objects.filter(
                    event=session.event,
                    status='checked_in'
                ).count() // 4
                attendance_data.append(attendance)
            session_attendance.append(attendance_data)
        
        # Get recent notifications
        notifications = Notification.objects.filter(
            recipient__tenant=user.tenant if not user.is_super_admin() else Q()
        ).order_by('-created_at')[:5]
        
        notification_list = []
        for notif in notifications:
            notification_list.append({
                'id': notif.id,
                'type': 'warning' if 'error' in notif.message.lower() else 'info',
                'message': notif.message
            })
        
        return Response({
            'events': total_events,
            'registrations': total_registrations,
            'revenue': float(total_revenue),
            'sessions': total_sessions,
            'engagementScore': engagement_score,
            'registrationTrends': {
                'labels': labels,
                'data': registrations_by_month
            },
            'ticketSales': {
                'labels': ticket_labels,
                'data': ticket_data
            },
            'sessionAttendance': session_attendance,
            'notifications': notification_list
        }, status=status.HTTP_200_OK)


class OrganizerEventsView(APIView):
    """
    Handle organizer event management
    GET /api/organizer/events - List all events
    POST /api/organizer/events - Create new event
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get all organizer's events with full details"""
        user = request.user
        
        # Get user's events
        events_qs = Event.objects.all()
        if not user.is_super_admin() and user.tenant:
            events_qs = events_qs.filter(tenant=user.tenant)
        
        events_data = []
        for event in events_qs:
            # Get ticket types
            ticket_types = []
            for ticket in event.ticket_types.all():
                ticket_types.append({
                    'type': ticket.name,
                    'price': float(ticket.price),
                    'sold': ticket.quantity_sold
                })
            
            # Get sessions
            sessions = []
            for session in event.sessions.all():
                sessions.append({
                    'id': session.id,
                    'title': session.name,
                    'speaker': session.speaker.get_full_name() if session.speaker else 'TBA',
                    'time': session.start_time.strftime('%H:%M') if session.start_time else 'TBA'
                })
            
            # Get attendees
            attendees = []
            for attendance in event.attendances.all():
                attendees.append({
                    'id': attendance.user.id,
                    'name': attendance.user.get_full_name(),
                    'email': attendance.user.email,
                    'checkedIn': attendance.status == 'checked_in'
                })
            
            events_data.append({
                'id': event.id,
                'name': event.name,
                'description': event.description,
                'startDate': event.start_time.strftime('%Y-%m-%d') if event.start_time else None,
                'endDate': event.end_time.strftime('%Y-%m-%d') if event.end_time else None,
                'venue': event.venue.name if event.venue else 'TBA',
                'ticketTypes': ticket_types,
                'sessions': sessions,
                'attendees': attendees
            })
        
        return Response(events_data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create new event with sessions and ticket types"""
        user = request.user
        
        # Verify permissions
        if not user.is_super_admin() and not user.tenant:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get tenant
        tenant = user.tenant if not user.is_super_admin() else request.data.get('tenant_id')
        
        # Create event
        event = Event.objects.create(
            tenant_id=tenant,
            name=request.data.get('name'),
            description=request.data.get('description', ''),
            event_type=request.data.get('event_type', 'workshop'),
            start_time=request.data.get('startDate'),
            end_time=request.data.get('endDate'),
            is_published=True
        )
        
        # Create ticket types
        for ticket in request.data.get('ticketTypes', []):
            TicketType.objects.create(
                event=event,
                name=ticket.get('type'),
                price=ticket.get('price', 0),
                quantity_available=ticket.get('quantity', 100)
            )
        
        # Create sessions
        for session_data in request.data.get('sessions', []):
            EventSession.objects.create(
                event=event,
                name=session_data.get('title'),
                start_time=session_data.get('start_time'),
                end_time=session_data.get('end_time'),
                room=session_data.get('room', '')
            )
        
        return Response({
            'id': event.id,
            'message': 'Event created successfully'
        }, status=status.HTTP_201_CREATED)


class OrganizerEventDetailView(APIView):
    """
    GET /api/organizer/events/:id - Get event details
    PUT /api/organizer/events/:id - Update event
    DELETE /api/organizer/events/:id - Delete event
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        """Get detailed event information"""
        user = request.user
        event = Event.objects.get(id=event_id)
        
        if not user.is_super_admin() and event.tenant != user.tenant:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Build response (same structure as listing)
        ticket_types = []
        for ticket in event.ticket_types.all():
            ticket_types.append({
                'type': ticket.name,
                'price': float(ticket.price),
                'sold': ticket.quantity_sold
            })
        
        sessions = []
        for session in event.sessions.all():
            sessions.append({
                'id': session.id,
                'title': session.name,
                'speaker': session.speaker.get_full_name() if session.speaker else 'TBA',
                'time': session.start_time.strftime('%H:%M') if session.start_time else 'TBA'
            })
        
        attendees = []
        for attendance in event.attendances.all():
            attendees.append({
                'id': attendance.user.id,
                'name': attendance.user.get_full_name(),
                'email': attendance.user.email,
                'checkedIn': attendance.status == 'checked_in'
            })
        
        return Response({
            'id': event.id,
            'name': event.name,
            'description': event.description,
            'startDate': event.start_time.strftime('%Y-%m-%d') if event.start_time else None,
            'endDate': event.end_time.strftime('%Y-%m-%d') if event.end_time else None,
            'venue': event.venue.name if event.venue else 'TBA',
            'ticketTypes': ticket_types,
            'sessions': sessions,
            'attendees': attendees
        }, status=status.HTTP_200_OK)

    def put(self, request, event_id):
        """Update event details"""
        user = request.user
        event = Event.objects.get(id=event_id)
        
        if not user.is_super_admin() and event.tenant != user.tenant:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Update event fields
        event.name = request.data.get('name', event.name)
        event.description = request.data.get('description', event.description)
        event.start_time = request.data.get('startDate', event.start_time)
        event.end_time = request.data.get('endDate', event.end_time)
        event.save()
        
        return Response({
            'message': 'Event updated successfully',
            'id': event.id
        }, status=status.HTTP_200_OK)

    def delete(self, request, event_id):
        """Delete event"""
        user = request.user
        event = Event.objects.get(id=event_id)
        
        if not user.is_super_admin() and event.tenant != user.tenant:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        event.delete()
        return Response({
            'message': 'Event deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


class OrganizerCheckInView(APIView):
    """
    POST /api/organizer/events/:eventId/attendees/:attendeeId/checkin
    Handle attendee check-in
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id, attendee_id):
        """Check in an attendee"""
        user = request.user
        event = Event.objects.get(id=event_id)
        
        if not user.is_super_admin() and event.tenant != user.tenant:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get or create attendance
        attendance, created = EventAttendance.objects.get_or_create(
            event=event,
            user_id=attendee_id
        )
        
        # Update check-in status
        is_checked_in = request.data.get('checkedIn', True)
        attendance.status = 'checked_in' if is_checked_in else 'registered'
        
        if is_checked_in:
            attendance.check_in_time = timezone.now()
            attendance.check_in_method = 'manual'
        else:
            attendance.check_in_time = None
        
        attendance.save()
        
        return Response({
            'message': 'Attendee check-in status updated',
            'status': attendance.status
        }, status=status.HTTP_200_OK)
