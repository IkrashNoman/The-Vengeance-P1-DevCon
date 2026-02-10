from django.db import models


class ChatbotKnowledgeBase(models.Model):
    """
    Knowledge base for RAG-powered chatbot.
    Contains event-specific information and FAQs.
    """

    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='chatbot_knowledge_base'
    )
    
    olympiad = models.ForeignKey(
        'olympiad_core.Olympiad',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='chatbot_documents'
    )
    
    # Document content
    title = models.CharField(max_length=500)
    content = models.TextField()
    category = models.CharField(
        max_length=255,
        choices=[
            ('faq', 'FAQ'),
            ('schedule', 'Schedule'),
            ('venue', 'Venue'),
            ('registration', 'Registration'),
            ('logistics', 'Logistics'),
            ('speakers', 'Speakers'),
            ('rules', 'Rules'),
            ('other', 'Other'),
        ],
        default='other'
    )
    
    # Metadata
    tags = models.JSONField(default=list, blank=True)
    is_published = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'title']

    def __str__(self):
        return f"{self.category}: {self.title}"


class ChatbotConversation(models.Model):
    """
    Tracks chatbot conversations with users.
    """

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='chatbot_conversations'
    )
    
    olympiad = models.ForeignKey(
        'olympiad_core.Olympiad',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='chatbot_conversations'
    )
    
    # Conversation metadata
    session_id = models.CharField(max_length=255, unique=True)
    summary = models.TextField(blank=True)
    sentiment = models.CharField(
        max_length=50,
        choices=[('positive', 'Positive'), ('neutral', 'Neutral'), ('negative', 'Negative')],
        default='neutral'
    )
    
    # Engagement
    message_count = models.IntegerField(default=0)
    resolution_status = models.CharField(
        max_length=50,
        choices=[('open', 'Open'), ('resolved', 'Resolved'), ('escalated', 'Escalated')],
        default='open'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Chatbot conversation with {self.user.email}"


class ChatbotMessage(models.Model):
    """
    Individual messages in chatbot conversations.
    """

    MESSAGE_TYPES = [
        ('user', 'User'),
        ('bot', 'Bot'),
    ]

    conversation = models.ForeignKey(
        ChatbotConversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    
    message_type = models.CharField(max_length=50, choices=MESSAGE_TYPES)
    content = models.TextField()
    
    # Bot response details
    confidence_score = models.FloatField(null=True, blank=True)
    retrieved_documents = models.JSONField(
        default=list,
        blank=True,
        help_text="IDs of documents used for RAG retrieval"
    )
    
    # User feedback
    is_helpful = models.BooleanField(null=True, blank=True)
    feedback_text = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.get_message_type_display()}: {self.content[:50]}"


class ChatbotIntentResponse(models.Model):
    """
    Pre-configured responses and intents for common questions.
    """

    INTENT_TYPES = [
        ('schedule', 'What is the schedule?'),
        ('venue', 'Where is the venue?'),
        ('registration', 'How do I register?'),
        ('payment', 'Payment related'),
        ('rules', 'What are the rules?'),
        ('speakers', 'Tell me about speakers'),
        ('accommodation', 'Accommodation info'),
        ('transport', 'Transport info'),
        ('general', 'General query'),
    ]

    olympiad = models.ForeignKey(
        'olympiad_core.Olympiad',
        on_delete=models.CASCADE,
        related_name='chatbot_intents'
    )
    
    intent = models.CharField(max_length=255, choices=INTENT_TYPES)
    keywords = models.JSONField(default=list, help_text="Keywords to trigger this intent")
    
    response_template = models.TextField()
    
    # Context
    context_required = models.JSONField(
        default=list,
        blank=True,
        help_text="Required context/variables for response"
    )
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('olympiad', 'intent')
        ordering = ['intent']

    def __str__(self):
        return f"{self.olympiad.name}: {self.get_intent_display()}"
