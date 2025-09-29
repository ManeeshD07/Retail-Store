"use client";
import { useState } from "react";

export default function LoginPage() {
  const [email, setEmail] = useState("user@example.com");
  const [password, setPassword] = useState("test1234");
  const [err, setErr] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErr(null);
    const res = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type":"application/json" },
      body: JSON.stringify({ email, password }),
    });
    if (res.ok) window.location.href = "/";
    else setErr((await res.json()).error || "Login failed");
  }

  return (
    <form onSubmit={onSubmit} className="max-w-sm mx-auto bg-white p-6 rounded-2xl shadow space-y-4">
      <h1 className="text-xl font-semibold">Login</h1>
      {err && <div className="text-red-600 text-sm">{err}</div>}
      <input className="w-full border rounded-lg p-2" value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email" />
      <input className="w-full border rounded-lg p-2" type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Password" />
      <button className="w-full bg-black text-white rounded-lg py-2">Sign in</button>
    </form>
  );
}
