from rest_framework import serializers
from .models import Registration, Team, TeamMember, RegistrationForm


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for Registration model."""

    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Registration
        fields = [
            'id',
            'user',
            'user_email',
            'user_name',
            'event',
            'module',
            'sport',
            'status',
            'payment_status',
            'registration_fee',
            'amount_paid',
            'payment_method',
            'transaction_id',
            'qr_code',
            'registration_data',
            'registered_at',
            'confirmed_at',
            'cancelled_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'qr_code',
            'registered_at',
            'confirmed_at',
            'cancelled_at',
            'updated_at',
        ]


class TeamMemberSerializer(serializers.ModelSerializer):
    """Serializer for TeamMember model."""

    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = TeamMember
        fields = [
            'id',
            'team',
            'team_name',
            'user',
            'user_email',
            'user_name',
            'role',
            'registration',
            'joined_at',
        ]
        read_only_fields = ['id', 'joined_at']


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model."""

    team_lead_name = serializers.CharField(source='team_lead.get_full_name', read_only=True, allow_null=True)
    category_name = serializers.CharField(source='category.name', read_only=True, allow_null=True)
    module_name = serializers.CharField(source='module.name', read_only=True, allow_null=True)
    sport_name = serializers.CharField(source='sport.name', read_only=True, allow_null=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'slug',
            'module',
            'module_name',
            'sport',
            'sport_name',
            'team_lead',
            'team_lead_name',
            'category',
            'category_name',
            'organization_name',
            'status',
            'is_qualified',
            'member_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']

    def get_member_count(self, obj):
        return obj.members.count()


class TeamDetailSerializer(TeamSerializer):
    """Detailed serializer with members."""

    members = TeamMemberSerializer(many=True, read_only=True)

    class Meta(TeamSerializer.Meta):
        fields = TeamSerializer.Meta.fields + ['members']


class RegistrationFormSerializer(serializers.ModelSerializer):
    """Serializer for RegistrationForm model."""

    class Meta:
        model = RegistrationForm
        fields = [
            'id',
            'module',
            'sport',
            'fields',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RegistrationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating registrations."""

    class Meta:
        model = Registration
        fields = [
            'user',
            'event',
            'module',
            'sport',
            'registration_fee',
            'payment_method',
            'registration_data',
        ]


class TeamCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating teams."""

    class Meta:
        model = Team
        fields = [
            'name',
            'module',
            'sport',
            'team_lead',
            'category',
            'organization_name',
        ]


class TeamMemberCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating team members."""

    class Meta:
        model = TeamMember
        fields = [
            'team',
            'user',
            'role',
            'registration',
        ]
