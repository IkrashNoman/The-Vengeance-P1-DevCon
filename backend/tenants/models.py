from django.db import models
from django.utils.text import slugify


class Tenant(models.Model):
    """
    Multi-tenant model to support multiple organizations/olympiads.
    Each tenant represents a separate event instance or organization.
    """

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    # Branding
    logo = models.ImageField(upload_to='tenant_logos/', null=True, blank=True)
    primary_color = models.CharField(max_length=7, default='#0066cc')
    secondary_color = models.CharField(max_length=7, default='#333333')
    
    # Organization details
    owner = models.ForeignKey(
        'accounts.User',
        on_delete=models.PROTECT,
        related_name='owned_tenants'
    )
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Settings
    max_events = models.IntegerField(default=100, help_text="Maximum events this tenant can create")
    max_users = models.IntegerField(default=10000, help_text="Maximum users for this tenant")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
