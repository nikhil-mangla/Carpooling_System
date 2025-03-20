import { useSession, signOut } from 'next-auth/react';
import { Typography, Button } from '@mui/material';

export default function Account() {
  const { data: session } = useSession();

  if (!session) return <Typography>Please log in.</Typography>;

  return (
    <div>
      <Typography variant="h5">Account</Typography>
      <Typography>Welcome, {session.user?.name}!</Typography>
      <Button variant="contained" onClick={() => signOut({ callbackUrl: '/' })} sx={{ mt: 2 }}>
        Logout
      </Button>
    </div>
  );
}