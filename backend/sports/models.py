from django.db import models
from django.utils.text import slugify


class Sport(models.Model):
    """
    Represents a sport/athletic competition offered in the olympiad.
    """

    SPORT_TYPES = [
        ('individual', 'Individual'),
        ('team', 'Team'),
        ('mixed', 'Mixed'),
    ]

    olympiad = models.ForeignKey(
        'olympiad_core.Olympiad',
        on_delete=models.CASCADE,
        related_name='sports'
    )
    
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    sport_type = models.CharField(max_length=50, choices=SPORT_TYPES)
    
    # Categories
    categories = models.ManyToManyField(
        'olympiad_core.Category',
        related_name='sports',
        blank=True
    )
    
    # Organizing society
    organizing_society = models.ForeignKey(
        'societies.Society',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='organized_sports'
    )
    
    # Collaborating societies
    collaborating_societies = models.ManyToManyField(
        'societies.Society',
        related_name='collaborated_sports',
        blank=True
    )
    
    # Rules
    rules_document = models.FileField(upload_to='sport_rules/', null=True, blank=True)
    
    # Registration
    max_participants = models.IntegerField(default=50)
    min_team_size = models.IntegerField(default=1)
    max_team_size = models.IntegerField(default=15)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Schedule
    event_date = models.DateTimeField()
    registration_start = models.DateTimeField()
    registration_end = models.DateTimeField()
    
    # Venue
    venue = models.ForeignKey(
        'venues.Venue',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sports'
    )
    
    # Media
    banner = models.ImageField(upload_to='sport_banners/', null=True, blank=True)
    
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
        return f"{self.name} ({self.get_sport_type_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SportMatch(models.Model):
    """
    Individual matches/games in a sport.
    """

    MATCH_STATUS = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('postponed', 'Postponed'),
    ]

    sport = models.ForeignKey(
        Sport,
        on_delete=models.CASCADE,
        related_name='matches'
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Teams/Participants
    team_a = models.ForeignKey(
        'registrations.Team',
        on_delete=models.CASCADE,
        related_name='matches_as_team_a',
        null=True,
        blank=True
    )
    team_b = models.ForeignKey(
        'registrations.Team',
        on_delete=models.CASCADE,
        related_name='matches_as_team_b',
        null=True,
        blank=True
    )
    
    # Schedule & Venue
    scheduled_time = models.DateTimeField()
    venue = models.ForeignKey(
        'venues.Venue',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sport_matches'
    )
    
    # Results
    status = models.CharField(max_length=50, choices=MATCH_STATUS, default='scheduled')
    team_a_score = models.IntegerField(null=True, blank=True)
    team_b_score = models.IntegerField(null=True, blank=True)
    winner = models.ForeignKey(
        'registrations.Team',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='won_matches'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['scheduled_time']

    def __str__(self):
        return f"{self.name} - {self.sport.name}"


class SportRanking(models.Model):
    """
    Final rankings and medals for sports.
    """

    MEDAL_TYPES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
    ]

    sport = models.ForeignKey(
        Sport,
        on_delete=models.CASCADE,
        related_name='rankings'
    )
    team = models.ForeignKey(
        'registrations.Team',
        on_delete=models.CASCADE,
        related_name='sport_rankings'
    )
    
    rank = models.IntegerField()
    medal = models.CharField(max_length=50, choices=MEDAL_TYPES, null=True, blank=True)
    points = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sport', 'team')
        ordering = ['rank']

    def __str__(self):
        return f"{self.team.name} - {self.sport.name} (Rank: {self.rank})"
