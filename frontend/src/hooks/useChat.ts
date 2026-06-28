import { useState, useCallback } from 'react';
import { chatService, ChatMessageData } from '@/services/chat';
import { useAuth } from '@/contexts/AuthContext';

export function useChat(scanId?: string, selectedPlan?: string) {
  const { user } = useAuth();
  const [messages, setMessages] = useState<ChatMessageData[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasInitialized, setHasInitialized] = useState(false);

  const fetchHistory = useCallback(async () => {
    if (!user) return;
    
    setIsLoading(true);
    setError(null);
    try {
      const data = await chatService.getSessionHistory(scanId);
      if (data.session) {
        setSessionId(data.session.id);
        setMessages(data.history || []);
      } else {
        setMessages([
          {
            id: 'system-initial',
            role: 'assistant',
            message: "Hello! 👋 I'm AgroGuard AI.<br><br>I can help you with crop disease questions, treatment recommendations, and agricultural guidance. How can I assist you today?"
          }
        ]);
      }
      setHasInitialized(true);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to load chat history');
    } finally {
      setIsLoading(false);
    }
  }, [user, scanId]);

  const sendMessage = async (content: string) => {
    if (!content.trim() || isGenerating || !user) return;

    const optimisticUserMsg: ChatMessageData = {
      id: Date.now().toString(),
      role: 'user',
      message: content,
    };

    setMessages(prev => [...prev, optimisticUserMsg]);
    setIsGenerating(true);
    setError(null);

    try {
      const data = await chatService.sendMessage(content, sessionId, scanId || null, selectedPlan || null);
      if (!sessionId) {
        setSessionId(data.session_id);
      }
      // Replace the optimistic message sequence with the true state if needed,
      // but simpler is to just append the assistant response
      setMessages(prev => [...prev, data.message]);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to send message');
      // On failure, the backend orchestrator still saved the user message to the DB,
      // so our optimistic UI remains accurate!
      // We just inject a local error message so the user knows the AI failed.
      setMessages(prev => [
        ...prev, 
        {
          id: Date.now().toString() + "-err",
          role: "assistant",
          message: "<span class='text-red-300'>Sorry, I encountered an error connecting to the AI provider. Please try again.</span>"
        }
      ]);
    } finally {
      setIsGenerating(false);
    }
  };

  return {
    messages,
    isLoading,
    isGenerating,
    error,
    sendMessage,
    fetchHistory,
    hasInitialized
  };
}
