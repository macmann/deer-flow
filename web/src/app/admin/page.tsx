import { getServerSession } from "next-auth";
import { authOptions } from "../api/auth/[...nextauth]/route";
import { redirect } from "next/navigation";

export default async function AdminPage() {
  const session = await getServerSession(authOptions);
  if (!session || session.user?.email !== "admin@gmail.com") {
    redirect("/login");
  }
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/admin/users`, {
    headers: { Authorization: `Bearer admin-token` },
    cache: "no-cache",
  });
  const users: string[] = await res.json();
  return (
    <div className="p-4">
      <h1 className="text-2xl mb-4">Signed in users</h1>
      <ul className="list-disc ml-4">
        {users.map((u) => (
          <li key={u}>{u}</li>
        ))}
      </ul>
    </div>
  );
}
