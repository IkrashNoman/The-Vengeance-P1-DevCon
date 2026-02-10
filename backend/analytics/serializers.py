from rest_framework import serializers
from .models import (
    EventAnalytics,
    ModuleAnalytics,
    SportAnalytics,
    OlympiadAnalytics,
    UserEngagementScore,
    DailyMetrics,
)


class EventAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for EventAnalytics model."""

    event_name = serializers.CharField(source='event.name', read_only=True)

    class Meta:
        model = EventAnalytics
        fields = [
            'id',
            'event',
            'event_name',
            'total_registered',
            'total_attended',
            'no_show_count',
            'average_session_duration',
            'engagement_score',
            'total_polls_created',
            'total_poll_responses',
            'total_qna_questions',
            'total_feedback_responses',
            'connections_made',
            'card_exchanges',
            'demographics_data',
            'overall_sentiment',
            'average_satisfaction_score',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ModuleAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for ModuleAnalytics model."""

    module_name = serializers.CharField(source='module.name', read_only=True)

    class Meta:
        model = ModuleAnalytics
        fields = [
            'id',
            'module',
            'module_name',
            'total_registered_teams',
            'total_registered_members',
            'teams_participated',
            'members_participated',
            'average_team_score',
            'highest_team_score',
            'unique_organizations',
            'gender_distribution',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SportAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for SportAnalytics model."""

    sport_name = serializers.CharField(source='sport.name', read_only=True)

    class Meta:
        model = SportAnalytics
        fields = [
            'id',
            'sport',
            'sport_name',
            'total_registered_teams',
            'total_registered_members',
            'teams_participated',
            'members_participated',
            'total_matches',
            'completed_matches',
            'total_views',
            'unique_organizations',
            'gender_distribution',
            'age_distribution',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class OlympiadAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for OlympiadAnalytics model."""

    olympiad_name = serializers.CharField(source='olympiad.name', read_only=True)

    class Meta:
        model = OlympiadAnalytics
        fields = [
            'id',
            'olympiad',
            'olympiad_name',
            'total_registrations',
            'total_participants',
            'total_events',
            'total_modules',
            'total_sports',
            'total_check_ins',
            'attendance_rate',
            'total_connections',
            'avg_connections_per_user',
            'total_revenue',
            'overall_satisfaction',
            'nps_score',
            'total_unique_organizations',
            'gender_distribution',
            'geographic_distribution',
            'hashtag_mentions',
            'social_engagement_score',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserEngagementScoreSerializer(serializers.ModelSerializer):
    """Serializer for UserEngagementScore model."""

    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = UserEngagementScore
        fields = [
            'id',
            'user',
            'user_email',
            'user_name',
            'base_score',
            'attendance_score',
            'interaction_score',
            'networking_score',
            'learning_score',
            'overall_score',
            'achievements',
            'tier',
            'updated_at',
        ]
        read_only_fields = ['id', 'updated_at']


class DailyMetricsSerializer(serializers.ModelSerializer):
    """Serializer for DailyMetrics model."""

    olympiad_name = serializers.CharField(source='olympiad.name', read_only=True)

    class Meta:
        model = DailyMetrics
        fields = [
            'id',
            'date',
            'olympiad',
            'olympiad_name',
            'new_registrations',
            'daily_active_users',
            'sessions_attended',
            'polls_created',
            'qna_questions',
            'messages_sent',
            'connections_made',
            'daily_revenue',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
