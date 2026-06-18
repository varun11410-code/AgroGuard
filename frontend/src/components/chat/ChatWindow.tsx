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
}

export default function ChatWindow({ isOpen, onClose, messages, onSendMessage }: ChatWindowProps) {
  const { user } = useAuth();

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
      
      {!user ? (
        <>
          <ChatGuestPrompt />
          <ChatInputArea onSend={() => {}} disabled={true} />
        </>
      ) : (
        <>
          <ChatMessageList messages={messages} />
          <ChatInputArea onSend={onSendMessage} autoFocus={isOpen} />
        </>
      )}
    </div>
  );
}
