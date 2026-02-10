from rest_framework import serializers
from .models import Module, ModuleRound, Judge, RoundJudge


class ModuleSerializer(serializers.ModelSerializer):
    """Serializer for Module model."""

    olympiad_name = serializers.CharField(source='olympiad.name', read_only=True)
    society_name = serializers.CharField(source='organizing_society.name', read_only=True, allow_null=True)
    days_until_registration_end = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = [
            'id',
            'olympiad',
            'olympiad_name',
            'name',
            'slug',
            'description',
            'module_type',
            'organizing_society',
            'society_name',
            'rules_document',
            'max_participants',
            'min_team_size',
            'max_team_size',
            'participation_fee',
            'event_date',
            'registration_start',
            'registration_end',
            'banner',
            'is_published',
            'is_active',
            'days_until_registration_end',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']

    def get_days_until_registration_end(self, obj):
        from datetime import datetime
        from django.utils import timezone
        now = timezone.now()
        delta = obj.registration_end - now
        return max(delta.days, 0)


class ModuleDetailSerializer(ModuleSerializer):
    """Detailed serializer with rounds and registrations."""

    rounds = serializers.SerializerMethodField()
    total_registrations = serializers.SerializerMethodField()
    collaborating_societies = serializers.SerializerMethodField()

    class Meta(ModuleSerializer.Meta):
        fields = ModuleSerializer.Meta.fields + [
            'rounds',
            'total_registrations',
            'collaborating_societies',
        ]

    def get_rounds(self, obj):
        rounds = obj.rounds.all().order_by('order')
        return ModuleRoundSerializer(rounds, many=True).data

    def get_total_registrations(self, obj):
        from registrations.models import Registration
        return Registration.objects.filter(
            module=obj,
            status='confirmed'
        ).count()

    def get_collaborating_societies(self, obj):
        from societies.serializers import SocietySerializer
        societies = obj.collaborating_societies.all()
        return SocietySerializer(societies, many=True).data


class ModuleRoundSerializer(serializers.ModelSerializer):
    """Serializer for ModuleRound model."""

    module_name = serializers.CharField(source='module.name', read_only=True)
    venue_name = serializers.CharField(source='venue.name', read_only=True, allow_null=True)
    judges = serializers.SerializerMethodField()

    class Meta:
        model = ModuleRound
        fields = [
            'id',
            'module',
            'module_name',
            'name',
            'round_type',
            'description',
            'start_time',
            'end_time',
            'venue',
            'venue_name',
            'max_advancement',
            'is_active',
            'order',
            'judges',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'judges']

    def get_judges(self, obj):
        judges = obj.judges.all()
        return RoundJudgeSerializer(judges, many=True).data


class JudgeSerializer(serializers.ModelSerializer):
    """Serializer for Judge model."""

    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Judge
        fields = [
            'id',
            'user',
            'user_email',
            'user_name',
            'expertise',
            'bio',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class RoundJudgeSerializer(serializers.ModelSerializer):
    """Serializer for RoundJudge model."""

    judge_name = serializers.CharField(source='judge.user.get_full_name', read_only=True)
    judge_email = serializers.CharField(source='judge.user.email', read_only=True)

    class Meta:
        model = RoundJudge
        fields = [
            'id',
            'round',
            'judge',
            'judge_name',
            'judge_email',
            'assigned_at',
        ]
        read_only_fields = ['id', 'assigned_at']


class ModuleCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating modules."""

    class Meta:
        model = Module
        fields = [
            'olympiad',
            'name',
            'description',
            'module_type',
            'organizing_society',
            'rules_document',
            'max_participants',
            'min_team_size',
            'max_team_size',
            'participation_fee',
            'event_date',
            'registration_start',
            'registration_end',
            'banner',
        ]
