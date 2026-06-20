// Auth service
import api from './api';
import { User } from '../types/auth';

export const authService = {
  // Authentication methods
  updatePreferences: async (data: { language?: string }) => {
    const response = await api.patch<{ success: boolean; data: User }>('/auth/preferences', data);
    return response.data;
  }
};
