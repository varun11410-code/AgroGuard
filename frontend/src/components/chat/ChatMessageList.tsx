import React, { useRef, useEffect } from "react";
import ChatMessage, { MessageType } from "./ChatMessage";

interface ChatMessageListProps {
  messages: MessageType[];
}

export default function ChatMessageList({ messages }: ChatMessageListProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div 
      ref={scrollRef}
      className="flex-1 p-5 overflow-y-auto overscroll-contain flex flex-col"
    >
      {messages.map((msg) => (
        <ChatMessage key={msg.id} message={msg} />
      ))}
    </div>
  );
}
