from rest_framework import serializers
from .models import Society, SocietyMember


class SocietyMemberSerializer(serializers.ModelSerializer):
    """Serializer for SocietyMember model."""

    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    society_name = serializers.CharField(source='society.name', read_only=True)

    class Meta:
        model = SocietyMember
        fields = [
            'id',
            'society',
            'society_name',
            'user',
            'user_email',
            'user_name',
            'position',
            'bio',
            'is_active',
            'joined_at',
            'left_at',
        ]
        read_only_fields = ['id', 'joined_at']


class SocietySerializer(serializers.ModelSerializer):
    """Serializer for Society model."""

    president_name = serializers.CharField(source='president.get_full_name', read_only=True, allow_null=True)
    vice_president_name = serializers.CharField(source='vice_president.get_full_name', read_only=True, allow_null=True)
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)

    class Meta:
        model = Society
        fields = [
            'id',
            'tenant',
            'tenant_name',
            'name',
            'slug',
            'description',
            'president',
            'president_name',
            'vice_president',
            'vice_president_name',
            'email',
            'phone',
            'logo',
            'banner',
            'is_active',
            'founded_year',
            'member_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class SocietyDetailSerializer(SocietySerializer):
    """Detailed serializer with members."""

    members = serializers.SerializerMethodField()
    organized_modules = serializers.SerializerMethodField()
    organized_sports = serializers.SerializerMethodField()

    class Meta(SocietySerializer.Meta):
        fields = SocietySerializer.Meta.fields + [
            'members',
            'organized_modules',
            'organized_sports',
        ]

    def get_members(self, obj):
        members = obj.members.filter(is_active=True)
        return SocietyMemberSerializer(members, many=True).data

    def get_organized_modules(self, obj):
        from modules.serializers import ModuleSerializer
        modules = obj.organized_modules.all()
        return ModuleSerializer(modules, many=True).data

    def get_organized_sports(self, obj):
        from sports.serializers import SportSerializer
        sports = obj.organized_sports.all()
        return SportSerializer(sports, many=True).data


class SocietyCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating societies."""

    class Meta:
        model = Society
        fields = [
            'tenant',
            'name',
            'description',
            'president',
            'vice_president',
            'email',
            'phone',
            'logo',
            'banner',
            'founded_year',
        ]


class SocietyMemberCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating society members."""

    class Meta:
        model = SocietyMember
        fields = [
            'society',
            'user',
            'position',
            'bio',
        ]
