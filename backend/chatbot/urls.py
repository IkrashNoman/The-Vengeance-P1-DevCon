from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatbotKnowledgeBaseViewSet, ChatbotConversationViewSet

router = DefaultRouter()
router.register(r'kb', ChatbotKnowledgeBaseViewSet, basename='chatbot-kb')
router.register(r'conversations', ChatbotConversationViewSet, basename='chatbot-conversation')

urlpatterns = [
    path('', include(router.urls)),
]

