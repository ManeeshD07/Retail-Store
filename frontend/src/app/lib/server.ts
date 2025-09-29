export const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000/api";

export async function sfetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    // pass cookies on server when proxying to our own route handlers (not needed for direct Flask calls)
    cache: "no-store",
    ...init,
  });
  if (!res.ok) throw new Error(`API ${path} failed: ${res.status}`);
  return res.json() as Promise<T>;
}
