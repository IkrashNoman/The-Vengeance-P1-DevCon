from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import User, UserPermission
from .serializers import (
    UserSerializer,
    UserDetailSerializer,
    UserCreateSerializer,
    LoginSerializer,
    UserPermissionSerializer,
)
from core_permissions import IsSuperAdmin, IsOwner, IsReadOnly


class AuthenticationView(views.APIView):
    """
    API View for user authentication (login/signup).
    """

    permission_classes = [AllowAny]

    def post(self, request, action='login'):
        if action == 'login':
            return self.login(request)
        elif action == 'signup':
            return self.signup(request)
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

    def login(self, request):
        """User login endpoint."""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def signup(self, request):
        """User signup endpoint."""
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users with role-based access control.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'list']:
            return [AllowAny() if self.action == 'create' else IsAuthenticated()]
        elif self.action in ['retrieve', 'me']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsOwner()]
        elif self.action == 'destroy':
            return [IsSuperAdmin()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        """List users - filtered by tenant for non-admins."""
        if not request.user.is_super_admin():
            self.queryset = self.queryset.filter(tenant=request.user.tenant)
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return User.objects.none()
        if user.is_super_admin():
            return User.objects.all()
        if user.tenant:
            return User.objects.filter(tenant=user.tenant)
        return User.objects.filter(id=user.id)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user details."""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change user password."""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsSuperAdmin])
    def assign_role(self, request, pk=None):
        """Assign a role to a user (admin only)."""
        user = self.get_object()
        role = request.data.get('role')

        if role not in dict(User.ROLE_CHOICES):
            return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)

        user.role = role
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """User logout endpoint."""
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


class UserPermissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user permissions.
    """

    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin():
            return UserPermission.objects.all()
        return UserPermission.objects.filter(user=user)

    @action(detail=False, methods=['post'])
    def bulk_assign(self, request):
        """Bulk assign permissions to multiple users."""
        users = request.data.get('users', [])
        permissions = request.data.get('permissions', [])

        for user_id in users:
            try:
                user = User.objects.get(id=user_id)
                perm, created = UserPermission.objects.get_or_create(user=user)
                perm.permissions = permissions
                perm.save()
            except User.DoesNotExist:
                pass

        return Response({'message': f'Permissions assigned to {len(users)} users'}, status=status.HTTP_200_OK)
