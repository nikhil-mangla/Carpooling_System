from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ride, RideRequest
from datetime import datetime

class RideModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.ride = Ride.objects.create(
            driver=self.user,
            pickup_location='A',
            dropoff_location='B',
            pickup_lat=1.0,
            pickup_lng=1.0,
            dropoff_lat=2.0,
            dropoff_lng=2.0,
            departure_time=datetime(2025, 3, 21, 12, 0),
            available_seats=3
        )

    def test_ride_creation(self):
        self.assertEqual(str(self.ride), 'Ride from A to B')
        self.assertEqual(self.ride.available_seats, 3)

    def test_ride_request_creation(self):
        request = RideRequest.objects.create(
            ride=self.ride,
            requester_name='John Doe',
            requester_phone='1234567890',
            status='pending'
        )
        self.assertEqual(str(request), f'Request by John Doe for {self.ride}')