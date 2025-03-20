import { useSession } from 'next-auth/react';
import { useState, useEffect } from 'react';
import { TextField, Button, Typography } from '@mui/material';
import { LoadScript, Autocomplete } from '@react-google-maps/api';
import { io, Socket } from 'socket.io-client';
import axios from 'axios';

// WebSocket connection
const socket: Socket = io(process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');

const libraries: ("places")[] = ['places'];

interface Ride {
  id: number;
  pickup_location: string;
  dropoff_location: string;
  pickup_lat: number;
  pickup_lng: number;
  dropoff_lat: number;
  dropoff_lng: number;
  departure_time: string;
  available_seats: number;
  driver: number;
  rider_phone?: string;
}

export default function CreateRide() {
  const { data: session } = useSession();
  const [pickup, setPickup] = useState('');
  const [dropoff, setDropoff] = useState('');
  const [pickupLatLng, setPickupLatLng] = useState<{ lat: number; lng: number } | null>(null);
  const [dropoffLatLng, setDropoffLatLng] = useState<{ lat: number; lng: number } | null>(null);
  const [newRide, setNewRide] = useState<Ride | null>(null);

  useEffect(() => {
    socket.on('connect', () => console.log('WebSocket connected'));
    socket.on('ride_created', (ride: Ride) => {
      console.log('New ride:', ride);
      setNewRide(ride);
    });

    return () => {
      socket.off('ride_created');
      socket.disconnect();
    };
  }, []);

  const handleSubmit = async () => {
    if (!pickupLatLng || !dropoffLatLng) {
      alert('Please select both pickup and drop-off locations.');
      return;
    }

    if (!session?.accessToken) {
      alert('You need to be logged in to create a ride.');
      return;
    }

    try {
      const response = await axios.post<Ride>(
        `${process.env.NEXT_PUBLIC_API_URL}/api/rides/`,
        {
          pickup_location: pickup,
          dropoff_location: dropoff,
          pickup_lat: pickupLatLng.lat,
          pickup_lng: pickupLatLng.lng,
          dropoff_lat: dropoffLatLng.lat,
          dropoff_lng: dropoffLatLng.lng,
          departure_time: new Date().toISOString(),
          available_seats: 3,
          driver: session?.user?.id, // Use authenticated user's ID
        },
        {
          headers: { Authorization: `Bearer ${session.accessToken}` },
        }
      );

      console.log('Ride created:', response.data);
      socket.emit('ride_created', response.data);
    } catch (error) {
      console.error('Error creating ride:', error);
    }
  };

  const initiateCall = async () => {
    if (!newRide) {
      alert('No ride available to call.');
      return;
    }

    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/initiate-call/`,
        { to: newRide.rider_phone || '+1234567890' }
      );
      console.log('Call initiated:', response.data);
    } catch (error) {
      console.error('Call error:', error);
    }
  };

  return (
    <LoadScript googleMapsApiKey={process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY!} libraries={libraries}>
      <Typography variant="h5">Create a Ride</Typography>

      <Autocomplete
        onLoad={(autocomplete) => {
          autocomplete.addListener('place_changed', () => {
            const place = autocomplete.getPlace();
            if (place.geometry?.location) {
              setPickup(place.formatted_address || '');
              setPickupLatLng({
                lat: place.geometry.location.lat(),
                lng: place.geometry.location.lng(),
              });
            }
          });
        }}
      >
        <TextField label="Pickup Location" value={pickup} onChange={(e) => setPickup(e.target.value)} fullWidth margin="normal" />
      </Autocomplete>

      <Autocomplete
        onLoad={(autocomplete) => {
          autocomplete.addListener('place_changed', () => {
            const place = autocomplete.getPlace();
            if (place.geometry?.location) {
              setDropoff(place.formatted_address || '');
              setDropoffLatLng({
                lat: place.geometry.location.lat(),
                lng: place.geometry.location.lng(),
              });
            }
          });
        }}
      >
        <TextField label="Drop-off Location" value={dropoff} onChange={(e) => setDropoff(e.target.value)} fullWidth margin="normal" />
      </Autocomplete>

      <Button variant="contained" onClick={handleSubmit} sx={{ mt: 2 }}>
        Post Ride
      </Button>

      {newRide && (
        <Typography variant="body1" sx={{ mt: 2 }}>
          New Ride Created: {newRide.pickup_location} to {newRide.dropoff_location}
        </Typography>
      )}

      {newRide && (
        <Button variant="outlined" onClick={initiateCall} sx={{ mt: 2 }}>
          Call Rider
        </Button>
      )}
    </LoadScript>
  );
}