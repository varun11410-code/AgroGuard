import Link from "next/link";
import { cn } from "@/lib/utils";

const FOOTER_LINKS = [
  { label: "GitHub", href: "https://github.com/varun11410-code" },
  { label: "Contact", href: "mailto:sinhavarun99@gmail.com" },
  { label: "API Docs", href: "#" },
  { label: "LinkedIn", href: "https://www.linkedin.com/in/varunkumarsinha" },
  { label: "Privacy", href: "#" },

];

export default function Footer() {
  return (
    <footer id="global-footer" className="pt-[60px] pb-10 px-[7%] w-full mt-auto">
      <div className="container mx-auto glass-card p-[50px] grid grid-cols-1 md:grid-cols-[1fr_auto] gap-10 items-center">

        {/* Brand Area */}
        <div className="flex flex-col">
          <div className="flex items-center gap-2.5 mb-2.5">
            <div
              className="w-9 h-9 rounded-[10px] text-base bg-[linear-gradient(135deg,var(--g),var(--g2))] flex items-center justify-center shadow-sm relative overflow-hidden"
              aria-hidden="true"
            >
              🌱
            </div>
            <h2 className="font-heading text-[1.2rem] font-extrabold tracking-[-0.03em] text-foreground">
              AgroGuard
            </h2>
          </div>
          <p className="text-muted-foreground text-[0.85rem] mt-1.5">
            AI-Powered Crop Disease Intelligence Platform
          </p>
        </div>

        {/* Navigation Links */}
        <div className="flex gap-2.5 flex-wrap">
          {FOOTER_LINKS.map((link) => (
            <Link
              key={link.label}
              href={link.href}
              className="py-2.5 px-[18px] rounded-full text-muted-foreground no-underline text-[0.85rem] border border-border transition-all duration-300 font-sans hover:text-foreground hover:border-foreground/20 hover:bg-secondary/50"
            >
              {link.label}
            </Link>
          ))}
        </div>
      </div>

      {/* Footer Bottom */}
      <div className="container mx-auto mt-6 pt-6 border-t border-border flex flex-col md:flex-row justify-between items-center text-muted-foreground/70 text-[0.8rem] font-sans gap-2.5 md:gap-0 text-center md:text-left">
        <span>&copy; {new Date().getFullYear()} AgroGuard. All Rights Reserved.</span>
        <span className="flex items-center gap-2">
          Built with <span className="text-primary" aria-label="love">&hearts;</span> for farmers
        </span>
      </div>
    </footer>
  );
}
