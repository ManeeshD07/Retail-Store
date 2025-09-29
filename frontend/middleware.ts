import { NextRequest, NextResponse } from "next/server";
const COOKIE = process.env.JWT_COOKIE_NAME || "retail_token";

// Protect selected paths
const PROTECTED = ["/cart", "/admin"];

export function middleware(req: NextRequest) {
  const url = req.nextUrl.clone();
  const pathname = url.pathname;

  if (PROTECTED.some(p => pathname.startsWith(p))) {
    const token = req.cookies.get(COOKIE)?.value;
    if (!token) {
      url.pathname = "/login";
      return NextResponse.redirect(url);
    }
    // Optionally: decode/verify JWT here (with public key) to check role for /admin
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/cart/:path*", "/admin/:path*"],
};
