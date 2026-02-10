from rest_framework import serializers
from .models import Olympiad, Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""

    class Meta:
        model = Category
        fields = [
            'id',
            'olympiad',
            'name',
            'category_type',
            'description',
            'is_active',
            'order',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class OlympiadSerializer(serializers.ModelSerializer):
    """Serializer for Olympiad model."""

    organizer_name = serializers.CharField(source='organizer.get_full_name', read_only=True)
    days_until_start = serializers.SerializerMethodField()

    class Meta:
        model = Olympiad
        fields = [
            'id',
            'tenant',
            'name',
            'slug',
            'description',
            'start_date',
            'end_date',
            'registration_start',
            'registration_end',
            'organizer',
            'organizer_name',
            'banner',
            'logo',
            'max_participants',
            'is_published',
            'is_active',
            'days_until_start',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']

    def get_days_until_start(self, obj):
        from datetime import datetime
        from django.utils import timezone
        now = timezone.now()
        delta = obj.start_date - now
        return delta.days


class OlympiadDetailSerializer(OlympiadSerializer):
    """Detailed serializer with related categories, modules, and sports."""

    categories = CategorySerializer(many=True, read_only=True)
    modules_count = serializers.SerializerMethodField()
    sports_count = serializers.SerializerMethodField()
    total_registrations = serializers.SerializerMethodField()

    class Meta(OlympiadSerializer.Meta):
        fields = OlympiadSerializer.Meta.fields + [
            'categories',
            'modules_count',
            'sports_count',
            'total_registrations',
        ]

    def get_modules_count(self, obj):
        return obj.modules.count()

    def get_sports_count(self, obj):
        return obj.sports.count()

    def get_total_registrations(self, obj):
        from registrations.models import Registration
        return Registration.objects.filter(
            olympiad=obj,
            status='confirmed'
        ).count()


class OlympiadCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating olympiads."""

    class Meta:
        model = Olympiad
        fields = [
            'tenant',
            'name',
            'description',
            'start_date',
            'end_date',
            'registration_start',
            'registration_end',
            'organizer',
            'banner',
            'logo',
            'max_participants',
        ]


class CategoryCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating categories."""

    class Meta:
        model = Category
        fields = [
            'olympiad',
            'name',
            'category_type',
            'description',
            'order',
        ]
