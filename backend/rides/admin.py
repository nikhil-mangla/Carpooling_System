from django.contrib import admin
from .models import Ride, RideRequest, UserProfile

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('pickup_location', 'dropoff_location', 'departure_time', 'driver', 'available_seats')
    list_filter = ('departure_time', 'driver')
    search_fields = ('pickup_location', 'dropoff_location')

@admin.register(RideRequest)
class RideRequestAdmin(admin.ModelAdmin):
    list_display = ('requester_name', 'ride', 'status', 'requester_phone')
    list_filter = ('status',)
    search_fields = ('requester_name', 'requester_phone')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')