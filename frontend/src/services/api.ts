// API service
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor: Attach access token
api.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('agroguard_access_token');
      if (token && config.headers && !config.headers.Authorization) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor: Handle 401s and token rotation
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Only attempt rotation if 401 and we haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry && typeof window !== 'undefined') {
      originalRequest._retry = true;
      
      const refreshToken = localStorage.getItem('agroguard_refresh_token');
      if (!refreshToken) {
        localStorage.removeItem('agroguard_access_token');
        localStorage.removeItem('agroguard_refresh_token');
        localStorage.removeItem('agroguard_user');
        window.location.href = '/login';
        return Promise.reject(error);
      }

      try {
        const response = await axios.post(`${API_URL}/auth/refresh`, {}, {
          headers: {
            Authorization: `Bearer ${refreshToken}`
          }
        });
        
        const newAccessToken = response.data?.data?.access_token;
        if (newAccessToken) {
          localStorage.setItem('agroguard_access_token', newAccessToken);
          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
          return api(originalRequest);
        }
      } catch {
        // Refresh token invalid or expired
        localStorage.removeItem('agroguard_access_token');
        localStorage.removeItem('agroguard_refresh_token');
        localStorage.removeItem('agroguard_user');
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

export default api;
