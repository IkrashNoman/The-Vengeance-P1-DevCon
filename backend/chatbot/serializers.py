from rest_framework import serializers
from .models import ChatbotKnowledgeBase, ChatbotConversation, ChatbotMessage, ChatbotIntentResponse


class ChatbotKnowledgeBaseSerializer(serializers.ModelSerializer):
    """Serializer for ChatbotKnowledgeBase model."""

    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    olympiad_name = serializers.CharField(source='olympiad.name', read_only=True, allow_null=True)

    class Meta:
        model = ChatbotKnowledgeBase
        fields = [
            'id',
            'tenant',
            'tenant_name',
            'olympiad',
            'olympiad_name',
            'title',
            'content',
            'category',
            'tags',
            'is_published',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ChatbotMessageSerializer(serializers.ModelSerializer):
    """Serializer for ChatbotMessage model."""

    class Meta:
        model = ChatbotMessage
        fields = [
            'id',
            'conversation',
            'message_type',
            'content',
            'confidence_score',
            'retrieved_documents',
            'is_helpful',
            'feedback_text',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class ChatbotConversationSerializer(serializers.ModelSerializer):
    """Serializer for ChatbotConversation model."""

    user_email = serializers.CharField(source='user.email', read_only=True)
    olympiad_name = serializers.CharField(source='olympiad.name', read_only=True, allow_null=True)
    messages = ChatbotMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatbotConversation
        fields = [
            'id',
            'user',
            'user_email',
            'olympiad',
            'olympiad_name',
            'session_id',
            'summary',
            'sentiment',
            'message_count',
            'resolution_status',
            'messages',
            'created_at',
            'updated_at',
            'closed_at',
        ]
        read_only_fields = ['id', 'session_id', 'created_at', 'updated_at', 'closed_at', 'messages']


class ChatbotIntentResponseSerializer(serializers.ModelSerializer):
    """Serializer for ChatbotIntentResponse model."""

    olympiad_name = serializers.CharField(source='olympiad.name', read_only=True)

    class Meta:
        model = ChatbotIntentResponse
        fields = [
            'id',
            'olympiad',
            'olympiad_name',
            'intent',
            'keywords',
            'response_template',
            'context_required',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ChatbotMessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating chatbot messages."""

    class Meta:
        model = ChatbotMessage
        fields = [
            'conversation',
            'message_type',
            'content',
            'confidence_score',
            'retrieved_documents',
        ]
