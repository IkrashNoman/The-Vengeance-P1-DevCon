from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import EventAnalytics, ModuleAnalytics, SportAnalytics
from .serializers import (
	EventAnalyticsSerializer,
	ModuleAnalyticsSerializer,
	SportAnalyticsSerializer,
)


class EventAnalyticsViewSet(viewsets.ModelViewSet):
	queryset = EventAnalytics.objects.all()
	serializer_class = EventAnalyticsSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return EventAnalytics.objects.all()
		return EventAnalytics.objects.filter(event__tenant=user.tenant)


class ModuleAnalyticsViewSet(viewsets.ModelViewSet):
	queryset = ModuleAnalytics.objects.all()
	serializer_class = ModuleAnalyticsSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return ModuleAnalytics.objects.all()
		return ModuleAnalytics.objects.filter(module__olympiad__tenant=user.tenant)


class SportAnalyticsViewSet(viewsets.ModelViewSet):
	queryset = SportAnalytics.objects.all()
	serializer_class = SportAnalyticsSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return SportAnalytics.objects.all()
		return SportAnalytics.objects.filter(sport__olympiad__tenant=user.tenant)
