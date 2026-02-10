from django.db import models


class NetworkProfile(models.Model):
    """
    Enhanced networking profile for attendees.
    """

    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='network_profile'
    )
    
    # Professional info
    job_title = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    industry = models.CharField(max_length=255, blank=True)
    
    # Interests and goals
    interests = models.JSONField(default=list, blank=True)
    networking_goals = models.TextField(blank=True)
    expertise = models.JSONField(default=list, blank=True)
    
    # Visibility preferences
    show_in_discovery = models.BooleanField(default=True)
    allow_direct_messages = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Network Profile - {self.user.email}"


class Connection(models.Model):
    """
    Represents a networking connection between two users.
    """

    CONNECTION_STATUS = [
        ('pending', 'Pending'),
        ('connected', 'Connected'),
        ('blocked', 'Blocked'),
    ]

    user_from = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='connections_initiated'
    )
    user_to = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='connections_received'
    )
    
    status = models.CharField(max_length=50, choices=CONNECTION_STATUS, default='pending')
    
    # Details
    message = models.TextField(blank=True, help_text="Connection request message")
    tags = models.JSONField(default=list, blank=True, help_text="Tags for this connection")
    
    # Timestamps
    initiated_at = models.DateTimeField(auto_now_add=True)
    connected_at = models.DateTimeField(null=True, blank=True)
    last_interaction = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user_from', 'user_to')
        ordering = ['-initiated_at']

    def __str__(self):
        return f"{self.user_from.email} -> {self.user_to.email} ({self.status})"


class RecommendedConnection(models.Model):
    """
    AI-recommended connections based on similarity and mutual interests.
    """

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='recommended_connections'
    )
    recommended_user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='recommended_by'
    )
    
    # Recommendation details
    match_score = models.FloatField(default=0.0, help_text="Similarity score 0.0-1.0")
    reason = models.CharField(
        max_length=255,
        blank=True,
        help_text="Reason for recommendation (e.g., 'Similar interests', 'Same industry')"
    )
    
    was_connected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recommended_user')
        ordering = ['-match_score']

    def __str__(self):
        return f"Recommend {self.recommended_user.email} to {self.user.email}"


class Message(models.Model):
    """
    Direct messaging between connected users.
    """

    conversation_with = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE
    )
    
    sender = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    
    content = models.TextField()
    
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.sender.email} to {self.receiver.email}"


class DigitalCard(models.Model):
    """
    Digital business cards for networking.
    """

    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='digital_card'
    )
    
    # Card data
    card_data = models.JSONField(
        default=dict,
        help_text="Complete business card information"
    )
    qr_code = models.CharField(max_length=255, unique=True)
    
    template_style = models.CharField(max_length=50, default='modern')
    custom_colors = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Digital Card - {self.user.email}"


class CardExchange(models.Model):
    """
    Track digital card exchanges between users.
    """

    user_a = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='card_exchanges_sent'
    )
    user_b = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='card_exchanges_received'
    )
    
    exchanged_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('user_a', 'user_b')

    def __str__(self):
        return f"Card Exchange: {self.user_a.email} <-> {self.user_b.email}"
