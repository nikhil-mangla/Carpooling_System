import os
import logging
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Ride, RideRequest
from .serializers import RideSerializer, RideRequestSerializer, UserSerializer
from geopy.distance import geodesic
from django.utils import timezone
from rest_framework.views import APIView

# Set up logging
logger = logging.getLogger(__name__)

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

class RouteMatchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info("Starting RouteMatchView.get")
        try:
            pickup_lat = float(request.query_params.get('pickup_lat'))
            pickup_lng = float(request.query_params.get('pickup_lng'))
            dropoff_lat = float(request.query_params.get('dropoff_lat'))
            dropoff_lng = float(request.query_params.get('dropoff_lng'))
            logger.info(f"Query params: pickup_lat={pickup_lat}, pickup_lng={pickup_lng}, dropoff_lat={dropoff_lat}, dropoff_lng={dropoff_lng}")
        except (TypeError, ValueError) as e:
            logger.error(f"Error parsing query params: {e}")
            return Response({"error": "Invalid or missing coordinates"}, status=400)

        # Get all rides that haven't departed yet
        logger.info("Fetching rides from database")
        rides = Ride.objects.filter(departure_time__gte=timezone.now())
        logger.info(f"Found {rides.count()} rides")

        if not rides:
            logger.info("No rides available")
            return Response({"message": "No rides available"}, status=200)

        # Calculate distances and match percentage
        matches = []
        for ride in rides:
            logger.info(f"Processing ride ID {ride.id}")
            try:
                # Calculate distances using geodesic
                pickup_distance = geodesic(
                    (pickup_lat, pickup_lng),
                    (ride.pickup_lat, ride.pickup_lng)
                ).km
                dropoff_distance = geodesic(
                    (dropoff_lat, dropoff_lng),
                    (ride.dropoff_lat, ride.dropoff_lng)
                ).km
                logger.info(f"Ride {ride.id}: pickup_distance={pickup_distance}, dropoff_distance={dropoff_distance}")

                # Simple match percentage (lower distance = better match)
                max_distance = 50  # km
                match_percentage = max(0, 100 - ((pickup_distance + dropoff_distance) / max_distance) * 100)

                if match_percentage > 0:  # Only include rides with a positive match
                    matches.append({
                        "ride": {
                            "id": ride.id,
                            "pickup_location": ride.pickup_location,
                            "dropoff_location": ride.dropoff_location,
                            "pickup_lat": ride.pickup_lat,
                            "pickup_lng": ride.pickup_lng,
                            "dropoff_lat": ride.dropoff_lat,
                            "dropoff_lng": ride.dropoff_lng,
                            "departure_time": ride.departure_time.isoformat(),
                            "available_seats": ride.available_seats,
                            "driver": ride.driver.id,
                            "created_at": ride.created_at.isoformat(),
                        },
                        "match_percentage": match_percentage,
                        "pickup_distance_km": pickup_distance,
                        "dropoff_distance_km": dropoff_distance,
                    })
            except Exception as e:
                logger.error(f"Error processing ride ID {ride.id}: {e}")
                return Response({"error": f"Error calculating distances: {str(e)}"}, status=500)

        logger.info(f"Returning {len(matches)} matches")
        matches.sort(key=lambda x: x["match_percentage"], reverse=True)
        return Response(matches, status=200)

class RideRequestCreateView(generics.CreateAPIView):
    queryset = RideRequest.objects.all()
    serializer_class = RideRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        ride_request = serializer.save()
        # Check if Twilio environment variables are set
        twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        base_url = os.getenv('BASE_URL', 'https://carpooling-backend1.onrender.com')

        if not all([twilio_account_sid, twilio_auth_token, twilio_phone_number]):
            logger.warning("Twilio environment variables are not set. Skipping call initiation.")
            return

        try:
            # Check if the driver has a phone number
            driver_phone = None
            if hasattr(ride_request.ride.driver, 'profile') and hasattr(ride_request.ride.driver.profile, 'phone_number'):
                driver_phone = ride_request.ride.driver.profile.phone_number
            else:
                logger.warning("Driver has no phone number configured")
                return

            client = Client(twilio_account_sid, twilio_auth_token)
            call = client.calls.create(
                to=driver_phone,
                from_=twilio_phone_number,
                url=f'{base_url}/api/twilio-callback/'
            )
            logger.info(f'Twilio Call SID: {call.sid}')
        except Exception as e:
            logger.error(f"Twilio error: {str(e)}")

class InitiateCallView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        to_number = request.data.get('to')
        if not to_number:
            return Response({'error': 'Missing "to" field'}, status=400)

        # Check if Twilio environment variables are set
        twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')

        if not all([twilio_account_sid, twilio_auth_token, twilio_phone_number]):
            return Response({'error': 'Twilio environment variables are not set'}, status=500)

        try:
            client = Client(twilio_account_sid, twilio_auth_token)
            call = client.calls.create(
                to=to_number,
                from_=twilio_phone_number,
                url=f'{request.scheme}://{request.get_host()}/api/twilio-callback/'
            )
            logger.info(f"Initiated call with SID: {call.sid}")
            return Response({'sid': call.sid}, status=200)
        except Exception as e:
            logger.error(f"Twilio error in InitiateCallView: {str(e)}")
            return Response({'error': str(e)}, status=500)

class TwilioCallbackView(views.APIView):
    def post(self, request):
        response = VoiceResponse()
        # Twilio sends the 'To' number in the request body (case-sensitive)
        to_number = request.POST.get('To')
        if to_number:
            response.dial(to_number, caller_id=os.getenv('TWILIO_PHONE_NUMBER'))
            logger.info(f"Twilio callback: Dialing {to_number}")
        else:
            response.say("No number provided for the call.")
            logger.warning("Twilio callback: No 'To' number provided")
        return Response(str(response), content_type='text/xml')