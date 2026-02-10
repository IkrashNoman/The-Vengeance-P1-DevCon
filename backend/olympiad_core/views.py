from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Olympiad, Category
from .serializers import (
    OlympiadSerializer,
    OlympiadDetailSerializer,
    OlympiadCreateSerializer,
    CategorySerializer,
)
from core_permissions import IsSuperAdmin, CanManageEvents


class OlympiadViewSet(viewsets.ModelViewSet):
    """ViewSet for managing olympiads."""

    queryset = Olympiad.objects.all()
    serializer_class = OlympiadSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OlympiadDetailSerializer
        elif self.action == 'create':
            return OlympiadCreateSerializer
        return OlympiadSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin():
            return Olympiad.objects.filter(is_active=True)
        if user.tenant:
            return Olympiad.objects.filter(tenant=user.tenant, is_active=True)
        return Olympiad.objects.filter(is_published=True)

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), CanManageEvents()]
        return [IsAuthenticated()]


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for managing categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        olympiad_id = self.request.query_params.get('olympiad')
        if olympiad_id:
            return Category.objects.filter(olympiad_id=olympiad_id)
        return Category.objects.all()
