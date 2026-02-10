from django.db import models


class EventAnalytics(models.Model):
    """
    Aggregate analytics for events.
    """

    event = models.OneToOneField(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='analytics'
    )
    
    # Attendance
    total_registered = models.IntegerField(default=0)
    total_attended = models.IntegerField(default=0)
    no_show_count = models.IntegerField(default=0)
    
    # Engagement
    average_session_duration = models.FloatField(default=0, help_text="In minutes")
    engagement_score = models.FloatField(default=0, help_text="0.0-1.0")
    
    # Interactions
    total_polls_created = models.IntegerField(default=0)
    total_poll_responses = models.IntegerField(default=0)
    total_qna_questions = models.IntegerField(default=0)
    total_feedback_responses = models.IntegerField(default=0)
    
    # Network
    connections_made = models.IntegerField(default=0)
    card_exchanges = models.IntegerField(default=0)
    
    # Demographics
    demographics_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Age, gender, industry distributions"
    )
    
    # Sentiment
    overall_sentiment = models.CharField(
        max_length=50,
        choices=[('positive', 'Positive'), ('neutral', 'Neutral'), ('negative', 'Negative')],
        default='neutral'
    )
    average_satisfaction_score = models.FloatField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics for {self.event.name}"


class ModuleAnalytics(models.Model):
    """
    Analytics for module competitions.
    """

    module = models.OneToOneField(
        'modules.Module',
        on_delete=models.CASCADE,
        related_name='analytics'
    )
    
    # Registration
    total_registered_teams = models.IntegerField(default=0)
    total_registered_members = models.IntegerField(default=0)
    
    # Participation
    teams_participated = models.IntegerField(default=0)
    members_participated = models.IntegerField(default=0)
    
    # Performance
    average_team_score = models.FloatField(default=0)
    highest_team_score = models.FloatField(default=0)
    
    # Diversity
    unique_organizations = models.IntegerField(default=0)
    gender_distribution = models.JSONField(default=dict, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics for {self.module.name}"


class SportAnalytics(models.Model):
    """
    Analytics for sports competitions.
    """

    sport = models.OneToOneField(
        'sports.Sport',
        on_delete=models.CASCADE,
        related_name='analytics'
    )
    
    # Registration
    total_registered_teams = models.IntegerField(default=0)
    total_registered_members = models.IntegerField(default=0)
    
    # Participation
    teams_participated = models.IntegerField(default=0)
    members_participated = models.IntegerField(default=0)
    
    # Matches
    total_matches = models.IntegerField(default=0)
    completed_matches = models.IntegerField(default=0)
    
    # Viewership
    total_views = models.IntegerField(default=0)
    
    # Diversity
    unique_organizations = models.IntegerField(default=0)
    gender_distribution = models.JSONField(default=dict, blank=True)
    age_distribution = models.JSONField(default=dict, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics for {self.sport.name}"


class OlympiadAnalytics(models.Model):
    """
    Top-level analytics for entire olympiad.
    """

    olympiad = models.OneToOneField(
        'olympiad_core.Olympiad',
        on_delete=models.CASCADE,
        related_name='analytics'
    )
    
    # Overall metrics
    total_registrations = models.IntegerField(default=0)
    total_participants = models.IntegerField(default=0)
    total_events = models.IntegerField(default=0)
    total_modules = models.IntegerField(default=0)
    total_sports = models.IntegerField(default=0)
    
    # Engagement
    total_check_ins = models.IntegerField(default=0)
    attendance_rate = models.FloatField(default=0, help_text="Percentage 0-100")
    
    # Networking
    total_connections = models.IntegerField(default=0)
    avg_connections_per_user = models.FloatField(default=0)
    
    # Financial
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Satisfaction
    overall_satisfaction = models.FloatField(default=0, help_text="Average rating 1-5")
    nps_score = models.IntegerField(null=True, blank=True, help_text="Net Promoter Score -100 to 100")
    
    # Demographics
    total_unique_organizations = models.IntegerField(default=0)
    gender_distribution = models.JSONField(default=dict, blank=True)
    geographic_distribution = models.JSONField(default=dict, blank=True)
    
    # Social media
    hashtag_mentions = models.IntegerField(default=0)
    social_engagement_score = models.FloatField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics for {self.olympiad.name}"


class UserEngagementScore(models.Model):
    """
    Individual engagement scores for users.
    """

    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='engagement_score'
    )
    
    # Scores (0.0-1.0)
    base_score = models.FloatField(default=0)
    attendance_score = models.FloatField(default=0)
    interaction_score = models.FloatField(default=0)
    networking_score = models.FloatField(default=0)
    learning_score = models.FloatField(default=0)
    
    # Overall
    overall_score = models.FloatField(default=0)
    
    # Badges/Achievements
    achievements = models.JSONField(default=list, blank=True)
    
    # Tier
    TIER_CHOICES = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ]
    tier = models.CharField(max_length=50, choices=TIER_CHOICES, default='bronze')
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Engagement Score for {self.user.email}"


class DailyMetrics(models.Model):
    """
    Daily aggregated metrics for tracking trends.
    """

    date = models.DateField()
    
    olympiad = models.ForeignKey(
        'olympiad_core.Olympiad',
        on_delete=models.CASCADE,
        related_name='daily_metrics'
    )
    
    # Daily activity
    new_registrations = models.IntegerField(default=0)
    daily_active_users = models.IntegerField(default=0)
    sessions_attended = models.IntegerField(default=0)
    
    # Engagement
    polls_created = models.IntegerField(default=0)
    qna_questions = models.IntegerField(default=0)
    messages_sent = models.IntegerField(default=0)
    
    # Networking
    connections_made = models.IntegerField(default=0)
    
    # Financial
    daily_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('date', 'olympiad')
        ordering = ['-date']

    def __str__(self):
        return f"Metrics for {self.olympiad.name} on {self.date}"
