from django.db import models
from django.utils.text import slugify


class Society(models.Model):
    """
    Represents a society/club that organizes modules and sports.
    Acts as a container for organizing events within the olympiad.
    """

    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='societies'
    )
    
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    
    # Leadership
    president = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='presided_societies'
    )
    vice_president = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vice_presided_societies'
    )
    
    # Contact
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Media
    logo = models.ImageField(upload_to='society_logos/', null=True, blank=True)
    banner = models.ImageField(upload_to='society_banners/', null=True, blank=True)
    
    # Status and Metadata
    is_active = models.BooleanField(default=True)
    founded_year = models.IntegerField(null=True, blank=True)
    member_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('tenant', 'slug')
        ordering = ['name']
        verbose_name_plural = "Societies"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SocietyMember(models.Model):
    """
    Links users to societies with specific roles/positions.
    """

    POSITION_CHOICES = [
        ('president', 'President'),
        ('vice_president', 'Vice President'),
        ('treasurer', 'Treasurer'),
        ('secretary', 'Secretary'),
        ('coordinator', 'Coordinator'),
        ('member', 'Member'),
        ('core_member', 'Core Member'),
    ]

    society = models.ForeignKey(
        Society,
        on_delete=models.CASCADE,
        related_name='members'
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='society_memberships'
    )
    
    position = models.CharField(max_length=50, choices=POSITION_CHOICES, default='member')
    
    # Tenure
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Additional fields
    bio = models.TextField(blank=True)

    class Meta:
        unique_together = ('society', 'user')
        ordering = ['-joined_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.society.name} ({self.get_position_display()})"
