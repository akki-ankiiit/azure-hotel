from django.db import models


class Room(models.Model):
    ROOM_TYPES = [
        ('Standard', 'Standard'),
        ('Deluxe', 'Deluxe'),
        ('Suite', 'Suite'),
        ('Presidential', 'Presidential'),
    ]
    BED_TYPES = [
        ('Single Bed', 'Single Bed'),
        ('Double Bed', 'Double Bed'),
        ('King Bed', 'King Bed'),
        ('Queen Bed', 'Queen Bed'),
        ('Twin Beds', 'Twin Beds'),
    ]
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='Standard')
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    size_sqm = models.PositiveIntegerField(default=30)
    bed_type = models.CharField(max_length=20, choices=BED_TYPES, default='King Bed')
    max_guests = models.PositiveIntegerField(default=2)
    amenities = models.TextField(blank=True, help_text="Comma-separated list of amenities")
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type})"

    def get_amenities_list(self):
        return [a.strip() for a in self.amenities.split(',') if a.strip()]


class Guest(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    LOYALTY_TIERS = [
        ('None', 'None'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
        ('Elite', 'Elite'),
    ]
    guest_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    passport_number = models.CharField(max_length=20, blank=True)
    loyalty_status = models.CharField(max_length=20, choices=LOYALTY_TIERS, default='None')
    loyalty_tier = models.CharField(max_length=20, blank=True)
    points_balance = models.PositiveIntegerField(default=0)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.guest_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Checked-In', 'Checked-In'),
        ('Checked-Out', 'Checked-Out'),
        ('Cancelled', 'Cancelled'),
    ]
    booking_id = models.CharField(max_length=20, unique=True)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='bookings')
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    num_adults = models.PositiveIntegerField(default=1)
    num_children = models.PositiveIntegerField(default=0)
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    # Amenities
    complimentary_breakfast = models.BooleanField(default=False)
    free_wifi = models.BooleanField(default=False)
    gym_pool_access = models.BooleanField(default=False)
    transportation = models.CharField(max_length=100, blank=True)
    # Billing
    extras_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    vat_percent = models.DecimalField(max_digits=5, decimal_places=2, default=8)
    city_tax = models.DecimalField(max_digits=8, decimal_places=2, default=49.50)
    billing_notes = models.TextField(blank=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.booking_id} – {self.guest.full_name}"

    @property
    def num_nights(self):
        delta = self.check_out - self.check_in
        return max(delta.days, 1)

    @property
    def room_total(self):
        if self.room:
            return self.room.price_per_night * self.num_nights
        return 0

    @property
    def vat_amount(self):
        return round(float(self.room_total) * float(self.vat_percent) / 100, 2)

    @property
    def total_price(self):
        return round(float(self.room_total) + float(self.extras_amount) + float(self.vat_amount) + float(self.city_tax), 2)
