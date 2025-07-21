"use client";
import { signIn } from "next-auth/react";
import { useState } from "react";
import { Button } from "~/components/ui/button";

export default function LoginPage() {
  const [email, setEmail] = useState("admin@gmail.com");
  const [password, setPassword] = useState("admin");

  const handleAdmin = async (e: React.FormEvent) => {
    e.preventDefault();
    await signIn("credentials", {
      username: email,
      password,
      callbackUrl: "/admin",
    });
  };

  return (
    <div className="flex flex-col items-center gap-4 p-4">
      <h1 className="text-2xl">Login</h1>
      <Button onClick={() => signIn("google")}>Sign in with Google</Button>
      <form onSubmit={handleAdmin} className="flex flex-col gap-2 w-60">
        <input
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          type="email"
          className="border p-2"
          placeholder="Admin Email"
        />
        <input
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          type="password"
          className="border p-2"
          placeholder="Password"
        />
        <Button type="submit">Admin Login</Button>
      </form>
    </div>
  );
}
