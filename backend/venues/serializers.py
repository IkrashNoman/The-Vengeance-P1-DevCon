from rest_framework import serializers
from .models import Venue, VenueSpace, Seating


class SeatingSerializer(serializers.ModelSerializer):
    """Serializer for Seating model."""

    space_name = serializers.CharField(source='space.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = Seating
        fields = [
            'id',
            'space',
            'space_name',
            'seat_number',
            'seating_type',
            'row',
            'column',
            'status',
            'assigned_to',
            'assigned_to_name',
            'assigned_at',
            'x_coordinate',
            'y_coordinate',
        ]
        read_only_fields = ['id']


class VenueSpaceSerializer(serializers.ModelSerializer):
    """Serializer for VenueSpace model."""

    venue_name = serializers.CharField(source='venue.name', read_only=True)
    seating_count = serializers.SerializerMethodField()
    available_seating = serializers.SerializerMethodField()

    class Meta:
        model = VenueSpace
        fields = [
            'id',
            'venue',
            'venue_name',
            'name',
            'space_type',
            'capacity',
            'floor',
            'layout_data',
            'is_available',
            'seating_count',
            'available_seating',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_seating_count(self, obj):
        return obj.seating.count()

    def get_available_seating(self, obj):
        return obj.seating.filter(status='available').count()


class VenueSpaceDetailSerializer(VenueSpaceSerializer):
    """Detailed serializer with seating."""

    seating = SeatingSerializer(many=True, read_only=True)

    class Meta(VenueSpaceSerializer.Meta):
        fields = VenueSpaceSerializer.Meta.fields + ['seating']


class VenueSerializer(serializers.ModelSerializer):
    """Serializer for Venue model."""

    tenant_name = serializers.CharField(source='tenant.name', read_only=True)

    class Meta:
        model = Venue
        fields = [
            'id',
            'tenant',
            'tenant_name',
            'name',
            'description',
            'address',
            'city',
            'state',
            'postal_code',
            'country',
            'latitude',
            'longitude',
            'total_capacity',
            'contact_name',
            'contact_phone',
            'image',
            'floor_plan',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class VenueDetailSerializer(VenueSerializer):
    """Detailed serializer with spaces."""

    spaces = VenueSpaceSerializer(many=True, read_only=True)
    available_capacity = serializers.SerializerMethodField()

    class Meta(VenueSerializer.Meta):
        fields = VenueSerializer.Meta.fields + ['spaces', 'available_capacity']

    def get_available_capacity(self, obj):
        available = obj.spaces.count()
        return available


class VenueCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating venues."""

    class Meta:
        model = Venue
        fields = [
            'tenant',
            'name',
            'description',
            'address',
            'city',
            'state',
            'postal_code',
            'country',
            'latitude',
            'longitude',
            'total_capacity',
            'contact_name',
            'contact_phone',
            'image',
            'floor_plan',
        ]


class VenueSpaceCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating venue spaces."""

    class Meta:
        model = VenueSpace
        fields = [
            'venue',
            'name',
            'space_type',
            'capacity',
            'floor',
            'layout_data',
        ]


class SeatingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating seating."""

    class Meta:
        model = Seating
        fields = [
            'space',
            'seat_number',
            'seating_type',
            'row',
            'column',
            'x_coordinate',
            'y_coordinate',
        ]
