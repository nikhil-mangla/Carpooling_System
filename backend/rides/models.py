from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Ride(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_driver')
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    pickup_lat = models.FloatField(default=0.0)
    pickup_lng = models.FloatField(default=0.0)
    dropoff_lat = models.FloatField(default=0.0)
    dropoff_lng = models.FloatField(default=0.0)
    departure_time = models.DateTimeField()
    available_seats = models.IntegerField(default=3, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ride from {self.pickup_location} to {self.dropoff_location}'

    class Meta:
        indexes = [
            models.Index(fields=['departure_time'], name='ride_departure_idx'),
            models.Index(fields=['driver'], name='ride_driver_idx'),
        ]

class RideRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('canceled', 'Canceled'),
    ]
    
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='requests')
    requester_name = models.CharField(max_length=100)
    requester_phone = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Request by {self.requester_name} for {self.ride}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"