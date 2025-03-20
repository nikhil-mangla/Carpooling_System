import { useState } from 'react';
import { TextField, Button, Typography, List, ListItem, ListItemText } from '@mui/material';
import { LoadScript, Autocomplete } from '@react-google-maps/api';
import axios from 'axios';

const libraries: ("places")[] = ['places'];

interface LatLng {
  lat: number;
  lng: number;
}

interface Match {
  ride: {
    pickup_location: string;
    dropoff_location: string;
  };
  match_percentage: number;
}

export default function SearchRides() {
  const [pickup, setPickup] = useState('');
  const [dropoff, setDropoff] = useState('');
  const [pickupLatLng, setPickupLatLng] = useState<LatLng | null>(null);
  const [dropoffLatLng, setDropoffLatLng] = useState<LatLng | null>(null);
  const [matches, setMatches] = useState<Match[]>([]);

  const handleSearch = async () => {
    if (!pickupLatLng || !dropoffLatLng) return;
    try {
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/route-match/`, {
        params: {
          pickup_lat: pickupLatLng.lat,
          pickup_lng: pickupLatLng.lng,
          dropoff_lat: dropoffLatLng.lat,
          dropoff_lng: dropoffLatLng.lng,
        },
      });
      setMatches(response.data);
    } catch (error) {
      console.error('Error searching rides:', error);
    }
  };

  return (
    <LoadScript googleMapsApiKey={process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY!} libraries={libraries}>
      <Typography variant="h5">Search Rides</Typography>
      <Autocomplete
        onLoad={(autocomplete) => {
          autocomplete.addListener('place_changed', () => {
            const place = autocomplete.getPlace();
            if (place.geometry && place.geometry.location) {
              setPickup(place.formatted_address || '');
              setPickupLatLng({ lat: place.geometry.location.lat(), lng: place.geometry.location.lng() });
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
            if (place.geometry && place.geometry.location) {
              setDropoff(place.formatted_address || '');
              setDropoffLatLng({ lat: place.geometry.location.lat(), lng: place.geometry.location.lng() });
            }
          });
        }}
      >
        <TextField label="Drop-off Location" value={dropoff} onChange={(e) => setDropoff(e.target.value)} fullWidth margin="normal" />
      </Autocomplete>
      <Button variant="contained" onClick={handleSearch} sx={{ mt: 2 }}>Search</Button>
      <List>
        {matches.map((match, index) => (
          <ListItem key={index}>
            <ListItemText
              primary={`${match.ride.pickup_location} to ${match.ride.dropoff_location}`}
              secondary={`Match: ${match.match_percentage.toFixed(2)}%`}
            />
          </ListItem>
        ))}
      </List>
    </LoadScript>
  );
}