"use client";
import { QueryClient, QueryClientProvider as QP } from "@tanstack/react-query";
import { useState } from "react";

export function QueryClientProvider({ children }: { children: React.ReactNode }) {
  const [client] = useState(() => new QueryClient());
  return <QP client={client}>{children}</QP>;
}
