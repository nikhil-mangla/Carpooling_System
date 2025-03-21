import os
import googlemaps
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Ride, RideRequest
from .serializers import RideSerializer, RideRequestSerializer,UserSerializer
from geopy.distance import geodesic


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": {
                "username": user.username,
                "email": user.email
            },
            "message": "User created successfully"
        }, status=status.HTTP_201_CREATED)

class RideListCreateView(generics.ListCreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        ride = serializer.save(driver=self.request.user)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'rides',
            {
                'type': 'ride_created',
                'ride': RideSerializer(ride).data,
            }
        )

class RouteMatchView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))
        try:
            rider_pickup_lat = float(request.query_params.get('pickup_lat'))
            rider_pickup_lng = float(request.query_params.get('pickup_lng'))
            rider_dropoff_lat = float(request.query_params.get('dropoff_lat'))
            rider_dropoff_lng = float(request.query_params.get('dropoff_lng'))

            rider_coords = (rider_pickup_lat, rider_pickup_lng)
            rider_dropoff_coords = (rider_dropoff_lat, rider_dropoff_lng)

            rides = Ride.objects.all()
            matches = []

            for ride in rides:
                driver_pickup_coords = (ride.pickup_lat, ride.pickup_lng)
                driver_dropoff_coords = (ride.dropoff_lat, ride.dropoff_lng)

                # Check proximity (within 5km)
                pickup_distance = geodesic(rider_coords, driver_pickup_coords).km
                dropoff_distance = geodesic(rider_dropoff_coords, driver_dropoff_coords).km

                if pickup_distance < 5 and dropoff_distance < 5:
                    driver_route_response = gmaps.directions(
                        driver_pickup_coords,
                        driver_dropoff_coords,
                        mode="driving"
                    )
                    if not driver_route_response:
                        continue

                    driver_route = driver_route_response[0]['overview_polyline']['points']
                    rider_route_response = gmaps.directions(rider_coords, rider_dropoff_coords, mode="driving")
                    if not rider_route_response:
                        continue

                    rider_route = rider_route_response[0]['overview_polyline']['points']
                    overlap = len(set(rider_route).intersection(driver_route)) / len(rider_route) * 100

                    matches.append({
                        'ride': RideSerializer(ride).data,
                        'match_percentage': min(100, max(0, overlap)),
                        'pickup_distance_km': pickup_distance,
                        'dropoff_distance_km': dropoff_distance,
                    })

            return Response(matches)

        except ValueError as e:
            return Response({"error": "Invalid coordinates"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class RideRequestCreateView(generics.CreateAPIView):
    queryset = RideRequest.objects.all()
    serializer_class = RideRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        ride_request = serializer.save()
        try:
            # Assumes User has a related profile with phone_number
            driver_phone = ride_request.ride.driver.profile.phone_number
            if driver_phone:
                client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
                call = client.calls.create(
                    to=driver_phone,
                    from_=os.getenv('TWILIO_PHONE_NUMBER'),
                    url=f'{os.getenv("BASE_URL", "https://your-app-name.onrender.com")}/api/twilio-callback/'
                )
                print(f'Twilio Call SID: {call.sid}')
        except AttributeError:
            print("Driver has no phone number configured")
        except Exception as e:
            print(f"Twilio error: {str(e)}")

class InitiateCallView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        to_number = request.data.get('to')
        if not to_number:
            return Response({'error': 'Missing "to" field'}, status=400)

        try:
            client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
            call = client.calls.create(
                to=to_number,
                from_=os.getenv('TWILIO_PHONE_NUMBER'),
                url=f'{request.scheme}://{request.get_host()}/api/twilio-callback/'
            )
            return Response({'sid': call.sid})
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class TwilioCallbackView(views.APIView):
    def post(self, request):
        response = VoiceResponse()
        to_number = request.POST.get('to')
        if to_number:
            response.dial(to_number, caller_id=os.getenv('TWILIO_PHONE_NUMBER'))
        else:
            response.say("No number provided for the call.")
        return Response(str(response), content_type='text/xml')