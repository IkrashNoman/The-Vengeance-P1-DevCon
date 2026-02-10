from django.db import models
from django.utils.text import slugify


class Module(models.Model):
    """
    Represents a module/competition in the olympiad.
    Can be technical or non-technical, organized by societies.
    """

    MODULE_TYPES = [
        ('technical', 'Technical'),
        ('non_technical', 'Non-Technical'),
    ]

    olympiad = models.ForeignKey(
        'olympiad_core.Olympiad',
        on_delete=models.CASCADE,
        related_name='modules'
    )
    
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    module_type = models.CharField(max_length=50, choices=MODULE_TYPES)
    
    # Categories
    categories = models.ManyToManyField(
        'olympiad_core.Category',
        related_name='modules',
        blank=True
    )
    
    # Organizing society
    organizing_society = models.ForeignKey(
        'societies.Society',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='organized_modules'
    )
    
    # Collaborating societies
    collaborating_societies = models.ManyToManyField(
        'societies.Society',
        related_name='collaborated_modules',
        blank=True
    )
    
    # Details
    description = models.TextField(blank=True)
    rules_document = models.FileField(upload_to='module_rules/', null=True, blank=True)
    max_participants = models.IntegerField(default=100)
    min_team_size = models.IntegerField(default=1)
    max_team_size = models.IntegerField(default=5)
    
    # Fees
    participation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Schedule
    event_date = models.DateTimeField()
    registration_start = models.DateTimeField()
    registration_end = models.DateTimeField()
    
    # Media
    banner = models.ImageField(upload_to='module_banners/', null=True, blank=True)
    
    # Status
    is_published = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('olympiad', 'slug')
        ordering = ['event_date']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ModuleRound(models.Model):
    """
    Represents rounds/stages in a module competition.
    """

    ROUND_TYPES = [
        ('preliminary', 'Preliminary'),
        ('semi_final', 'Semi-Final'),
        ('final', 'Final'),
        ('qualifying', 'Qualifying'),
    ]

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='rounds'
    )
    
    name = models.CharField(max_length=255)
    round_type = models.CharField(max_length=50, choices=ROUND_TYPES)
    description = models.TextField(blank=True)
    
    # Schedule
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    venue = models.ForeignKey(
        'venues.Venue',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='module_rounds'
    )
    
    # Details
    max_advancement = models.IntegerField(null=True, blank=True, help_text="Teams advancing to next round")
    
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('module', 'name')
        ordering = ['order', 'start_time']

    def __str__(self):
        return f"{self.module.name} - {self.name}"


class Judge(models.Model):
    """
    Judges/Evaluators for module rounds.
    """

    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='judge_profile'
    )
    
    expertise = models.JSONField(default=list, help_text="JSON array of expertise areas")
    bio = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Judge: {self.user.get_full_name()}"


class RoundJudge(models.Model):
    """
    Maps judges to rounds.
    """

    round = models.ForeignKey(
        ModuleRound,
        on_delete=models.CASCADE,
        related_name='judges'
    )
    judge = models.ForeignKey(
        Judge,
        on_delete=models.CASCADE,
        related_name='round_assignments'
    )
    
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('round', 'judge')

    def __str__(self):
        return f"{self.judge.user.get_full_name()} judging {self.round.name}"
