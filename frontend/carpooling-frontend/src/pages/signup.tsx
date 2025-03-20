import { useState } from 'react';
import { TextField, Button, Typography } from '@mui/material';
import axios from 'axios';
import { useRouter } from 'next/router';

export default function Signup() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const router = useRouter();

  const handleSignup = async () => {
    try {
      await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/register/`, {
        username,
        password,
        email,
      });
      router.push('/login');
    } catch (error) {
      console.error('Signup error:', error);
    }
  };

  return (
    <div>
      <Typography variant="h5">Sign Up</Typography>
      <TextField label="Username" value={username} onChange={(e) => setUsername(e.target.value)} fullWidth margin="normal" />
      <TextField label="Email" value={email} onChange={(e) => setEmail(e.target.value)} fullWidth margin="normal" />
      <TextField label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} fullWidth margin="normal" />
      <Button variant="contained" onClick={handleSignup} sx={{ mt: 2 }}>Sign Up</Button>
    </div>
  );
}