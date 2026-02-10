from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Module, ModuleRound, Judge, RoundJudge
from .serializers import (
    ModuleSerializer,
    ModuleDetailSerializer,
    ModuleRoundSerializer,
    JudgeSerializer,
)
from core_permissions import CanManageEvents


class ModuleViewSet(viewsets.ModelViewSet):
    """ViewSet for managing modules."""

    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ModuleDetailSerializer
        return ModuleSerializer

    def get_queryset(self):
        olympiad_id = self.request.query_params.get('olympiad')
        if olympiad_id:
            return Module.objects.filter(olympiad_id=olympiad_id, is_active=True)
        return Module.objects.filter(is_active=True)


class ModuleRoundViewSet(viewsets.ModelViewSet):
    """ViewSet for managing module rounds."""

    queryset = ModuleRound.objects.all()
    serializer_class = ModuleRoundSerializer
    permission_classes = [IsAuthenticated]


class JudgeViewSet(viewsets.ModelViewSet):
    """ViewSet for managing judges."""

    queryset = Judge.objects.all()
    serializer_class = JudgeSerializer
    permission_classes = [IsAuthenticated, CanManageEvents]
