from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import NotificationTemplate, Notification
from .serializers import (
	NotificationTemplateSerializer,
	NotificationSerializer,
)


class NotificationTemplateViewSet(viewsets.ModelViewSet):
	queryset = NotificationTemplate.objects.all()
	serializer_class = NotificationTemplateSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return NotificationTemplate.objects.all()
		return NotificationTemplate.objects.filter(is_active=True)


class NotificationViewSet(viewsets.ModelViewSet):
	queryset = Notification.objects.all()
	serializer_class = NotificationSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return Notification.objects.all()
		return Notification.objects.filter(recipient=user)
