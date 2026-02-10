from rest_framework import serializers
from .models import (
    UserActivityLog,
    SessionRecommendation,
    ModuleRecommendation,
    PersonalizedAgenda,
    RecommendationFeedback,
)


class UserActivityLogSerializer(serializers.ModelSerializer):
    """Serializer for UserActivityLog model."""

    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = UserActivityLog
        fields = [
            'id',
            'user',
            'user_email',
            'activity_type',
            'content_type',
            'object_id',
            'duration_seconds',
            'engagement_score',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class SessionRecommendationSerializer(serializers.ModelSerializer):
    """Serializer for SessionRecommendation model."""

    user_email = serializers.CharField(source='user.email', read_only=True)
    session_name = serializers.CharField(source='session.name', read_only=True)

    class Meta:
        model = SessionRecommendation
        fields = [
            'id',
            'user',
            'user_email',
            'session',
            'session_name',
            'score',
            'reason',
            'was_clicked',
            'was_attended',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class ModuleRecommendationSerializer(serializers.ModelSerializer):
    """Serializer for ModuleRecommendation model."""

    user_email = serializers.CharField(source='user.email', read_only=True)
    module_name = serializers.CharField(source='module.name', read_only=True)

    class Meta:
        model = ModuleRecommendation
        fields = [
            'id',
            'user',
            'user_email',
            'module',
            'module_name',
            'score',
            'reason',
            'was_viewed',
            'was_registered',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class PersonalizedAgendaSerializer(serializers.ModelSerializer):
    """Serializer for PersonalizedAgenda model."""

    user_email = serializers.CharField(source='user.email', read_only=True)
    olympiad_name = serializers.CharField(source='olympiad.name', read_only=True, allow_null=True)

    class Meta:
        model = PersonalizedAgenda
        fields = [
            'id',
            'user',
            'user_email',
            'olympiad',
            'olympiad_name',
            'items',
            'generation_reason',
            'algorithm_version',
            'user_satisfaction',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RecommendationFeedbackSerializer(serializers.ModelSerializer):
    """Serializer for RecommendationFeedback model."""

    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = RecommendationFeedback
        fields = [
            'id',
            'user',
            'user_email',
            'feedback_type',
            'content_type',
            'object_id',
            'relevance_score',
            'comments',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class RecommendationFeedbackCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating recommendation feedback."""

    class Meta:
        model = RecommendationFeedback
        fields = [
            'user',
            'feedback_type',
            'content_type',
            'object_id',
            'relevance_score',
            'comments',
        ]
