from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsAuthenticated(permissions.IsAuthenticated):
    """Extended is authenticated check."""
    pass


class IsSuperAdmin(permissions.BasePermission):
    """Permission for super admin users."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_super_admin()


class IsOrganizer(permissions.BasePermission):
    """Permission for organizer users."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_organizer()


class IsStaff(permissions.BasePermission):
    """Permission for staff users."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user.is_super_admin()


class IsAttendee(permissions.BasePermission):
    """Permission for attendee users."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_attendee()


class IsTenantMember(permissions.BasePermission):
    """Permission to check if user is member of a tenant."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.tenant_id is not None

    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, 'tenant'):
            return False
        return request.user.tenant == obj.tenant


class IsDepartmentHead(permissions.BasePermission):
    """Permission for department heads."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, 'head'):
            return False
        return request.user == obj.head or request.user.is_super_admin()


class IsDepartmentMember(permissions.BasePermission):
    """Permission for department members."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, 'members'):
            return False
        return obj.members.filter(user=request.user, is_active=True).exists() or request.user.is_super_admin()


class CanManageEvents(permissions.BasePermission):
    """Permission to manage events."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_super_admin() or
            request.user.is_organizer() or
            (hasattr(request.user, 'permissions') and request.user.permissions.can_manage_events)
        )


class CanManageRegistrations(permissions.BasePermission):
    """Permission to manage registrations."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_super_admin() or
            (hasattr(request.user, 'permissions') and request.user.permissions.can_manage_registrations)
        )


class CanViewAnalytics(permissions.BasePermission):
    """Permission to view analytics."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_super_admin() or
            request.user.is_organizer() or
            (hasattr(request.user, 'permissions') and request.user.permissions.can_view_analytics)
        )


class CanApproveContent(permissions.BasePermission):
    """Permission to approve content."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_super_admin() or
            (hasattr(request.user, 'permissions') and request.user.permissions.can_approve_content)
        )


class IsOwner(permissions.BasePermission):
    """Permission to check if user is the owner of an object."""

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return request.user == obj.user or request.user.is_super_admin()
        elif hasattr(obj, 'owner'):
            return request.user == obj.owner or request.user.is_super_admin()
        return request.user.is_super_admin()


class IsReadOnly(permissions.BasePermission):
    """Permission for read-only access."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class RoleBasedPermission(permissions.BasePermission):
    """
    Base class for role-based permissions.
    Subclasses should define role_required and optionally object_ownership_required.
    """

    role_required = None
    object_ownership_required = False

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if self.role_required is None:
            return True

        if request.user.is_super_admin():
            return True

        if isinstance(self.role_required, (list, tuple)):
            return request.user.role in self.role_required
        else:
            return request.user.role == self.role_required

    def has_object_permission(self, request, view, obj):
        if request.user.is_super_admin():
            return True

        if self.object_ownership_required:
            if hasattr(obj, 'user') and obj.user == request.user:
                return True
            if hasattr(obj, 'owner') and obj.owner == request.user:
                return True
            return False

        return True
