from rest_framework import serializers
from .models import Event, EventAttendance, EventSession


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model."""

    speaker_name = serializers.CharField(source='speaker.get_full_name', read_only=True, allow_null=True)
    venue_name = serializers.CharField(source='venue.name', read_only=True, allow_null=True)
    olympiad_name = serializers.CharField(source='olympiad.name', read_only=True, allow_null=True)
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'tenant',
            'tenant_name',
            'olympiad',
            'olympiad_name',
            'name',
            'slug',
            'description',
            'content',
            'event_type',
            'start_time',
            'end_time',
            'venue',
            'venue_name',
            'speaker',
            'speaker_name',
            'max_capacity',
            'current_capacity',
            'registration_required',
            'thumbnail',
            'is_published',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'current_capacity', 'created_at', 'updated_at']


class EventDetailSerializer(EventSerializer):
    """Detailed serializer with sessions and analytics."""

    sessions = serializers.SerializerMethodField()
    total_registrations = serializers.SerializerMethodField()
    attendance_rate = serializers.SerializerMethodField()

    class Meta(EventSerializer.Meta):
        fields = EventSerializer.Meta.fields + [
            'sessions',
            'total_registrations',
            'attendance_rate',
        ]

    def get_sessions(self, obj):
        sessions = obj.sessions.all()
        return EventSessionSerializer(sessions, many=True).data

    def get_total_registrations(self, obj):
        return obj.attendances.filter(status='registered').count()

    def get_attendance_rate(self, obj):
        total = obj.attendances.count()
        if total == 0:
            return 0
        attended = obj.attendances.filter(status='checked_in').count()
        return round((attended / total) * 100, 2)


class EventSessionSerializer(serializers.ModelSerializer):
    """Serializer for EventSession model."""

    event_name = serializers.CharField(source='event.name', read_only=True)
    speaker_name = serializers.CharField(source='speaker.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = EventSession
        fields = [
            'id',
            'event',
            'event_name',
            'name',
            'description',
            'start_time',
            'end_time',
            'room',
            'speaker',
            'speaker_name',
            'max_capacity',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class EventAttendanceSerializer(serializers.ModelSerializer):
    """Serializer for EventAttendance model."""

    event_name = serializers.CharField(source='event.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = EventAttendance
        fields = [
            'id',
            'event',
            'event_name',
            'user',
            'user_email',
            'user_name',
            'status',
            'check_in_time',
            'check_in_method',
            'registered_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'registered_at', 'updated_at']


class EventCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating events."""

    class Meta:
        model = Event
        fields = [
            'tenant',
            'olympiad',
            'name',
            'description',
            'content',
            'event_type',
            'start_time',
            'end_time',
            'venue',
            'speaker',
            'max_capacity',
            'registration_required',
            'thumbnail',
        ]
