import NextAuth from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import axios from 'axios';
import type { NextAuthOptions } from 'next-auth'; // Use NextAuthOptions instead of AuthOptions

// Define the custom user type
interface CustomUser {
  id: string;
  name: string;
  token: string;
}

// Define auth options with explicit typing
export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        username: { label: 'Username', type: 'text' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        try {
          const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/token/`, {
            username: credentials?.username,
            password: credentials?.password,
          });

          if (response.data.access) {
            return {
              id: '1', // Replace with actual user ID from backend if available
              name: credentials?.username || '',
              token: response.data.access,
            } as CustomUser;
          }
          return null;
        } catch (error) {
          console.error('Error authorizing credentials:', error);
          return null;
        }
      },
    }),
  ],
  callbacks: {
    // Explicitly type the parameters
    async jwt({ token, user }: { token: import('next-auth/jwt').JWT; user?: import('next-auth').User }) {
      if (user) {
        token.accessToken = (user as CustomUser).token; // Add accessToken to JWT
      }
      return token;
    },
    async session({ session, token }: { session: import('next-auth').Session; token: import('next-auth/jwt').JWT }) {
      session.accessToken = token.accessToken; // Add accessToken to session
      if (token.sub) {
        session.user.id = token.sub; // Ensure user ID is set
      }
      return session;
    },
  },
  pages: {
    signIn: '/login',
  },
};

// Export the NextAuth handler
export default NextAuth(authOptions);