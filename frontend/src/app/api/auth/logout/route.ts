import { NextResponse } from "next/server";
const COOKIE = process.env.JWT_COOKIE_NAME || "retail_token";

export async function POST() {
  const res = NextResponse.json({ ok: true });
  res.cookies.set(COOKIE, "", { httpOnly: true, path: "/", maxAge: 0 });
  return res;
}
