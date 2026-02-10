from django.db import models


class NotificationTemplate(models.Model):
    """
    Notification templates for different events and triggers.
    """

    NOTIFICATION_TYPES = [
        ('registration', 'Registration'),
        ('payment', 'Payment'),
        ('session_reminder', 'Session Reminder'),
        ('announcement', 'Announcement'),
        ('networking', 'Networking'),
        ('system', 'System'),
        ('feedback', 'Feedback'),
    ]

    name = models.CharField(max_length=255, unique=True)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    
    # Template content
    title_template = models.CharField(max_length=500)
    body_template = models.TextField()
    
    # Settings
    is_active = models.BooleanField(default=True)
    can_customize = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Notification(models.Model):
    """
    Individual notifications sent to users.
    """

    NOTIFICATION_CHANNELS = [
        ('in_app', 'In-App'),
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('read', 'Read'),
    ]

    recipient = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    
    template = models.ForeignKey(
        NotificationTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )
    
    # Content
    title = models.CharField(max_length=500)
    message = models.TextField()
    
    # Metadata
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Delivery
    channels = models.JSONField(default=list, help_text="JSON array of channels to send through")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    
    # Related object
    content_type = models.CharField(max_length=50, blank=True)
    object_id = models.CharField(max_length=255, blank=True)
    
    # Actions/Links
    action_url = models.URLField(blank=True)
    action_text = models.CharField(max_length=255, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    scheduled_for = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"Notification to {self.recipient.email}: {self.title}"


class NotificationPreference(models.Model):
    """
    User preferences for notifications.
    """

    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='notification_preferences'
    )
    
    # Email preferences
    email_on_registration = models.BooleanField(default=True)
    email_on_session_reminder = models.BooleanField(default=True)
    email_on_announcement = models.BooleanField(default=True)
    email_on_networking = models.BooleanField(default=True)
    email_on_feedback = models.BooleanField(default=False)
    
    # Push notification preferences
    push_enabled = models.BooleanField(default=True)
    push_on_session_reminder = models.BooleanField(default=True)
    push_on_announcement = models.BooleanField(default=True)
    push_on_networking = models.BooleanField(default=True)
    
    # SMS preferences
    sms_enabled = models.BooleanField(default=False)
    sms_for_urgent_only = models.BooleanField(default=True)
    
    # Frequency preferences
    digest_frequency = models.CharField(
        max_length=50,
        choices=[
            ('instant', 'Instant'),
            ('daily', 'Daily Digest'),
            ('weekly', 'Weekly Digest'),
        ],
        default='instant'
    )
    
    # Do not disturb
    quiet_hours_enabled = models.BooleanField(default=False)
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notification Preferences for {self.user.email}"
