import { useState } from 'react';
import { TextField, Button, Typography } from '@mui/material';
import { signIn } from 'next-auth/react';
import { useRouter } from 'next/router';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  const handleLogin = async () => {
    const result = await signIn('credentials', {
      redirect: false,
      username,
      password,
    });
    if (result?.ok) router.push('/account');
  };

  return (
    <div>
      <Typography variant="h5">Login</Typography>
      <TextField label="Username" value={username} onChange={(e) => setUsername(e.target.value)} fullWidth margin="normal" />
      <TextField label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} fullWidth margin="normal" />
      <Button variant="contained" onClick={handleLogin} sx={{ mt: 2 }}>Login</Button>
    </div>
  );
}