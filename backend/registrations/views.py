from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Registration, Team, TeamMember, RegistrationForm
from .serializers import (
    RegistrationSerializer,
    TeamSerializer,
    TeamDetailSerializer,
    TeamMemberSerializer,
    RegistrationFormSerializer,
)
from core_permissions import IsOwner


class RegistrationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing registrations."""

    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin():
            return Registration.objects.all()
        return Registration.objects.filter(user=user)

    @action(detail=False, methods=['get'])
    def my_registrations(self, request):
        """Get current user registrations."""
        registrations = Registration.objects.filter(user=request.user)
        serializer = self.get_serializer(registrations, many=True)
        return Response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for managing teams."""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TeamDetailSerializer
        return TeamSerializer


class TeamMemberViewSet(viewsets.ModelViewSet):
    """ViewSet for managing team members."""

    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAuthenticated]


class RegistrationFormViewSet(viewsets.ModelViewSet):
    """ViewSet for managing registration forms."""

    queryset = RegistrationForm.objects.all()
    serializer_class = RegistrationFormSerializer
    permission_classes = [IsAuthenticated]
