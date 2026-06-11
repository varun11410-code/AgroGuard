/**
 * app/page.tsx
 *
 * Root page.  Renders HeroSection only, as requested.
 * HeroSection is a Client Component ("use client") so it is imported
 * directly — no dynamic() wrapper needed unless you want to skip SSR.
 */

import HeroSection from "@/components/sections/HeroSection";

export default function HomePage() {
  return (
    <main>
      <HeroSection />
    </main>
  );
}
