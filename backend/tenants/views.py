from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Tenant
from .serializers import TenantSerializer, TenantDetailSerializer, TenantCreateSerializer
from core_permissions import IsSuperAdmin, IsTenantMember, IsOwner


class TenantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tenants (organizations/olympiads).
    """

    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TenantDetailSerializer
        elif self.action == 'create':
            return TenantCreateSerializer
        return TenantSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated()]
        elif self.action == 'retrieve':
            return [IsAuthenticated(), IsTenantMember()]
        elif self.action in ['create']:
            return [IsSuperAdmin()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsOwner()]
        elif self.action == 'destroy':
            return [IsSuperAdmin()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        """List tenants - filter based on user role."""
        if not request.user.is_super_admin():
            if request.user.tenant:
                self.queryset = self.queryset.filter(id=request.user.tenant.id)
            else:
                self.queryset = self.queryset.filter(owner=request.user)
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get tenant statistics."""
        tenant = self.get_object()
        return Response({
            'total_users': tenant.users.count(),
            'total_events': tenant.events.count(),
            'total_departments': tenant.departments.count(),
            'total_registrations': tenant.users.filter(
                registrations__status='confirmed'
            ).count(),
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwner])
    def invite_user(self, request, pk=None):
        """Invite user to tenant."""
        tenant = self.get_object()
        email = request.data.get('email')
        role = request.data.get('role', 'attendee')

        from accounts.models import User
        try:
            user = User.objects.get(email=email)
            user.tenant = tenant
            user.role = role
            user.save()
            return Response({'message': 'User invited successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
