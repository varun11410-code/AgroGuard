import React from "react";
import { X, Sparkles } from "lucide-react";

interface ChatHeaderProps {
  onClose: () => void;
}

export default function ChatHeader({ onClose }: ChatHeaderProps) {
  return (
    <div className="px-5 py-4 bg-gradient-to-br from-[#166534]/80 to-[#22c55e]/30 border-b border-white/10 flex items-center gap-3 shrink-0">
      <div className="w-9 h-9 rounded-full bg-gradient-to-br from-[#166534] to-[#22c55e] flex items-center justify-center border-2 border-white/20">
        <Sparkles className="w-4 h-4 text-white" />
      </div>
      <div className="flex-1">
        <div className="font-syne font-bold text-[15px] text-white leading-tight">AgroGuard AI</div>
        <div className="text-[11.5px] text-white/60 flex items-center gap-1.5 mt-0.5">
          <span className="w-1.5 h-1.5 rounded-full bg-g2 inline-block shadow-[0_0_8px_rgba(34,197,94,0.8)]"></span>
          Online · Powered by Gemini
        </div>
      </div>
      <button 
        onClick={onClose}
        aria-label="Close chat"
        className="p-1.5 opacity-60 hover:opacity-100 transition-opacity text-white rounded-full hover:bg-white/10"
      >
        <X className="w-5 h-5" />
      </button>
    </div>
  );
}
