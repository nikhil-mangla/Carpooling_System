// next-auth.d.ts
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import NextAuth from 'next-auth'; // Optional, ensures module context

declare module 'next-auth' {
  interface Session {
    accessToken?: string; // Add accessToken to Session
    user: {
      id: string; // Required
      name?: string | null;
    };
  }

  interface User {
    id: string;
    name: string;
    token: string; // Custom user type
  }
}

declare module 'next-auth/jwt' {
  interface JWT {
    accessToken?: string; // Add accessToken to JWT
  }
}