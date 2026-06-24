"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Users, Scan, Activity, LayoutDashboard, FileText, HeartPulse, ShieldCheck } from "lucide-react";

export function AdminSidebar() {
  const pathname = usePathname();

  const links = [
    { name: "Dashboard", href: "/admin", icon: LayoutDashboard },
    { name: "Users", href: "/admin/users", icon: Users },
    { name: "Scans", href: "/admin/scans", icon: Scan },
    { name: "Reports", href: "/admin/reports", icon: FileText },
    { name: "Activity Logs", href: "/admin/logs", icon: Activity },
  ];

  return (
    <aside className="fixed inset-y-0 left-0 w-[260px] bg-[#050d07]/95 border-r border-white/5 backdrop-blur-xl z-50 flex-col hidden md:flex">
      <div className="p-6">
        <Link href="/" className="flex items-center gap-3 font-heading text-xl font-extrabold tracking-tight">
          <div className="w-9 h-9 rounded-[10px] bg-[linear-gradient(135deg,var(--g),var(--g2))] flex items-center justify-center text-xl shadow-sm relative overflow-hidden">
            🌱
          </div>
          <span className="text-foreground">Agro<span className="text-primary">Guard</span></span>
        </Link>
      </div>

      <div className="px-4 py-2">
        <p className="text-[0.65rem] font-mono tracking-[0.15em] text-green-500/70 uppercase mb-4 px-2">Admin Panel</p>
        <nav className="flex flex-col gap-1">
          {links.map((link) => {
            const isActive = pathname === link.href || (link.href !== "/admin" && pathname?.startsWith(link.href));
            const Icon = link.icon;
            return (
              <Link key={link.href} href={link.href} className={`flex items-center gap-3 px-3 py-2.5 rounded-xl cursor-pointer transition-colors ${isActive ? 'bg-green-500/10 text-green-400 font-medium' : 'text-white/50 hover:text-white hover:bg-white/5'}`}>
                <Icon size={18} />
                <span className="text-sm">{link.name}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="mt-auto p-4">
        <div className="rounded-2xl p-4 bg-gradient-to-b from-white/5 to-transparent border border-white/5 relative overflow-hidden group cursor-default">
          <div className="absolute inset-0 bg-green-500/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div className="text-green-500 mb-2">
            <ShieldCheck size={24} />
          </div>
          <h4 className="font-bold text-sm text-white/90 mb-1">AgroGuard Admin</h4>
          <p className="text-[0.7rem] text-white/50 leading-relaxed">Powerful analytics for a healthier tomorrow</p>
        </div>
      </div>
    </aside>
  );
}
