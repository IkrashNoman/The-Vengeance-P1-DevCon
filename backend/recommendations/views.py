from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import UserActivityLog, SessionRecommendation, ModuleRecommendation
from .serializers import (
	UserActivityLogSerializer,
	SessionRecommendationSerializer,
	ModuleRecommendationSerializer,
)


class UserActivityLogViewSet(viewsets.ModelViewSet):
	queryset = UserActivityLog.objects.all()
	serializer_class = UserActivityLogSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return UserActivityLog.objects.all()
		return UserActivityLog.objects.filter(user=user)


class SessionRecommendationViewSet(viewsets.ModelViewSet):
	queryset = SessionRecommendation.objects.all()
	serializer_class = SessionRecommendationSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return SessionRecommendation.objects.all()
		return SessionRecommendation.objects.filter(user=user)


class ModuleRecommendationViewSet(viewsets.ModelViewSet):
	queryset = ModuleRecommendation.objects.all()
	serializer_class = ModuleRecommendationSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return ModuleRecommendation.objects.all()
		return ModuleRecommendation.objects.filter(user=user)
