from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import ChatbotKnowledgeBase, ChatbotConversation
from .serializers import (
	ChatbotKnowledgeBaseSerializer,
	ChatbotConversationSerializer,
)


class ChatbotKnowledgeBaseViewSet(viewsets.ModelViewSet):
	queryset = ChatbotKnowledgeBase.objects.all()
	serializer_class = ChatbotKnowledgeBaseSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return ChatbotKnowledgeBase.objects.all()
		if user.tenant:
			return ChatbotKnowledgeBase.objects.filter(tenant=user.tenant)
		return ChatbotKnowledgeBase.objects.none()


class ChatbotConversationViewSet(viewsets.ModelViewSet):
	queryset = ChatbotConversation.objects.all()
	serializer_class = ChatbotConversationSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_super_admin():
			return ChatbotConversation.objects.all()
		return ChatbotConversation.objects.filter(user=user)
