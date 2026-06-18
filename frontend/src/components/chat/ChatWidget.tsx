"use client";

import React, { useState, useEffect } from "react";
import { Sparkles } from "lucide-react";
import ChatWindow from "./ChatWindow";
import { MessageType } from "./ChatMessage";

export interface ChatWidgetProps {
  mode?: "general" | "diagnosis";
  scanContext?: {
    crop: string;
    disease: string;
    confidence: number;
  } | null;
}

export default function ChatWidget({ mode = "general", scanContext }: ChatWidgetProps) {
  const [isOpen, setIsOpen] = useState(false);
  
  // Mock messages for UI scaffolding
  const [messages, setMessages] = useState<MessageType[]>([
    {
      id: "1",
      role: "assistant",
      content: "Hello! 👋 I'm AgroGuard AI, powered by Google Gemini.<br><br>I can help you with crop disease questions, treatment recommendations, and agricultural guidance. How can I assist you today?"
    }
  ]);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen) {
        setIsOpen(false);
      }
    };
    document.addEventListener("keydown", handleEscape);
    return () => document.removeEventListener("keydown", handleEscape);
  }, [isOpen]);

  const handleSendMessage = (content: string) => {
    // Scaffold implementation for UI
    const newMessage: MessageType = {
      id: Date.now().toString(),
      role: "user",
      content,
    };
    setMessages(prev => [...prev, newMessage]);
  };

  return (
    <>
      {/* Floating Button */}
      <button
        onClick={() => setIsOpen(true)}
        aria-label="Open AI Assistant"
        className={`fixed right-[28px] bottom-[28px] z-[9000] w-[64px] h-[64px] rounded-full 
                   bg-gradient-to-br from-[#166534] to-[#22c55e] border-none cursor-pointer 
                   flex items-center justify-center text-white
                   shadow-[0_8px_30px_rgba(34,197,94,0.5)] animate-chat-pulse
                   transition-all duration-300 hover:scale-110
                   ${isOpen ? 'scale-0 opacity-0 pointer-events-none' : 'scale-100 opacity-100'}`}
      >
        <Sparkles className="w-8 h-8" />
      </button>

      {/* Chat Window */}
      <ChatWindow 
        isOpen={isOpen} 
        onClose={() => setIsOpen(false)} 
        messages={messages}
        onSendMessage={handleSendMessage}
      />
    </>
  );
}
