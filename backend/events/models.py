from django.db import models
from django.utils.text import slugify


class Event(models.Model):
    """
    Event model for hosting sessions, workshops, and general gatherings.
    Can be associated with an olympiad or standalone.
    """

    EVENT_TYPES = [
        ('workshop', 'Workshop'),
        ('session', 'Session'),
        ('panel', 'Panel Discussion'),
        ('networking', 'Networking'),
        ('opening', 'Opening Ceremony'),
        ('closing', 'Closing Ceremony'),
        ('keynote', 'Keynote'),
    ]

    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='events'
    )
    
    olympiad = models.ForeignKey(
        'olympiad_core.Olympiad',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
    )
    
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    
    # Details
    content = models.TextField(blank=True, help_text="Detailed event content/description")
    
    # Schedule
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    # Location
    venue = models.ForeignKey(
        'venues.Venue',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
    )
    
    # Speaker/Host
    speaker = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hosted_events'
    )
    
    # Capacity and Registration
    max_capacity = models.IntegerField(default=100)
    current_capacity = models.IntegerField(default=0)
    registration_required = models.BooleanField(default=False)
    
    # Media
    thumbnail = models.ImageField(upload_to='event_thumbnails/', null=True, blank=True)
    
    # Status
    is_published = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('tenant', 'slug')
        ordering = ['-start_time']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class EventAttendance(models.Model):
    """
    Track attendance for events.
    """

    ATTENDANCE_STATUS = [
        ('registered', 'Registered'),
        ('checked_in', 'Checked In'),
        ('marked_absent', 'Marked Absent'),
        ('cancelled', 'Cancelled'),
    ]

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='event_attendances'
    )
    
    status = models.CharField(max_length=50, choices=ATTENDANCE_STATUS, default='registered')
    
    # Check-in details
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_in_method = models.CharField(
        max_length=50,
        choices=[('qr', 'QR Code'), ('manual', 'Manual'), ('mobile_app', 'Mobile App')],
        null=True,
        blank=True
    )
    
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('event', 'user')
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.user.email} - {self.event.name}"


class EventSession(models.Model):
    """
    Represents breakout sessions or sub-events within a main event.
    """

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Schedule
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    # Room/Venue
    room = models.CharField(max_length=255, blank=True)
    
    # Speaker
    speaker = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sessions_led'
    )
    
    # Capacity
    max_capacity = models.IntegerField(default=50)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.event.name} - {self.name}"


class TicketType(models.Model):
    """
    Ticket types and pricing for events.
    """

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='ticket_types'
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.IntegerField()
    quantity_sold = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return f"{self.event.name} - {self.name}"
