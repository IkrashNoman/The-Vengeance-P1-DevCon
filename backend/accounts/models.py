from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import URLValidator, EmailValidator


class UserManager(BaseUserManager):
    """Custom user manager for the User model."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user."""
        if not email:
            raise ValueError("Email must be provided")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'super_admin')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Enhanced custom user model with tenant, role, and additional profile fields.
    Supports multi-tenancy and role-based access control (RBAC).
    """

    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('organizer', 'Organizer'),
        ('staff', 'Staff'),
        ('attendee', 'Attendee'),
        ('speaker', 'Speaker'),
        ('sponsor', 'Sponsor'),
    ]

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Multi-tenancy
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='users'
    )

    # Enhanced fields
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='attendee')
    
    # Profile information
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    company = models.CharField(max_length=255, blank=True)
    industry = models.CharField(max_length=255, blank=True)
    interests = models.JSONField(default=list, blank=True, help_text="JSON array of interests")
    
    # Verification and status
    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tenant', 'role']),
            models.Index(fields=['email']),
        ]

    def __str__(self) -> str:
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    def get_full_name(self):
        """Return the user's full name with fallback."""
        return super().get_full_name() or self.email

    def is_super_admin(self):
        return self.role == 'super_admin'

    def is_organizer(self):
        return self.role == 'organizer'

    def is_staff_member(self):
        return self.role == 'staff'

    def is_attendee(self):
        return self.role == 'attendee'


class UserPermission(models.Model):
    """
    Fine-grained permission model for RBAC.
    Maps permissions to departments and event-specific roles.
    """

    PERMISSION_CHOICES = [
        ('view_all', 'View All'),
        ('edit_all', 'Edit All'),
        ('delete_all', 'Delete All'),
        ('manage_registrations', 'Manage Registrations'),
        ('manage_sessions', 'Manage Sessions'),
        ('manage_venues', 'Manage Venues'),
        ('manage_speakers', 'Manage Speakers'),
        ('view_analytics', 'View Analytics'),
        ('manage_staff', 'Manage Staff'),
        ('approve_submissions', 'Approve Submissions'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='permissions'
    )
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='user_permissions'
    )
    permissions = models.JSONField(
        default=list,
        blank=True,
        help_text="JSON array of permission codes"
    )
    can_manage_events = models.BooleanField(default=False)
    can_manage_registrations = models.BooleanField(default=False)
    can_manage_staff = models.BooleanField(default=False)
    can_view_analytics = models.BooleanField(default=False)
    can_approve_content = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Permission"
        verbose_name_plural = "User Permissions"

    def __str__(self):
        return f"Permissions for {self.user.email}"

    def has_permission(self, permission_code):
        """Check if user has a specific permission."""
        return permission_code in self.permissions
