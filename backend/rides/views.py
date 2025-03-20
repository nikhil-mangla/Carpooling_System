import os
import googlemaps
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import generics, views
from rest_framework.response import Response
from .models import Ride, RideRequest
from .serializers import RideSerializer, RideRequestSerializer
from geopy.distance import geodesic


class RideListCreateView(generics.ListCreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

    def perform_create(self, serializer):
        ride = serializer.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'rides',
            {
                'type': 'ride_created',
                'ride': RideSerializer(ride).data,
            }
        )


class RouteMatchView(views.APIView):
    def get(self, request):
        gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))

        try:
            rider_pickup_lat = float(request.query_params.get('pickup_lat'))
            rider_pickup_lng = float(request.query_params.get('pickup_lng'))
            rider_dropoff_lat = float(request.query_params.get('dropoff_lat'))
            rider_dropoff_lng = float(request.query_params.get('dropoff_lng'))

            rider_route_response = gmaps.directions(
                (rider_pickup_lat, rider_pickup_lng),
                (rider_dropoff_lat, rider_dropoff_lng),
                mode="driving"
            )

            if not rider_route_response:
                return Response({"error": "No route found"}, status=400)

            rider_route = rider_route_response[0]['overview_polyline']['points']

            rides = Ride.objects.all()
            matches = []

            for ride in rides:
                driver_route_response = gmaps.directions(
                    (ride.pickup_lat, ride.pickup_lng),
                    (ride.dropoff_lat, ride.dropoff_lng),
                    mode="driving"
                )

                if not driver_route_response:
                    continue  # Skip if no route found

                driver_route = driver_route_response[0]['overview_polyline']['points']
                overlap = len(set(rider_route).intersection(driver_route)) / len(rider_route) * 100

                matches.append({
                    'ride': RideSerializer(ride).data,
                    'match_percentage': min(100, max(0, overlap))
                })

            return Response(matches)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class RideRequestCreateView(generics.CreateAPIView):
    queryset = RideRequest.objects.all()
    serializer_class = RideRequestSerializer

    def perform_create(self, serializer):
        ride_request = serializer.save()

        if ride_request.ride.driver.phone_number:
            client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
            call = client.calls.create(
                to=ride_request.ride.driver.phone_number,
                from_=os.getenv('TWILIO_PHONE_NUMBER'),
                url=f'{os.getenv("BASE_URL")}/api/twilio-callback/'
            )
            print(f'Twilio Call SID: {call.sid}')


class InitiateCallView(views.APIView):
    def post(self, request):
        to_number = request.data.get('to')
        if not to_number:
            return Response({'error': 'Missing "to" field'}, status=400)

        client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
        call = client.calls.create(
            to=to_number,
            from_=os.getenv('TWILIO_PHONE_NUMBER'),
            url=f'{request.scheme}://{request.get_host()}/api/twilio-callback/'
        )
        return Response({'sid': call.sid})


class TwilioCallbackView(views.APIView):
    def post(self, request):
        response = VoiceResponse()
        response.dial(request.POST.get('to'), caller_id=os.getenv('TWILIO_PHONE_NUMBER'))
        return Response(str(response), content_type='text/xml')