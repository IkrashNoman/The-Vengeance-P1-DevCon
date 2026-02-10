from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import Event, EventAttendance, EventSession
from .serializers import (
    EventSerializer,
    EventDetailSerializer,
    EventAttendanceSerializer,
    EventSessionSerializer,
)
from core_permissions import CanManageEvents


class EventViewSet(viewsets.ModelViewSet):
    """ViewSet for managing events."""

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventDetailSerializer
        return EventSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin():
            return Event.objects.all()
        if user.tenant:
            return Event.objects.filter(tenant=user.tenant, is_active=True)
        return Event.objects.filter(is_published=True)


class EventAttendanceViewSet(viewsets.ModelViewSet):
    """ViewSet for managing event attendance."""

    queryset = EventAttendance.objects.all()
    serializer_class = EventAttendanceSerializer
    permission_classes = [IsAuthenticated]


class EventSessionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing event sessions."""

    queryset = EventSession.objects.all()
    serializer_class = EventSessionSerializer
    permission_classes = [IsAuthenticated]
