from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Poll, PollResponse, QnA
from .serializers import (
	PollSerializer,
	PollResponseSerializer,
	QnASerializer,
)


class PollViewSet(viewsets.ModelViewSet):
	queryset = Poll.objects.all()
	serializer_class = PollSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return Poll.objects.all()
		if user.tenant:
			return Poll.objects.filter(created_by__tenant=user.tenant)
		return Poll.objects.none()


class PollResponseViewSet(viewsets.ModelViewSet):
	queryset = PollResponse.objects.all()
	serializer_class = PollResponseSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return PollResponse.objects.all()
		return PollResponse.objects.filter(user=user)


class QnAViewSet(viewsets.ModelViewSet):
	queryset = QnA.objects.all()
	serializer_class = QnASerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return QnA.objects.all()
		if user.tenant:
			return QnA.objects.filter(event_session__event__tenant=user.tenant)
		return QnA.objects.none()
