from django.db import models


class Venue(models.Model):
    """
    Represents physical venues/locations where events take place.
    """

    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='venues'
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Location
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=255, default='Pakistan')
    
    # Coordinates for mapping
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # Capacity
    total_capacity = models.IntegerField()
    
    # Contact
    contact_name = models.CharField(max_length=255, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    
    # Media
    image = models.ImageField(upload_to='venue_images/', null=True, blank=True)
    
    # Floor plan
    floor_plan = models.FileField(upload_to='floor_plans/', null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('tenant', 'name')
        ordering = ['name']

    def __str__(self):
        return self.name


class VenueSpace(models.Model):
    """
    Represents physical spaces/areas within a venue (e.g., rooms, halls, areas).
    """

    SPACE_TYPES = [
        ('auditorium', 'Auditorium'),
        ('classroom', 'Classroom'),
        ('workshop_room', 'Workshop Room'),
        ('breakout_room', 'Breakout Room'),
        ('office', 'Office'),
        ('lounge', 'Lounge'),
        ('dining', 'Dining Area'),
        ('outdoor', 'Outdoor'),
    ]

    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        related_name='spaces'
    )
    
    name = models.CharField(max_length=255)
    space_type = models.CharField(max_length=50, choices=SPACE_TYPES)
    capacity = models.IntegerField()
    
    # Layout
    floor = models.IntegerField(default=1)
    layout_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="SVG layout and seat/booth data"
    )
    
    is_available = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('venue', 'name')
        ordering = ['floor', 'name']

    def __str__(self):
        return f"{self.venue.name} - {self.name}"


class Seating(models.Model):
    """
    Individual seats/positions within a venue space.
    """

    SEATING_TYPES = [
        ('seat', 'Seat'),
        ('booth', 'Booth'),
        ('zone', 'Zone'),
        ('standing', 'Standing Area'),
    ]

    OCCUPANCY_STATUS = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
    ]

    space = models.ForeignKey(
        VenueSpace,
        on_delete=models.CASCADE,
        related_name='seating'
    )
    
    seat_number = models.CharField(max_length=20)
    seating_type = models.CharField(max_length=50, choices=SEATING_TYPES, default='seat')
    row = models.CharField(max_length=10)
    column = models.IntegerField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=50, choices=OCCUPANCY_STATUS, default='available')
    
    # Assignment
    assigned_to = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_seats'
    )
    assigned_at = models.DateTimeField(null=True, blank=True)
    
    # Coordinates for map visualization
    x_coordinate = models.FloatField(null=True, blank=True)
    y_coordinate = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('space', 'seat_number')
        ordering = ['row', 'column']

    def __str__(self):
        return f"{self.space.name} - {self.seat_number}"
