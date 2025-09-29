import { NextRequest, NextResponse } from "next/server";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000/api";
const COOKIE = process.env.JWT_COOKIE_NAME || "retail_token";

export async function POST(req: NextRequest) {
  const body = await req.json();
  const res = await fetch(`${API}/auth/login`, {
    method: "POST",
    headers: { "Content-Type":"application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    return NextResponse.json(err, { status: res.status });
  }

  const data = await res.json();
  const token = data.access_token;
  const response = NextResponse.json({ ok: true });

  response.cookies.set(COOKIE, token, {
    httpOnly: true,
    sameSite: "lax",
    path: "/",
    maxAge: 60 * 60 * 24 * 7, // 7 days
    secure: process.env.NODE_ENV === "production",
  });

  return response;
}
