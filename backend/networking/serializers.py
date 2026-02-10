from rest_framework import serializers
from .models import (
    NetworkProfile,
    Connection,
    RecommendedConnection,
    Message,
    DigitalCard,
    CardExchange,
)


class NetworkProfileSerializer(serializers.ModelSerializer):
    """Serializer for NetworkProfile model."""

    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = NetworkProfile
        fields = [
            'id',
            'user',
            'user_email',
            'user_name',
            'job_title',
            'company',
            'industry',
            'interests',
            'networking_goals',
            'expertise',
            'show_in_discovery',
            'allow_direct_messages',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ConnectionSerializer(serializers.ModelSerializer):
    """Serializer for Connection model."""

    user_from_name = serializers.CharField(source='user_from.get_full_name', read_only=True)
    user_from_email = serializers.CharField(source='user_from.email', read_only=True)
    user_to_name = serializers.CharField(source='user_to.get_full_name', read_only=True)
    user_to_email = serializers.CharField(source='user_to.email', read_only=True)

    class Meta:
        model = Connection
        fields = [
            'id',
            'user_from',
            'user_from_name',
            'user_from_email',
            'user_to',
            'user_to_name',
            'user_to_email',
            'status',
            'message',
            'tags',
            'initiated_at',
            'connected_at',
            'last_interaction',
        ]
        read_only_fields = ['id', 'initiated_at', 'connected_at', 'last_interaction']


class RecommendedConnectionSerializer(serializers.ModelSerializer):
    """Serializer for RecommendedConnection model."""

    recommended_user_name = serializers.CharField(source='recommended_user.get_full_name', read_only=True)
    recommended_user_email = serializers.CharField(source='recommended_user.email', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = RecommendedConnection
        fields = [
            'id',
            'user',
            'user_email',
            'recommended_user',
            'recommended_user_name',
            'recommended_user_email',
            'match_score',
            'reason',
            'was_connected',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""

    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    sender_email = serializers.CharField(source='sender.email', read_only=True)
    receiver_name = serializers.CharField(source='receiver.get_full_name', read_only=True)
    receiver_email = serializers.CharField(source='receiver.email', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'sender_name',
            'sender_email',
            'receiver',
            'receiver_name',
            'receiver_email',
            'content',
            'is_read',
            'read_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'read_at', 'created_at', 'updated_at']


class DigitalCardSerializer(serializers.ModelSerializer):
    """Serializer for DigitalCard model."""

    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = DigitalCard
        fields = [
            'id',
            'user',
            'user_email',
            'user_name',
            'card_data',
            'qr_code',
            'template_style',
            'custom_colors',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'qr_code', 'created_at', 'updated_at']


class CardExchangeSerializer(serializers.ModelSerializer):
    """Serializer for CardExchange model."""

    user_a_name = serializers.CharField(source='user_a.get_full_name', read_only=True)
    user_a_email = serializers.CharField(source='user_a.email', read_only=True)
    user_b_name = serializers.CharField(source='user_b.get_full_name', read_only=True)
    user_b_email = serializers.CharField(source='user_b.email', read_only=True)

    class Meta:
        model = CardExchange
        fields = [
            'id',
            'user_a',
            'user_a_name',
            'user_a_email',
            'user_b',
            'user_b_name',
            'user_b_email',
            'exchanged_at',
            'location',
            'notes',
        ]
        read_only_fields = ['id', 'exchanged_at']
