from django.db import models


class Poll(models.Model):
    """
    Live polls during sessions.
    """

    POLL_TYPES = [
        ('single_choice', 'Single Choice'),
        ('multiple_choice', 'Multiple Choice'),
        ('rating', 'Rating'),
        ('free_text', 'Free Text'),
    ]

    event_session = models.ForeignKey(
        'events.EventSession',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='polls'
    )
    
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='created_polls'
    )
    
    question = models.TextField()
    poll_type = models.CharField(max_length=50, choices=POLL_TYPES)
    
    # Options for choice-based polls (JSON array)
    options = models.JSONField(
        default=list,
        blank=True,
        help_text="JSON array of poll options"
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    results_visible = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.question[:100]


class PollResponse(models.Model):
    """
    User responses to polls.
    """

    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='poll_responses'
    )
    
    # Response data
    selected_option = models.CharField(max_length=255, blank=True)
    text_response = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True)
    
    responded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('poll', 'user')

    def __str__(self):
        return f"Response to {self.poll.question[:50]}"


class QnA(models.Model):
    """
    Q&A system for sessions and events.
    """

    QNA_STATUS = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    event_session = models.ForeignKey(
        'events.EventSession',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='qna'
    )
    
    asked_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='asked_questions'
    )
    
    question = models.TextField()
    answer = models.TextField(blank=True)
    
    answered_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='answered_questions'
    )
    
    # Community engagement
    upvotes = models.PositiveIntegerField(default=0)
    
    # Status
    status = models.CharField(max_length=50, choices=QNA_STATUS, default='pending')
    is_featured = models.BooleanField(default=False)
    
    # Timestamps
    asked_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-upvotes', '-asked_at']

    def __str__(self):
        return self.question[:100]


class QnAUpvote(models.Model):
    """
    Track upvotes on Q&A questions/answers.
    """

    qna = models.ForeignKey(
        QnA,
        on_delete=models.CASCADE,
        related_name='upvoters'
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='qna_upvotes'
    )
    
    upvoted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('qna', 'user')


class SessionNote(models.Model):
    """
    Personal notes taken by attendees during sessions.
    """

    event_session = models.ForeignKey(
        'events.EventSession',
        on_delete=models.CASCADE,
        related_name='attendee_notes'
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='session_notes'
    )
    
    content = models.TextField()
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('event_session', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"Note by {self.user.email} on {self.event_session.name}"


class Feedback(models.Model):
    """
    Feedback on events, sessions, and overall experience.
    """

    FEEDBACK_TYPES = [
        ('event', 'Event'),
        ('session', 'Session'),
        ('overall', 'Overall'),
        ('speaker', 'Speaker'),
        ('venue', 'Venue'),
    ]

    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    feedback_type = models.CharField(max_length=50, choices=FEEDBACK_TYPES)
    
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='feedback'
    )
    
    session = models.ForeignKey(
        'events.EventSession',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='feedback'
    )
    
    given_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='given_feedback'
    )
    
    # Ratings
    overall_rating = models.IntegerField(choices=RATING_CHOICES)
    content_rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    organization_rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    venue_rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    
    # Comments
    comments = models.TextField(blank=True)
    suggestions = models.TextField(blank=True)
    
    given_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-given_at']

    def __str__(self):
        return f"Feedback from {self.given_by.email} - {self.get_feedback_type_display()}"
