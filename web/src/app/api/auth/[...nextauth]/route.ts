import NextAuth from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";

export const authOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID ?? "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET ?? "",
    }),
    CredentialsProvider({
      name: "Admin",
      credentials: {
        username: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      authorize(credentials) {
        if (
          credentials?.username === "admin@gmail.com" &&
          credentials?.password === "admin"
        ) {
          return {
            id: "admin",
            name: "Admin",
            email: "admin@gmail.com",
            role: "admin",
          };
        }
        return null;
      },
    }),
  ],
  callbacks: {
    async signIn({ user }) {
      if (user.email && user.email !== "admin@gmail.com") {
        try {
          await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/users/record`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: user.email }),
          });
        } catch (e) {
          console.error("Failed to record user login", e);
        }
      }
      return true;
    },
  },
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
