from django.db import models
from django.contrib.auth.models import User

class Ride(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    pickup_lat = models.FloatField()
    pickup_lng = models.FloatField()
    dropoff_lat = models.FloatField()
    dropoff_lng = models.FloatField()
    departure_time = models.DateTimeField()
    available_seats = models.IntegerField(default=3)

    def __str__(self):
        return f'Ride from {self.pickup_location} to {self.dropoff_location}'

class RideRequest(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    requester_name = models.CharField(max_length=100)
    requester_phone = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted')])

    def __str__(self):
        return f'Request by {self.requester_name} for {self.ride}'