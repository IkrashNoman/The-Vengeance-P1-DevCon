from rest_framework import serializers
from .models import Sport, SportMatch, SportRanking


class SportSerializer(serializers.ModelSerializer):
    """Serializer for Sport model."""

    olympiad_name = serializers.CharField(source='olympiad.name', read_only=True)
    society_name = serializers.CharField(source='organizing_society.name', read_only=True, allow_null=True)
    venue_name = serializers.CharField(source='venue.name', read_only=True, allow_null=True)

    class Meta:
        model = Sport
        fields = [
            'id',
            'olympiad',
            'olympiad_name',
            'name',
            'slug',
            'description',
            'sport_type',
            'organizing_society',
            'society_name',
            'rules_document',
            'max_participants',
            'min_team_size',
            'max_team_size',
            'registration_fee',
            'event_date',
            'registration_start',
            'registration_end',
            'venue',
            'venue_name',
            'banner',
            'is_published',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class SportDetailSerializer(SportSerializer):
    """Detailed serializer with matches and rankings."""

    matches = serializers.SerializerMethodField()
    rankings = serializers.SerializerMethodField()
    total_registrations = serializers.SerializerMethodField()

    class Meta(SportSerializer.Meta):
        fields = SportSerializer.Meta.fields + [
            'matches',
            'rankings',
            'total_registrations',
        ]

    def get_matches(self, obj):
        matches = obj.matches.all().order_by('scheduled_time')
        return SportMatchSerializer(matches, many=True).data

    def get_rankings(self, obj):
        rankings = obj.rankings.all().order_by('rank')[:10]
        return SportRankingSerializer(rankings, many=True).data

    def get_total_registrations(self, obj):
        from registrations.models import Registration
        return Registration.objects.filter(
            sport=obj,
            status='confirmed'
        ).count()


class SportMatchSerializer(serializers.ModelSerializer):
    """Serializer for SportMatch model."""

    sport_name = serializers.CharField(source='sport.name', read_only=True)
    team_a_name = serializers.CharField(source='team_a.name', read_only=True, allow_null=True)
    team_b_name = serializers.CharField(source='team_b.name', read_only=True, allow_null=True)
    winner_name = serializers.CharField(source='winner.name', read_only=True, allow_null=True)
    venue_name = serializers.CharField(source='venue.name', read_only=True, allow_null=True)

    class Meta:
        model = SportMatch
        fields = [
            'id',
            'sport',
            'sport_name',
            'name',
            'description',
            'team_a',
            'team_a_name',
            'team_b',
            'team_b_name',
            'scheduled_time',
            'venue',
            'venue_name',
            'status',
            'team_a_score',
            'team_b_score',
            'winner',
            'winner_name',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SportRankingSerializer(serializers.ModelSerializer):
    """Serializer for SportRanking model."""

    sport_name = serializers.CharField(source='sport.name', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)
    organization = serializers.CharField(source='team.organization_name', read_only=True)

    class Meta:
        model = SportRanking
        fields = [
            'id',
            'sport',
            'sport_name',
            'team',
            'team_name',
            'organization',
            'rank',
            'medal',
            'points',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class SportCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating sports."""

    class Meta:
        model = Sport
        fields = [
            'olympiad',
            'name',
            'description',
            'sport_type',
            'organizing_society',
            'rules_document',
            'max_participants',
            'min_team_size',
            'max_team_size',
            'registration_fee',
            'event_date',
            'registration_start',
            'registration_end',
            'venue',
            'banner',
        ]
