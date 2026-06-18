import React from "react";

export interface MessageType {
  id: string;
  role: "user" | "assistant";
  message: string;
}

interface ChatMessageProps {
  message: MessageType;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isBot = message.role === "assistant";
  
  return (
    <div className={`mb-4 flex w-full ${isBot ? "justify-start" : "justify-end"}`}>
      <div 
        className={`max-w-[85%] px-4 py-3 text-[14px] leading-relaxed break-words ${
          isBot 
            ? "bg-white/10 text-foreground border border-white/10 rounded-2xl rounded-tl-sm" 
            : "bg-gradient-to-br from-[#166534] to-[#22c55e] text-white rounded-2xl rounded-tr-sm shadow-md"
        }`}
        dangerouslySetInnerHTML={{ __html: message.message }}
      />
    </div>
  );
}
