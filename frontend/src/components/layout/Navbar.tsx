"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/contexts/AuthContext";

const PUBLIC_LINKS = [
  { label: "Home", href: "/" },
  { label: "Crops", href: "/#crops" },
  { label: "Features", href: "/#features" },
];

const PROTECTED_LINKS = [
  { label: "Upload", href: "/upload" },
  { label: "History", href: "/history" },
  { label: "Reports", href: "/reports" },
  { label: "Profile", href: "/profile" },
];

export default function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  
  const { status, user, logout } = useAuth();
  const router = useRouter();
  
  const navLinks = status === "authenticated" ? [...PUBLIC_LINKS, ...PROTECTED_LINKS] : PUBLIC_LINKS;

  const handleLogout = async () => {
    await logout();
    setIsMobileMenuOpen(false);
    router.push("/login");
  };

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
          {navLinks.map((item) => (
            <Link
              key={item.label}
              href={item.href}
              className="text-muted-foreground font-sans font-medium text-[1.1rem] py-2 px-4 rounded-full transition-all duration-300 hover:text-foreground hover:bg-secondary"
            >
              {item.label}
            </Link>
          ))}

          {status !== "loading" && (
            <div className="flex items-center gap-2 ml-2">
              {status === "authenticated" ? (
                <>
                  <div className="px-4 py-2 text-[1.1rem] font-medium text-foreground">
                    Hello, {user?.name.split(' ')[0]}
                  </div>
                  <Button onClick={handleLogout} variant="outline" className="text-[1.1rem]">
                    Logout
                  </Button>
                </>
              ) : (
                <>
                  <Button variant="outline" className="text-[1.1rem]" asChild>
                    <Link href="/login">Login</Link>
                  </Button>
                  <Button className="text-[1.1rem]" asChild>
                    <Link href="/register">Sign Up</Link>
                  </Button>
                </>
              )}
            </div>
          )}
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
        {navLinks.map((item) => (
          <Link
            key={item.label}
            href={item.href}
            onClick={() => setIsMobileMenuOpen(false)}
            className="font-heading text-3xl font-bold text-muted-foreground no-underline transition-colors duration-200 hover:text-primary"
          >
            {item.label}
          </Link>
        ))}
        {status !== "loading" && (
          <div className="flex flex-col items-center gap-4 mt-4">
            {status === "authenticated" ? (
              <>
                <div className="font-heading text-xl text-foreground">
                  Hello, {user?.name.split(' ')[0]}
                </div>
                <Button
                  variant="default"
                  size="lg"
                  onClick={handleLogout}
                >
                  Logout
                </Button>
              </>
            ) : (
              <Button
                variant="default"
                size="lg"
                onClick={() => setIsMobileMenuOpen(false)}
                asChild
              >
                <Link href="/login">Login</Link>
              </Button>
            )}
          </div>
        )}
      </div>
    </>
  );
}
