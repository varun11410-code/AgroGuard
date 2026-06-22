"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

const NAV_LINKS = [
  { label: "Home", href: "/" },
  { label: "Crops", href: "/#crops" },
  { label: "Features", href: "/#features" },
  { label: "Upload", href: "/upload" },
  { label: "Dashboard", href: "/#dashboard" },
  { label: "History", href: "/history" },
  { label: "Reports", href: "/reports" },
  { label: "Profile", href: "/profile" },
];

export default function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };

    // Initial check
    handleScroll();

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Prevent scrolling when mobile menu is open
  useEffect(() => {
    if (isMobileMenuOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
    }
    return () => {
      document.body.style.overflow = "unset";
    };
  }, [isMobileMenuOpen]);

  return (
    <>
      <nav
        className={cn(
          "fixed top-5 left-1/2 -translate-x-1/2 w-[92%] max-w-[1400px] py-4 px-7 flex items-center justify-between z-[900] transition-all duration-400 ease-out",
          isScrolled
            ? "bg-background/85 border border-border backdrop-blur-[30px] rounded-[var(--radius)] shadow-lg"
            : "bg-transparent border border-transparent"
        )}
      >
        {/* Logo */}
        <Link href="#home" className="flex items-center gap-3 font-heading text-xl font-extrabold tracking-tight">
          <div className="w-11 h-11 rounded-[14px] bg-[linear-gradient(135deg,var(--g),var(--g2))] flex items-center justify-center text-2xl shadow-sm relative overflow-hidden">
            🌱
          </div>
          <span className="text-foreground">Agro<span className="text-primary">Guard</span></span>
        </Link>

        {/* Desktop Nav Links */}
        <div className="hidden lg:flex items-center gap-2">
          {NAV_LINKS.map((item) => (
            <Link
              key={item.label}
              href={item.href}
              className="text-muted-foreground font-sans font-medium text-[1.1rem] py-2 px-4 rounded-full transition-all duration-300 hover:text-foreground hover:bg-secondary"
            >
              {item.label}
            </Link>
          ))}

          <div className="flex items-center gap-2 ml-2">
            <Button variant="outline" className="text-[1.1rem]" asChild>
              <Link href="/login">Login</Link>
            </Button>
            <Button className="text-[1.1rem]" asChild>
              <Link href="/signup">Sign Up</Link>
            </Button>
          </div>
        </div>

        {/* Hamburger Menu Button */}
        <button
          className="lg:hidden flex flex-col gap-[5px] p-2 bg-transparent border-none cursor-pointer z-[9501]"
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          aria-label="Toggle Menu"
          aria-expanded={isMobileMenuOpen}
        >
          <span className={cn("w-[22px] h-[2px] bg-foreground rounded-sm transition-all duration-300", isMobileMenuOpen ? "rotate-45 translate-y-[7px]" : "")} />
          <span className={cn("w-[22px] h-[2px] bg-foreground rounded-sm transition-all duration-300", isMobileMenuOpen ? "opacity-0" : "")} />
          <span className={cn("w-[22px] h-[2px] bg-foreground rounded-sm transition-all duration-300", isMobileMenuOpen ? "-rotate-45 -translate-y-[7px]" : "")} />
        </button>
      </nav>

      {/* Mobile Nav Overlay */}
      <div
        className={cn(
          "fixed inset-0 z-[9500] bg-background/98 backdrop-blur-[30px] flex flex-col items-center justify-center gap-6 transition-opacity duration-300",
          isMobileMenuOpen ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"
        )}
        aria-hidden={!isMobileMenuOpen}
      >
        <button
          className="absolute top-7 right-7 bg-transparent border-none text-muted-foreground text-2xl cursor-pointer p-2 hover:text-foreground transition-colors"
          onClick={() => setIsMobileMenuOpen(false)}
          aria-label="Close Menu"
        >
          ✕
        </button>
        {NAV_LINKS.map((item) => (
          <Link
            key={item.label}
            href={item.href}
            onClick={() => setIsMobileMenuOpen(false)}
            className="font-heading text-3xl font-bold text-muted-foreground no-underline transition-colors duration-200 hover:text-primary"
          >
            {item.label}
          </Link>
        ))}
        <Button
          variant="default"
          size="lg"
          onClick={() => setIsMobileMenuOpen(false)}
          asChild
        >
          <Link href="/login">Login</Link>
        </Button>
      </div>
    </>
  );
}
