from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Sport, SportMatch
from .serializers import (
	SportSerializer,
	SportDetailSerializer,
	SportMatchSerializer,
	SportCreateSerializer,
)


class SportViewSet(viewsets.ModelViewSet):
	queryset = Sport.objects.all()
	permission_classes = [IsAuthenticated]

	def get_serializer_class(self):
		if self.action == 'retrieve':
			return SportDetailSerializer
		if self.action in ['create', 'update', 'partial_update']:
			return SportCreateSerializer
		return SportSerializer

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return Sport.objects.all()
		if user.tenant:
			return Sport.objects.filter(olympiad__tenant=user.tenant)
		return Sport.objects.filter(is_published=True)


class SportMatchViewSet(viewsets.ModelViewSet):
	queryset = SportMatch.objects.all()
	serializer_class = SportMatchSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return SportMatch.objects.all()
		if user.tenant:
			return SportMatch.objects.filter(sport__olympiad__tenant=user.tenant)
		return SportMatch.objects.none()
