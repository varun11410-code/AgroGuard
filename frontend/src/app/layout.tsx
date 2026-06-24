import type { Metadata } from "next";
import { DM_Sans, Syne } from "next/font/google";
import BackgroundSystem from "@/components/layout/BackgroundSystem";
import { AuthProvider } from "@/contexts/AuthContext";
import "./globals.css";

const dmSans = DM_Sans({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  variable: "--font-dm-sans",
});

const syne = Syne({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
  variable: "--font-syne",
});

export const metadata: Metadata = {
  title: "AgroGuard",
  description: "AI-Powered Agricultural Intelligence",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${dmSans.variable} ${syne.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col font-sans bg-background text-foreground relative">
        <BackgroundSystem />
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
