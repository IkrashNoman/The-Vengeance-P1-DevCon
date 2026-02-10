from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import NetworkProfile, Connection, RecommendedConnection
from .serializers import (
	NetworkProfileSerializer,
	ConnectionSerializer,
	RecommendedConnectionSerializer,
)


class NetworkProfileViewSet(viewsets.ModelViewSet):
	queryset = NetworkProfile.objects.all()
	serializer_class = NetworkProfileSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return NetworkProfile.objects.all()
		if user.tenant:
			return NetworkProfile.objects.filter(user__tenant=user.tenant)
		return NetworkProfile.objects.none()


class ConnectionViewSet(viewsets.ModelViewSet):
	queryset = Connection.objects.all()
	serializer_class = ConnectionSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return Connection.objects.all()
		return Connection.objects.filter(user_from=user) | Connection.objects.filter(user_to=user)


class RecommendedConnectionViewSet(viewsets.ModelViewSet):
	queryset = RecommendedConnection.objects.all()
	serializer_class = RecommendedConnectionSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return RecommendedConnection.objects.all()
		return RecommendedConnection.objects.filter(user=user)
