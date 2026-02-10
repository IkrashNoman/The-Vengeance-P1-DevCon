from rest_framework import serializers
from .models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    """Serializer for Tenant model."""

    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)

    class Meta:
        model = Tenant
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'logo',
            'primary_color',
            'secondary_color',
            'owner',
            'owner_name',
            'contact_email',
            'contact_phone',
            'website',
            'is_active',
            'max_events',
            'max_users',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class TenantDetailSerializer(TenantSerializer):
    """Detailed serializer with related data."""

    departments_count = serializers.SerializerMethodField()
    events_count = serializers.SerializerMethodField()
    users_count = serializers.SerializerMethodField()

    class Meta(TenantSerializer.Meta):
        fields = TenantSerializer.Meta.fields + [
            'departments_count',
            'events_count',
            'users_count',
        ]

    def get_departments_count(self, obj):
        return obj.departments.count()

    def get_events_count(self, obj):
        return obj.events.count()

    def get_users_count(self, obj):
        return obj.users.count()


class TenantCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tenants."""

    class Meta:
        model = Tenant
        fields = [
            'name',
            'description',
            'logo',
            'primary_color',
            'secondary_color',
            'owner',
            'contact_email',
            'contact_phone',
            'website',
            'max_events',
            'max_users',
        ]
