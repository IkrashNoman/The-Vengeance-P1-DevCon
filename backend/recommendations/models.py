from django.db import models


class UserActivityLog(models.Model):
    """
    Tracks user activities for recommendation algorithms.
    """

    ACTIVITY_TYPES = [
        ('view_session', 'Viewed Session'),
        ('register_session', 'Registered for Session'),
        ('attend_session', 'Attended Session'),
        ('view_profile', 'Viewed Profile'),
        ('connect_request', 'Connection Request'),
        ('view_module', 'Viewed Module'),
        ('view_sport', 'Viewed Sport'),
    ]

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='activity_logs'
    )
    
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    
    # Related object
    content_type = models.CharField(max_length=50, blank=True)
    object_id = models.CharField(max_length=255, blank=True)
    
    # Engagement metrics
    duration_seconds = models.IntegerField(null=True, blank=True)
    engagement_score = models.FloatField(default=1.0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'activity_type']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.user.email}: {self.activity_type}"


class SessionRecommendation(models.Model):
    """
    AI-recommended sessions for users.
    """

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='session_recommendations'
    )
    
    session = models.ForeignKey(
        'events.EventSession',
        on_delete=models.CASCADE,
        related_name='recommendations'
    )
    
    # Recommendation details
    score = models.FloatField(help_text="Recommendation score 0.0-1.0")
    reason = models.CharField(
        max_length=255,
        choices=[
            ('interest_match', 'Matches your interests'),
            ('collaborative_filtering', 'Users like you attended'),
            ('trending', 'Trending session'),
            ('speaker_follow', 'By followed speaker'),
        ]
    )
    
    was_clicked = models.BooleanField(default=False)
    was_attended = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'session')
        ordering = ['-score']

    def __str__(self):
        return f"Recommend {self.session.name} to {self.user.email}"


class ModuleRecommendation(models.Model):
    """
    AI-recommended modules for users.
    """

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='module_recommendations'
    )
    
    module = models.ForeignKey(
        'modules.Module',
        on_delete=models.CASCADE,
        related_name='recommendations'
    )
    
    # Recommendation details
    score = models.FloatField(help_text="Recommendation score 0.0-1.0")
    reason = models.CharField(
        max_length=255,
        choices=[
            ('skill_level', 'Matches skill level'),
            ('interest', 'Matches interests'),
            ('performance', 'Based on past performance'),
        ]
    )
    
    was_viewed = models.BooleanField(default=False)
    was_registered = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'module')
        ordering = ['-score']

    def __str__(self):
        return f"Recommend {self.module.name} to {self.user.email}"


class PersonalizedAgenda(models.Model):
    """
    AI-generated personalized agendas for users.
    """

    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='personalized_agenda'
    )
    
    olympiad = models.ForeignKey(
        'olympiad_core.Olympiad',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='personalized_agendas'
    )
    
    # Agenda content
    items = models.JSONField(
        default=list,
        help_text="JSON array of recommended sessions/modules with timing"
    )
    
    # Generation metadata
    generation_reason = models.TextField(blank=True)
    algorithm_version = models.CharField(max_length=50, default='v1')
    
    # Feedback
    user_satisfaction = models.IntegerField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Agenda for {self.user.email}"


class RecommendationFeedback(models.Model):
    """
    User feedback on recommendations to improve algorithms.
    """

    FEEDBACK_TYPES = [
        ('session', 'Session Recommendation'),
        ('module', 'Module Recommendation'),
        ('connection', 'Connection Recommendation'),
    ]

    FEEDBACK_SCORES = [
        (1, '1 - Not relevant'),
        (2, '2 - Somewhat relevant'),
        (3, '3 - Relevant'),
        (4, '4 - Very relevant'),
        (5, '5 - Perfect'),
    ]

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='recommendation_feedback'
    )
    
    feedback_type = models.CharField(max_length=50, choices=FEEDBACK_TYPES)
    content_type = models.CharField(max_length=50)
    object_id = models.CharField(max_length=255)
    
    relevance_score = models.IntegerField(choices=FEEDBACK_SCORES)
    comments = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback from {self.user.email}: Score {self.relevance_score}"
