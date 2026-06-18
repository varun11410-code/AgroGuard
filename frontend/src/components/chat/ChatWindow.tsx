import React from "react";
import ChatHeader from "./ChatHeader";
import ChatGuestPrompt from "./ChatGuestPrompt";
import ChatMessageList from "./ChatMessageList";
import ChatInputArea from "./ChatInputArea";
import { MessageType } from "./ChatMessage";
import { useAuth } from "@/contexts/AuthContext";

interface ChatWindowProps {
  isOpen: boolean;
  onClose: () => void;
  messages: MessageType[];
  onSendMessage: (msg: string) => void;
  isGenerating?: boolean;
}

export default function ChatWindow({ isOpen, onClose, messages, onSendMessage, isGenerating }: ChatWindowProps) {
  const { user, status } = useAuth();

  return (
    <div 
      role="dialog" 
      aria-label="AgroGuard AI Assistant"
      className={`fixed z-[8999] bg-[#050d07]/95 border border-white/10 backdrop-blur-3xl 
                 shadow-[0_30px_80px_rgba(0,0,0,0.7),0_0_0_1px_rgba(34,197,94,0.05)] flex flex-col
                 transition-all duration-300 origin-bottom-right
                 /* Mobile styling: full screen */
                 inset-0 w-full h-[100dvh] rounded-none
                 /* Desktop styling: fixed panel */
                 md:inset-auto md:right-[28px] md:bottom-[110px] md:w-[400px] md:h-[540px] md:max-h-[calc(100dvh-140px)] md:rounded-[24px]
                 ${isOpen ? "scale-100 opacity-100 translate-y-0 pointer-events-auto" : "scale-95 opacity-0 translate-y-4 pointer-events-none"}`}
    >
      <ChatHeader onClose={onClose} />
      
      {status === "loading" ? (
        <div className="flex-1 flex items-center justify-center">
          <div className="w-8 h-8 border-2 border-g2 border-t-transparent rounded-full animate-spin"></div>
        </div>
      ) : !user ? (
        <>
          <ChatGuestPrompt />
          <ChatInputArea onSend={() => {}} disabled={true} />
        </>
      ) : (
        <>
          <div className="flex-1 overflow-hidden flex flex-col relative">
            <ChatMessageList messages={messages} />
            {isGenerating && (
              <div className="px-5 pb-2 text-xs text-g2 flex items-center gap-1.5 animate-pulse">
                <span className="w-1.5 h-1.5 bg-g2 rounded-full"></span>
                <span className="w-1.5 h-1.5 bg-g2 rounded-full animation-delay-150"></span>
                <span className="w-1.5 h-1.5 bg-g2 rounded-full animation-delay-300"></span>
                <span className="ml-1 opacity-80">AgroGuard AI is typing...</span>
              </div>
            )}
          </div>
          <ChatInputArea onSend={onSendMessage} disabled={isGenerating} autoFocus={isOpen && !isGenerating} />
        </>
      )}
    </div>
  );
}
