import "../src/styles/globals.css";

import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "Casablanca Fear & Greed Index",
  description: "Analytical dashboard for the Casablanca Stock Exchange sentiment index",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="fr">
      <body className="bg-slate-900 text-slate-100 min-h-screen">
        <main className="min-h-screen">{children}</main>
      </body>
    </html>
  );
}

