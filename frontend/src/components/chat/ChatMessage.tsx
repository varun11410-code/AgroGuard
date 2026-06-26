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
  const isBot = message.role.toLowerCase() === "assistant";
  
  return (
    <div className={`mb-4 flex w-full ${isBot ? "justify-start" : "justify-end"}`}>
      <div 
        className={`max-w-[85%] px-4 py-3 text-[14px] leading-relaxed break-words shadow-md ${
          isBot 
            ? "bg-[#0f2414] border border-[#166534] text-white/90 rounded-2xl rounded-tl-sm" 
            : "bg-gradient-to-br from-[#166534] to-[#22c55e] text-white rounded-2xl rounded-tr-sm"
        }`}
        dangerouslySetInnerHTML={{ __html: message.message }}
      />
    </div>
  );
}
