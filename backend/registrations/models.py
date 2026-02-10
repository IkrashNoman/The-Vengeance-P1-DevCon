from django.db import models
import uuid


class Registration(models.Model):
    """
    Represents registration of an attendee to an event or module.
    """

    REGISTRATION_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('rejected', 'Rejected'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    # Unique identifier
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # References
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    
    # Can register for event, module, or sport
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='registrations'
    )
    module = models.ForeignKey(
        'modules.Module',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='registrations'
    )
    sport = models.ForeignKey(
        'sports.Sport',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='registrations'
    )
    
    # Status
    status = models.CharField(max_length=50, choices=REGISTRATION_STATUS, default='pending')
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS, default='pending')
    
    # Fee information
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Payment details
    payment_method = models.CharField(
        max_length=50,
        choices=[('stripe', 'Stripe'), ('paypal', 'PayPal'), ('bank', 'Bank Transfer'), ('free', 'Free')],
        default='free'
    )
    transaction_id = models.CharField(max_length=255, blank=True)
    
    # QR Code for check-in
    qr_code = models.CharField(max_length=255, unique=True, null=True, blank=True)
    
    # Registration data
    registration_data = models.JSONField(default=dict, blank=True, help_text="Custom registration form data")
    
    # Timestamps
    registered_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-registered_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['qr_code']),
        ]

    def __str__(self):
        return f"{self.user.email} - Registration {self.id}"


class Team(models.Model):
    """
    Represents a team for team-based competitions (modules/sports).
    """

    TEAM_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('disqualified', 'Disqualified'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField()
    
    # Module/Sport association
    module = models.ForeignKey(
        'modules.Module',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='teams_competing'
    )
    sport = models.ForeignKey(
        'sports.Sport',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='teams_competing'
    )
    
    # Team leadership
    team_lead = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='led_teams'
    )
    
    # Category
    category = models.ForeignKey(
        'olympiad_core.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teams'
    )
    
    # Organization
    organization_name = models.CharField(max_length=255, blank=True)
    
    # Status and metadata
    status = models.CharField(max_length=50, choices=TEAM_STATUS, default='active')
    is_qualified = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    """
    Links users to teams as members.
    """

    MEMBER_ROLES = [
        ('leader', 'Leader'),
        ('member', 'Member'),
        ('alternate', 'Alternate'),
    ]

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='members'
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='team_memberships'
    )
    
    role = models.CharField(max_length=50, choices=MEMBER_ROLES, default='member')
    registration = models.ForeignKey(
        Registration,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='team_memberships'
    )
    
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'user')
        ordering = ['role', 'joined_at']

    def __str__(self):
        return f"{self.user.email} - {self.team.name}"


class RegistrationForm(models.Model):
    """
    Custom registration forms for events/modules/sports.
    """

    module = models.OneToOneField(
        'modules.Module',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='registration_form'
    )
    sport = models.OneToOneField(
        'sports.Sport',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='registration_form'
    )
    
    fields = models.JSONField(
        default=list,
        blank=True,
        help_text="JSON array of form fields with validation rules"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Registration Form for {self.module or self.sport}"
