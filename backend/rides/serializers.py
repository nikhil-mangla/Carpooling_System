from rest_framework import serializers
from .models import Ride, RideRequest

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'pickup_location', 'dropoff_location', 'pickup_lat', 'pickup_lng', 
                  'dropoff_lat', 'dropoff_lng', 'departure_time', 'available_seats', 'driver', 'created_at']

class RideRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideRequest
        fields = ['id', 'ride', 'requester_name', 'requester_phone', 'status', 'created_at']