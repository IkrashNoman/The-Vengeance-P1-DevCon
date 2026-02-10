from django.db import models


class Department(models.Model):
    """
    Represents departments within a tenant (e.g., Management, Registration, Marketing, Security).
    Each department has specific responsibilities and access levels.
    """

    DEPARTMENT_TYPES = [
        ('management', 'Management'),
        ('registration', 'Registration'),
        ('marketing', 'Marketing'),
        ('security', 'Security'),
        ('technical', 'Technical'),
        ('logistics', 'Logistics'),
        ('finance', 'Finance'),
        ('sponsorship', 'Sponsorship'),
    ]

    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='departments'
    )
    
    name = models.CharField(max_length=255)
    department_type = models.CharField(max_length=50, choices=DEPARTMENT_TYPES)
    description = models.TextField(blank=True)
    
    # Head of department
    head = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_departments'
    )
    
    # Permissions & Responsibilities
    can_manage_users = models.BooleanField(default=False)
    can_manage_events = models.BooleanField(default=False)
    can_manage_registrations = models.BooleanField(default=False)
    can_manage_content = models.BooleanField(default=False)
    can_view_analytics = models.BooleanField(default=False)
    can_manage_financials = models.BooleanField(default=False)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('tenant', 'name', 'department_type')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_department_type_display()})"


class DepartmentMember(models.Model):
    """
    Links users to departments with specific roles.
    """

    ROLE_CHOICES = [
        ('head', 'Head'),
        ('senior_member', 'Senior Member'),
        ('member', 'Member'),
        ('coordinator', 'Coordinator'),
    ]

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='members'
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='department_memberships'
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='member')
    
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('department', 'user')
        ordering = ['role', 'joined_at']

    def __str__(self):
        return f"{self.user.email} - {self.department.name} ({self.get_role_display()})"
