from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Society, SocietyMember
from .serializers import (
	SocietySerializer,
	SocietyDetailSerializer,
	SocietyCreateSerializer,
	SocietyMemberSerializer,
	SocietyMemberCreateSerializer,
)
from core_permissions import IsSuperAdmin


class SocietyViewSet(viewsets.ModelViewSet):
	queryset = Society.objects.all()
	serializer_class = SocietySerializer
	permission_classes = [IsAuthenticated]

	def get_serializer_class(self):
		if self.action == 'retrieve':
			return SocietyDetailSerializer
		elif self.action == 'create':
			return SocietyCreateSerializer
		return SocietySerializer

	def get_queryset(self):
		user = self.request.user
		if hasattr(user, 'is_super_admin') and user.is_super_admin():
			return Society.objects.all()
		if getattr(user, 'tenant', None):
			return Society.objects.filter(tenant=user.tenant, is_active=True)
		return Society.objects.filter(is_active=True)


class SocietyMemberViewSet(viewsets.ModelViewSet):
	queryset = SocietyMember.objects.all()
	serializer_class = SocietyMemberSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if hasattr(user, 'is_super_admin') and user.is_super_admin():
			return SocietyMember.objects.all()
		return SocietyMember.objects.filter(society__tenant=getattr(user, 'tenant', None))
