from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Department, DepartmentMember
from .serializers import (
    DepartmentSerializer,
    DepartmentDetailSerializer,
    DepartmentCreateSerializer,
    DepartmentMemberSerializer,
)
from core_permissions import IsSuperAdmin


class DepartmentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing departments."""

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DepartmentDetailSerializer
        elif self.action == 'create':
            return DepartmentCreateSerializer
        return DepartmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin():
            return Department.objects.all()
        if user.tenant:
            return Department.objects.filter(tenant=user.tenant)
        return Department.objects.none()

    @action(detail=False, methods=['get'])
    def my_departments(self, request):
        """Get departments for current user."""
        memberships = request.user.department_memberships.filter(is_active=True)
        departments = [m.department for m in memberships]
        serializer = self.get_serializer(departments, many=True)
        return Response(serializer.data)


class DepartmentMemberViewSet(viewsets.ModelViewSet):
    """ViewSet for managing department members."""

    queryset = DepartmentMember.objects.all()
    serializer_class = DepartmentMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin():
            return DepartmentMember.objects.all()
        return DepartmentMember.objects.filter(department__tenant=user.tenant)
