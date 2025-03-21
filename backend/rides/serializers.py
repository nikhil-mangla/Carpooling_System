from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Ride, RideRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # Password should not be readable
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'pickup_location', 'dropoff_location', 'pickup_lat', 'pickup_lng', 
                  'dropoff_lat', 'dropoff_lng', 'departure_time', 'available_seats', 'driver', 'created_at']

class RideRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideRequest
        fields = ['id', 'ride', 'requester_name', 'requester_phone', 'status', 'created_at']