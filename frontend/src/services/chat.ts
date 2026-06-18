import api from './api';

export interface ChatMessageData {
  id: string;
  role: "user" | "assistant";
  message: string;
  created_at?: string;
}

export interface ChatSessionData {
  id: string;
  scan_id?: string;
}

export interface ChatHistoryResponse {
  success: boolean;
  session: ChatSessionData | null;
  history: ChatMessageData[];
}

export interface ChatSendResponse {
  success: boolean;
  session_id: string;
  message: ChatMessageData;
}

export const chatService = {
  /**
   * Fetches the chat history for a given scan or the general chat.
   */
  getSessionHistory: async (scanId?: string): Promise<ChatHistoryResponse> => {
    const response = await api.get('/chat/session', {
      params: scanId ? { scan_id: scanId } : undefined
    });
    return response.data;
  },

  /**
   * Sends a message to the AI and persists it in the session.
   */
  sendMessage: async (
    message: string, 
    sessionId: string | null = null, 
    scanId: string | null = null,
    selectedPlan: string | null = null
  ): Promise<ChatSendResponse> => {
    const response = await api.post('/chat', {
      message,
      session_id: sessionId,
      scan_id: scanId,
      selected_plan: selectedPlan
    });
    return response.data;
  }
};
