from rest_framework import serializers
from .models import NotificationTemplate, Notification, NotificationPreference


class NotificationTemplateSerializer(serializers.ModelSerializer):
    """Serializer for NotificationTemplate model."""

    class Meta:
        model = NotificationTemplate
        fields = [
            'id',
            'name',
            'notification_type',
            'title_template',
            'body_template',
            'is_active',
            'can_customize',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model."""

    recipient_email = serializers.CharField(source='recipient.email', read_only=True)
    template_name = serializers.CharField(source='template.name', read_only=True, allow_null=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'recipient',
            'recipient_email',
            'template',
            'template_name',
            'title',
            'message',
            'is_read',
            'read_at',
            'channels',
            'status',
            'content_type',
            'object_id',
            'action_url',
            'action_text',
            'created_at',
            'sent_at',
            'scheduled_for',
        ]
        read_only_fields = ['id', 'created_at', 'sent_at', 'read_at']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for NotificationPreference model."""

    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = NotificationPreference
        fields = [
            'id',
            'user',
            'user_email',
            'email_on_registration',
            'email_on_session_reminder',
            'email_on_announcement',
            'email_on_networking',
            'email_on_feedback',
            'push_enabled',
            'push_on_session_reminder',
            'push_on_announcement',
            'push_on_networking',
            'sms_enabled',
            'sms_for_urgent_only',
            'digest_frequency',
            'quiet_hours_enabled',
            'quiet_hours_start',
            'quiet_hours_end',
            'updated_at',
        ]
        read_only_fields = ['id', 'updated_at']


class NotificationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating notifications."""

    class Meta:
        model = Notification
        fields = [
            'recipient',
            'template',
            'title',
            'message',
            'channels',
            'content_type',
            'object_id',
            'action_url',
            'action_text',
            'scheduled_for',
        ]
