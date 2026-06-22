// Auth service
import api from './api';
import { User, LoginCredentials, RegisterData, LoginResponse, RegisterResponse, ApiErrorResponse } from '../types/auth';
import axios, { AxiosError } from 'axios';

/**
 * Normalizes backend error responses into a safe, displayable error string.
 */
function handleAuthError(error: unknown): never {
  if (axios.isAxiosError(error)) {
    const data = error.response?.data as ApiErrorResponse | undefined;
    
    // Validation errors (400)
    if (data?.errors && Array.isArray(data.errors) && data.errors.length > 0) {
      throw new Error(data.errors[0].message);
    }
    
    // Specific business errors (401, 409)
    if (data?.message) {
      throw new Error(data.message);
    }
  }
  
  // Generic fallback
  throw new Error('An unexpected server error occurred. Please try again.');
}

export const authService = {
  /**
   * Registers a new user.
   * Backend returns { success, data: User } wrapped response.
   */
  register: async (data: RegisterData): Promise<RegisterResponse> => {
    try {
      const response = await api.post<RegisterResponse>('/auth/register', data);
      return response.data;
    } catch (error) {
      handleAuthError(error);
    }
  },

  /**
   * Logs in a user.
   * Backend directly returns { access_token, refresh_token, user } without success wrapper.
   */
  login: async (credentials: LoginCredentials): Promise<LoginResponse> => {
    try {
      const response = await api.post<LoginResponse>('/auth/login', credentials);
      return response.data;
    } catch (error) {
      handleAuthError(error);
    }
  },

  /**
   * Logs out the user.
   * Note: This requires the refresh_token as a Bearer token. Task 9E handles actual token management.
   */
  logout: async (refreshToken?: string): Promise<void> => {
    try {
      if (refreshToken) {
        await api.post('/auth/logout', {}, {
          headers: {
            Authorization: `Bearer ${refreshToken}`
          }
        });
      } else {
        await api.post('/auth/logout');
      }
    } catch (error) {
      handleAuthError(error);
    }
  },

  /**
   * Updates user preferences.
   */
  updatePreferences: async (data: { language?: string; preferred_budget_tier?: string }) => {
    try {
      const response = await api.patch<{ success: boolean; data: User }>('/auth/preferences', data);
      return response.data;
    } catch (error) {
      handleAuthError(error);
    }
  }
};
