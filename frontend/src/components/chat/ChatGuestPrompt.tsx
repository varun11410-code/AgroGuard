import React from "react";
import Link from "next/link";
import { UserCircle } from "lucide-react";

export default function ChatGuestPrompt() {
  return (
    <div className="flex-1 flex flex-col items-center justify-center p-6 text-center h-full">
      <div className="w-16 h-16 rounded-full bg-g2/10 flex items-center justify-center mb-4 border border-g2/20">
        <UserCircle className="w-8 h-8 text-g2" />
      </div>
      <h3 className="font-syne text-xl font-bold text-foreground mb-2">
        Sign in required
      </h3>
      <p className="text-muted-foreground text-sm mb-6 max-w-[250px]">
        Please log in to use the AgroGuard AI Assistant.
      </p>
      <Link
        href="/login"
        className="px-6 py-2.5 rounded-full bg-gradient-to-r from-[#166534] to-[#22c55e] text-white font-medium hover:opacity-90 transition-opacity w-full text-center"
      >
        Sign In
      </Link>
    </div>
  );
}
