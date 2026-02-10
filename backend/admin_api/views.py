from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.utils.dateformat import DateFormat
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
import csv

from events.models import Event, EventSession, EventAttendance, TicketType
from registrations.models import Registration
from notifications.models import Notification
from accounts.models import User


class AdminEventsView(APIView):
    """GET /api/admin/events - List events with sessions, attendees, and ticket types"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        qs = Event.objects.all()
        if not user.is_super_admin() and user.tenant:
            qs = qs.filter(tenant=user.tenant)

        data = []
        for e in qs.order_by('start_time'):
            # Build session details for each event
            sessions = []
            for session in e.sessions.all():
                # Get attendees for this session
                session_attendees = []
                for attendance in session.event.attendances.filter(status='checked_in'):
                    session_attendees.append({
                        'id': attendance.user.id,
                        'name': attendance.user.get_full_name(),
                        'email': attendance.user.email,
                        'checkedIn': attendance.check_in_time is not None,
                    })
                
                sessions.append({
                    'id': session.id,
                    'title': session.name,
                    'speaker': session.speaker.get_full_name() if session.speaker else 'TBA',
                    'startTime': DateFormat(session.start_time).format('H:i') if session.start_time else 'TBA',
                    'endTime': DateFormat(session.end_time).format('H:i') if session.end_time else 'TBA',
                    'room': session.room or 'TBA',
                    'capacity': session.max_capacity,
                    'attendees': session_attendees,
                })
            
            data.append({
                'id': e.id,
                'name': e.name,
                'sessions': sessions,
            })
        return Response(data)


class AdminNotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        qs = Notification.objects.all().order_by('-created_at')
        if not user.is_super_admin() and user.tenant:
            qs = qs.filter(recipient__tenant=user.tenant)

        data = []
        for n in qs[:20]:
            data.append({'id': n.id, 'msg': n.message})
        return Response(data)


class AdminAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        qs = EventAttendance.objects.all()
        if not user.is_super_admin() and user.tenant:
            qs = qs.filter(event__tenant=user.tenant)

        qs = qs.filter(check_in_time__isnull=False)
        series = (
            qs.annotate(date=TruncDate('check_in_time'))
            .values('date')
            .annotate(attendees=Count('id'))
            .order_by('date')
        )
        data = []
        for r in series:
            data.append({'date': r['date'].isoformat(), 'attendees': r['attendees']})
        return Response(data)


class AdminRevenueView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        qs = Registration.objects.filter(payment_status='paid')
        if not user.is_super_admin() and user.tenant:
            qs = qs.filter(user__tenant=user.tenant)

        series = (
            qs.values('event__name')
            .annotate(revenue=Sum('amount_paid'))
            .order_by('-revenue')
        )
        data = []
        for r in series:
            data.append({'event': r['event__name'], 'revenue': float(r['revenue'] or 0)})
        return Response(data)


class AdminEventDetailViewSet(viewsets.ModelViewSet):
    """
    ViewSet for detailed event management with nested sessions, attendees, and ticket types.
    Supports GET (list, retrieve), POST (create), PUT (update), DELETE.
    Endpoints: GET /api/admin/events/:id, POST /api/admin/events, etc.
    """
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Event.objects.all()
        if not user.is_super_admin() and user.tenant:
            qs = qs.filter(tenant=user.tenant)
        return qs

    def retrieve(self, request, *args, **kwargs):
        """GET /api/admin/events/:id - Get detailed event with sessions, attendees, ticket types"""
        event = self.get_object()
        data = self._build_event_detail(event)
        return Response(data)

    def create(self, request, *args, **kwargs):
        """POST /api/admin/events - Create new event with nested data"""
        user = request.user
        if not user.is_super_admin() and not (hasattr(user, 'permissions') and user.permissions.can_manage_events):
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        tenant_id = user.tenant.id if not user.is_super_admin() else request.data.get('tenant')
        if not tenant_id:
            return Response({'error': 'Tenant required'}, status=status.HTTP_400_BAD_REQUEST)

        event_data = {
            'tenant_id': tenant_id,
            'name': request.data.get('name'),
            'description': request.data.get('description', ''),
            'event_type': request.data.get('event_type', 'workshop'),
            'start_time': request.data.get('startDate'),
            'end_time': request.data.get('endDate'),
            'is_published': True,
        }
        event = Event.objects.create(**event_data)

        # Create ticket types
        for ticket in request.data.get('ticketTypes', []):
            TicketType.objects.create(
                event=event,
                name=ticket.get('type'),
                price=ticket.get('price', 0),
                quantity_available=ticket.get('quantity', 100),
                quantity_sold=ticket.get('sold', 0),
            )

        return Response(self._build_event_detail(event), status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """PUT /api/admin/events/:id - Update event and nested data"""
        event = self.get_object()
        event.name = request.data.get('name', event.name)
        event.description = request.data.get('description', event.description)
        event.start_time = request.data.get('startDate', event.start_time)
        event.end_time = request.data.get('endDate', event.end_time)
        event.save()

        # Update ticket types
        if 'ticketTypes' in request.data:
            event.ticket_types.all().delete()
            for ticket in request.data.get('ticketTypes', []):
                TicketType.objects.create(
                    event=event,
                    name=ticket.get('type'),
                    price=ticket.get('price', 0),
                    quantity_available=ticket.get('quantity', 100),
                    quantity_sold=ticket.get('sold', 0),
                )

        return Response(self._build_event_detail(event), status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """DELETE /api/admin/events/:id - Delete event"""
        event = self.get_object()
        event.delete()
        return Response({'message': 'Event deleted'}, status=status.HTTP_204_NO_CONTENT)

    def _build_event_detail(self, event):
        """
        Build detailed event response with nested sessions, attendees, and ticket types.
        """
        sessions = []
        for session in event.sessions.all():
            sessions.append({
                'id': session.id,
                'title': session.name,
                'speaker': session.speaker.get_full_name() if session.speaker else 'TBA',
                'time': DateFormat(session.start_time).format('g:i A') if session.start_time else 'TBA',
            })

        attendees = []
        for attendance in event.attendances.filter(status='checked_in'):
            attendees.append({
                'id': attendance.user.id,
                'name': attendance.user.get_full_name(),
                'email': attendance.user.email,
                'checkedIn': attendance.check_in_time is not None,
            })

        ticket_types = []
        for ticket in event.ticket_types.all():
            ticket_types.append({
                'type': ticket.name,
                'price': float(ticket.price),
                'sold': ticket.quantity_sold,
            })

        return {
            'id': event.id,
            'name': event.name,
            'description': event.description,
            'startDate': DateFormat(event.start_time).format('Y-m-d') if event.start_time else None,
            'endDate': DateFormat(event.end_time).format('Y-m-d') if event.end_time else None,
            'venue': event.venue.name if event.venue else 'TBA',
            'ticketTypes': ticket_types,
            'sessions': sessions,
            'attendees': attendees,
        }


class AdminSessionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing sessions within events.
    Supports POST (create), PUT (update), DELETE operations on sessions.
    Endpoints: POST /api/admin/events/:eventId/sessions
               PUT /api/admin/events/:eventId/sessions/:sessionId
               DELETE /api/admin/events/:eventId/sessions/:sessionId
    """
    queryset = EventSession.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        event_id = self.kwargs.get('event_id')
        qs = EventSession.objects.filter(event_id=event_id)
        if not user.is_super_admin() and user.tenant:
            qs = qs.filter(event__tenant=user.tenant)
        return qs

    def create(self, request, event_id=None):
        """POST /api/admin/events/:eventId/sessions - Create new session"""
        user = request.user
        if not user.is_super_admin() and not (hasattr(user, 'permissions') and user.permissions.can_manage_events):
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        event = get_object_or_404(Event, id=event_id)
        if not user.is_super_admin() and event.tenant != user.tenant:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        session_data = {
            'event': event,
            'name': request.data.get('title'),
            'description': request.data.get('description', ''),
            'start_time': request.data.get('startTime'),
            'end_time': request.data.get('endTime'),
            'room': request.data.get('room', ''),
            'max_capacity': request.data.get('capacity', 50),
            'is_active': True,
        }
        session = EventSession.objects.create(**session_data)
        return Response(self._format_session(session), status=status.HTTP_201_CREATED)

    def update(self, request, event_id=None, pk=None):
        """PUT /api/admin/events/:eventId/sessions/:sessionId - Update session"""
        session = get_object_or_404(EventSession, id=pk, event_id=event_id)
        user = request.user
        if not user.is_super_admin() and session.event.tenant != user.tenant:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        session.name = request.data.get('title', session.name)
        session.description = request.data.get('description', session.description)
        session.start_time = request.data.get('startTime', session.start_time)
        session.end_time = request.data.get('endTime', session.end_time)
        session.room = request.data.get('room', session.room)
        session.max_capacity = request.data.get('capacity', session.max_capacity)
        session.save()
        return Response(self._format_session(session), status=status.HTTP_200_OK)

    def destroy(self, request, event_id=None, pk=None):
        """DELETE /api/admin/events/:eventId/sessions/:sessionId - Delete session"""
        session = get_object_or_404(EventSession, id=pk, event_id=event_id)
        user = request.user
        if not user.is_super_admin() and session.event.tenant != user.tenant:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        session.delete()
        return Response({'message': 'Session deleted'}, status=status.HTTP_204_NO_CONTENT)

    def _format_session(self, session):
        """Format session response"""
        return {
            'id': session.id,
            'title': session.name,
            'speaker': session.speaker.get_full_name() if session.speaker else 'TBA',
            'startTime': DateFormat(session.start_time).format('H:i') if session.start_time else 'TBA',
            'endTime': DateFormat(session.end_time).format('H:i') if session.end_time else 'TBA',
            'room': session.room or 'TBA',
            'capacity': session.max_capacity,
        }


class AdminSessionAttendeeViewSet(viewsets.ViewSet):
    """
    ViewSet for exporting attendees of a specific session.
    Endpoints: GET /api/admin/events/:eventId/sessions/:sessionId/attendees
    """
    permission_classes = [IsAuthenticated]

    def list(self, request, event_id=None, session_id=None):
        """GET /api/admin/events/:eventId/sessions/:sessionId/attendees - Export attendees"""
        user = request.user
        session = get_object_or_404(EventSession, id=session_id, event_id=event_id)
        
        if not user.is_super_admin() and session.event.tenant != user.tenant:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        # Get attendees for this session's event
        attendees = []
        for attendance in session.event.attendances.filter(status='checked_in'):
            attendees.append({
                'id': attendance.user.id,
                'name': attendance.user.get_full_name(),
                'email': attendance.user.email,
                'checkedIn': attendance.check_in_time is not None,
            })

        return Response(attendees)


class QRCheckInView(APIView):
    """PUT /api/admin/events/:eventId/attendees/:attendeeId/checkin - Handle QR check-in"""
    permission_classes = [IsAuthenticated]

    def put(self, request, event_id=None, attendee_id=None):
        """Handle QR code check-in"""
        user = request.user
        
        # Get event and validate permissions
        event = get_object_or_404(Event, id=event_id)
        if not user.is_super_admin() and event.tenant != user.tenant:
            return Response(
                {'success': False, 'message': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get or create attendance record
        try:
            attendance = EventAttendance.objects.get(event=event, user_id=attendee_id)
        except EventAttendance.DoesNotExist:
            return Response(
                {'success': False, 'message': 'Attendee not found for this event'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Update check-in status
        checked_in = request.data.get('checkedIn', True)
        
        if checked_in:
            attendance.status = 'checked_in'
            attendance.check_in_time = timezone.now()
            attendance.check_in_method = 'qr'
        else:
            attendance.status = 'registered'
            attendance.check_in_time = None
            attendance.check_in_method = None
        
        attendance.save()
        
        return Response(
            {
                'success': True,
                'message': 'Attendee check-in updated successfully',
                'data': {
                    'attendeeId': attendance.user.id,
                    'eventId': event.id,
                    'status': attendance.status,
                    'checkInTime': attendance.check_in_time.isoformat() if attendance.check_in_time else None
                }
            },
            status=status.HTTP_200_OK
        )


class TicketsView(APIView):
    """Handle ticket endpoints for events"""
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id=None):
        """GET /api/admin/events/:eventId/tickets - Get all tickets for an event"""
        user = request.user
        event = get_object_or_404(Event, id=event_id)
        
        if not user.is_super_admin() and event.tenant != user.tenant:
            return Response(
                {'success': False, 'message': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        tickets = []
        for ticket in event.ticket_types.all():
            tickets.append({
                'id': ticket.id,
                'type': ticket.name,
                'price': float(ticket.price),
                'earlyBirdPrice': float(ticket.early_bird_price) if ticket.early_bird_price else None,
                'groupDiscount': ticket.group_discount or '',
                'sold': ticket.quantity_sold,
                'revenue': ticket.revenue,
            })
        
        return Response({
            'eventId': event.id,
            'tickets': tickets
        }, status=status.HTTP_200_OK)

    def post(self, request, event_id=None):
        """POST /api/events/:eventId/tickets - Create or update tickets for an event"""
        user = request.user
        event = get_object_or_404(Event, id=event_id)
        
        if not user.is_super_admin() and event.tenant != user.tenant:
            return Response(
                {'success': False, 'message': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        tickets_data = request.data if isinstance(request.data, list) else request.data.get('tickets', [])
        created_tickets = []
        
        for ticket_info in tickets_data:
            ticket = TicketType.objects.create(
                event=event,
                name=ticket_info.get('type'),
                price=ticket_info.get('price', 0),
                early_bird_price=ticket_info.get('earlyBirdPrice'),
                group_discount=ticket_info.get('groupDiscount', ''),
                quantity_available=ticket_info.get('quantity', 100),
                quantity_sold=ticket_info.get('sold', 0),
            )
            created_tickets.append({
                'id': ticket.id,
                'type': ticket.name,
                'price': float(ticket.price),
                'earlyBirdPrice': float(ticket.early_bird_price) if ticket.early_bird_price else None,
                'groupDiscount': ticket.group_discount,
                'sold': ticket.quantity_sold,
                'revenue': ticket.revenue,
            })
        
        return Response({
            'success': True,
            'message': 'Tickets updated successfully',
            'tickets': created_tickets
        }, status=status.HTTP_201_CREATED)


class TicketDetailView(APIView):
    """PUT /api/admin/events/:eventId/tickets/:ticketId - Update ticket prices"""
    permission_classes = [IsAuthenticated]

    def put(self, request, event_id=None, ticket_id=None):
        """Update ticket pricing and discount information"""
        user = request.user
        
        # Get event and validate permissions
        event = get_object_or_404(Event, id=event_id)
        if not user.is_super_admin() and event.tenant != user.tenant:
            return Response(
                {'success': False, 'message': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get ticket
        ticket = get_object_or_404(TicketType, id=ticket_id, event=event)
        
        # Update fields
        if 'price' in request.data:
            ticket.price = request.data.get('price')
        if 'earlyBirdPrice' in request.data:
            ticket.early_bird_price = request.data.get('earlyBirdPrice')
        if 'groupDiscount' in request.data:
            ticket.group_discount = request.data.get('groupDiscount')
        
        ticket.save()
        
        return Response({
            'success': True,
            'message': 'Ticket updated successfully',
            'ticket': {
                'id': ticket.id,
                'type': ticket.name,
                'price': float(ticket.price),
                'earlyBirdPrice': float(ticket.early_bird_price) if ticket.early_bird_price else None,
                'groupDiscount': ticket.group_discount,
                'sold': ticket.quantity_sold,
                'revenue': ticket.revenue,
            }
        }, status=status.HTTP_200_OK)


class TicketExportView(APIView):
    """GET /api/admin/events/:eventId/tickets/export - Export tickets to CSV"""
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id=None):
        """Export event tickets to CSV"""
        user = request.user
        event = get_object_or_404(Event, id=event_id)
        
        if not user.is_super_admin() and event.tenant != user.tenant:
            return Response(
                {'success': False, 'message': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="event_{event_id}_tickets.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Ticket ID', 'Type', 'Price', 'Early Bird Price', 'Group Discount', 'Sold', 'Revenue'])
        
        for ticket in event.ticket_types.all():
            writer.writerow([
                ticket.id,
                ticket.name,
                float(ticket.price),
                float(ticket.early_bird_price) if ticket.early_bird_price else '',
                ticket.group_discount,
                ticket.quantity_sold,
                ticket.revenue,
            ])
        
        return response
