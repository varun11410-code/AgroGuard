import React, { useRef, useEffect } from "react";
import { SendHorizontal } from "lucide-react";

interface ChatInputAreaProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  autoFocus?: boolean;
}

export default function ChatInputArea({ onSend, disabled, autoFocus }: ChatInputAreaProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (autoFocus && !disabled) {
      inputRef.current?.focus();
    }
  }, [autoFocus, disabled]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (disabled || !inputRef.current?.value.trim()) return;
    onSend(inputRef.current.value);
    inputRef.current.value = "";
  };

  return (
    <form 
      onSubmit={handleSubmit}
      className="p-4 border-t border-white/10 bg-background/50 flex items-center gap-2 pb-safe"
    >
      <input
        ref={inputRef}
        type="text"
        placeholder={disabled ? "Sign in to chat..." : "Ask about diseases, treatments..."}
        disabled={disabled}
        className="flex-1 bg-white/5 border border-white/10 rounded-full px-4 py-2.5 text-sm text-foreground focus:outline-none focus:border-g2/50 focus:bg-white/10 transition-colors disabled:opacity-50"
        autoComplete="off"
      />
      <button
        type="submit"
        disabled={disabled}
        aria-label="Send message"
        className="w-10 h-10 shrink-0 rounded-full bg-g2/20 text-g2 flex items-center justify-center border border-g2/30 hover:bg-g2 hover:text-white transition-colors disabled:opacity-50 disabled:hover:bg-g2/20 disabled:hover:text-g2"
      >
        <SendHorizontal className="w-4 h-4 ml-[-2px]" />
      </button>
    </form>
  );
}
