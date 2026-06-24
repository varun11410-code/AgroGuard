"use client";

import { useState } from "react";
import { Bell, ChevronDown, LogOut } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";

interface AdminTopbarProps {
  onMenuClick?: () => void;
}

export function AdminTopbar({ onMenuClick }: AdminTopbarProps) {
  const { user, logout } = useAuth();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const router = useRouter();

  const handleLogout = async () => {
    await logout();
    router.push("/login");
  };

  return (
    <header className="h-[80px] flex items-center justify-between px-8 border-b border-white/5 bg-[#050d07]/80 backdrop-blur-md sticky top-0 z-40">
      <div className="flex items-center">
        <div 
          className="md:hidden text-white/50 cursor-pointer hover:text-white transition-colors"
          onClick={onMenuClick}
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
        </div>
      </div>
      
      <div className="flex items-center gap-6">
        <div className="relative cursor-pointer text-white/60 hover:text-white transition-colors">
          <Bell size={20} />
        </div>
        
        <div className="relative">
          <div 
            className="flex items-center gap-3 cursor-pointer pl-6 border-l border-white/10"
            onClick={() => setDropdownOpen(!dropdownOpen)}
          >
            <div className="w-10 h-10 rounded-full bg-green-500/20 border border-green-500/30 flex items-center justify-center text-green-400 font-bold overflow-hidden shadow-[0_0_10px_rgba(34,197,94,0.2)]">
               {user?.name?.charAt(0) || "A"}
            </div>
            <div className="hidden md:block">
              <p className="text-sm font-bold text-white/90 leading-none mb-1.5">{user?.name || "Admin User"}</p>
              <p className="text-[0.7rem] text-green-500 leading-none font-mono">Administrator</p>
            </div>
            <ChevronDown size={14} className={`text-white/40 ml-1 transition-transform ${dropdownOpen ? 'rotate-180' : ''}`} />
          </div>

          {dropdownOpen && (
            <>
              <div 
                className="fixed inset-0 z-40" 
                onClick={() => setDropdownOpen(false)}
              ></div>
              <div className="absolute right-0 mt-3 w-48 bg-[#0a1a0d]/95 backdrop-blur-xl border border-white/10 rounded-xl shadow-xl z-50 overflow-hidden py-1">
                <div 
                  className="px-4 py-3 flex items-center gap-3 text-sm text-red-400 hover:bg-red-500/10 cursor-pointer transition-colors"
                  onClick={handleLogout}
                >
                  <LogOut size={16} />
                  <span>Log out</span>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
