// src/app/layout.tsx
import "./globals.css";
import type { Metadata } from "next";
import Link from "next/link";                 // ✅ add
import { QueryClientProvider } from "./lib/queryClient";

export const metadata: Metadata = { title: "Retail App", description: "Next.js + Flask Retail" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-neutral-50 text-neutral-900">
        <QueryClientProvider>
          <header className="p-4 border-b bg-white">
            <div className="max-w-6xl mx-auto flex items-center gap-6">
              <Link href="/" className="font-semibold text-xl">Retail App</Link>        {/* ✅ */}
              <nav className="ml-auto flex gap-4">
                <Link href="/cart">Cart</Link>                                          {/* ✅ */}
                <Link href="/login">Login</Link>                                        {/* ✅ */}
                <Link href="/admin">Admin</Link>                                        {/* ✅ */}
              </nav>
            </div>
          </header>
          <main className="max-w-6xl mx-auto p-6">{children}</main>
        </QueryClientProvider>
      </body>
    </html>
  );
}
