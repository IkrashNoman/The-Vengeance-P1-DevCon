from rest_framework import serializers
from .models import Department, DepartmentMember


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model."""

    head_name = serializers.CharField(source='head.get_full_name', read_only=True)
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)

    class Meta:
        model = Department
        fields = [
            'id',
            'tenant',
            'tenant_name',
            'name',
            'department_type',
            'description',
            'head',
            'head_name',
            'can_manage_users',
            'can_manage_events',
            'can_manage_registrations',
            'can_manage_content',
            'can_view_analytics',
            'can_manage_financials',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DepartmentDetailSerializer(DepartmentSerializer):
    """Detailed serializer with members."""

    members = serializers.SerializerMethodField()
    members_count = serializers.SerializerMethodField()

    class Meta(DepartmentSerializer.Meta):
        fields = DepartmentSerializer.Meta.fields + ['members', 'members_count']

    def get_members(self, obj):
        members = obj.members.filter(is_active=True)
        return DepartmentMemberSerializer(members, many=True).data

    def get_members_count(self, obj):
        return obj.members.filter(is_active=True).count()


class DepartmentMemberSerializer(serializers.ModelSerializer):
    """Serializer for DepartmentMember model."""

    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = DepartmentMember
        fields = [
            'id',
            'department',
            'department_name',
            'user',
            'user_email',
            'user_name',
            'role',
            'is_active',
            'joined_at',
            'left_at',
        ]
        read_only_fields = ['id', 'joined_at']


class DepartmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating departments."""

    class Meta:
        model = Department
        fields = [
            'tenant',
            'name',
            'department_type',
            'description',
            'head',
            'can_manage_users',
            'can_manage_events',
            'can_manage_registrations',
            'can_manage_content',
            'can_view_analytics',
            'can_manage_financials',
        ]


class DepartmentMemberCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating department members."""

    class Meta:
        model = DepartmentMember
        fields = [
            'department',
            'user',
            'role',
        ]
