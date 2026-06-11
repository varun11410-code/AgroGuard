/**
 * app/layout.tsx
 *
 * App Router root layout.
 * Wires BackgroundSystem (aurora + particles) globally so that every
 * page's glass cards render correctly over the background.
 *
 * Inter font loaded via next/font/google — same as the template's
 * <link href="https://fonts.googleapis.com/css2?family=Inter:...">
 */

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "../styles/globals.css";
import BackgroundSystem from "@/components/layout/BackgroundSystem";

/* next/font/google — Inter with the exact weights used in template */
const inter = Inter({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700", "800"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: "AgroGuard — AI Powered Agriculture",
  description:
    "Protect your harvest with next-generation AI. Detect diseases instantly, receive treatment recommendations, generate reports, and make smarter farming decisions.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body>
        {/*
         * BackgroundSystem renders:
         *   • .aurora-bg with three aurora blobs (CSS animations from globals.css)
         *   • 40 .particle divs injected into document.body (via useEffect)
         * Noise texture is handled by body::after in globals.css — no JSX needed.
         */}
        <BackgroundSystem />
        {children}
      </body>
    </html>
  );
}
