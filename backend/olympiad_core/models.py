from django.db import models
from django.utils.text import slugify


class Olympiad(models.Model):
    """
    Core Olympiad model representing a specific olympiad/competition event.
    """

    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='olympiads'
    )
    
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    
    # Event dates
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_start = models.DateTimeField()
    registration_end = models.DateTimeField()
    
    # Organization
    organizer = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='organized_olympiads'
    )
    
    # Branding & Media
    banner = models.ImageField(upload_to='olympiad_banners/', null=True, blank=True)
    logo = models.ImageField(upload_to='olympiad_logos/', null=True, blank=True)
    max_participants = models.IntegerField(default=1000)
    
    # Status
    is_published = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('tenant', 'slug')
        ordering = ['-start_date']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    """
    Categories for competitions (e.g., Age groups, skill levels).
    """

    CATEGORY_TYPES = [
        ('age_group', 'Age Group'),
        ('skill_level', 'Skill Level'),
        ('gender', 'Gender'),
        ('organization', 'Organization Type'),
    ]

    olympiad = models.ForeignKey(
        Olympiad,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    
    name = models.CharField(max_length=255)
    category_type = models.CharField(max_length=50, choices=CATEGORY_TYPES)
    description = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('olympiad', 'name', 'category_type')
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"
