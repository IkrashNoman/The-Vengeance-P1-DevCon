from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserPermission


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    full_name = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'full_name',
            'phone',
            'role',
            'bio',
            'avatar',
            'company',
            'industry',
            'interests',
            'email_verified',
            'is_active',
            'tenant',
            'is_admin',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_admin']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_is_admin(self, obj):
        return obj.is_super_admin()


class UserDetailSerializer(UserSerializer):
    """Detailed serializer with all user information."""
    
    permissions = serializers.SerializerMethodField()
    department_memberships = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['permissions', 'department_memberships']

    def get_permissions(self, obj):
        try:
            return UserPermissionSerializer(obj.permissions).data
        except UserPermission.DoesNotExist:
            return None

    def get_department_memberships(self, obj):
        from departments.serializers import DepartmentMemberSerializer
        memberships = obj.department_memberships.filter(is_active=True)
        return DepartmentMemberSerializer(memberships, many=True).data


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users."""

    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
            'password_confirm',
            'first_name',
            'last_name',
            'phone',
            'company',
            'industry',
        ]

    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data['user'] = user
        return data


class UserPermissionSerializer(serializers.ModelSerializer):
    """Serializer for UserPermission model."""

    class Meta:
        model = UserPermission
        fields = [
            'id',
            'department',
            'permissions',
            'can_manage_events',
            'can_manage_registrations',
            'can_manage_staff',
            'can_view_analytics',
            'can_approve_content',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
