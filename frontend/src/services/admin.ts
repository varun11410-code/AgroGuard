import api from "./api";

export interface DashboardStats {
  total_users: number;
  total_scans: number;
  top_diseases: Array<{
    disease: string;
    count: number;
  }>;
}

export interface AnalyticsPayload {
  user_growth: { current: number; previous: number; percentage: number; sparkline: number[] };
  scan_growth: { current: number; previous: number; percentage: number; sparkline: number[] };
  scans_overview: Array<{ name: string; scans: number }>;
  active_today: { count: number; previous: number };
}

export interface PaginationMeta {
  page: number;
  limit: number;
  total: number;
  total_pages: number;
}

export interface PaginatedResponse {
  pagination: PaginationMeta;
  [key: string]: any; // To allow 'logs', 'users', 'scans', 'reports' keys
}

export interface ActivityLog {
  id: string;
  user_id: string | null;
  user_email: string;
  activity_type: string;
  details: Record<string, any>;
  timestamp: string;
}

export interface AdminUser {
  id: string;
  name: string;
  email: string;
  role: string;
  created_at: string;
}

export interface AdminScan {
  id: string;
  user_email: string;
  crop: string;
  disease: string | null;
  confidence: number | null;
  created_at: string;
}

export interface AdminReport {
  id: string;
  scan_id: string;
  generated_at: string;
  user_email: string;
}

export const adminService = {
  getStats: async (): Promise<DashboardStats> => {
    const response = await api.get<{ success: boolean; data: DashboardStats }>("/admin/stats");
    return response.data.data;
  },

  getAnalytics: async (): Promise<AnalyticsPayload> => {
    const response = await api.get<{ success: boolean; data: AnalyticsPayload }>("/admin/stats/analytics");
    return response.data.data;
  },

  getLogs: async (page: number = 1, limit: number = 20): Promise<{ logs: ActivityLog[]; pagination: PaginationMeta }> => {
    const response = await api.get<{ success: boolean; data: { logs: ActivityLog[]; pagination: PaginationMeta } }>(`/admin/logs?page=${page}&limit=${limit}`);
    return response.data.data;
  },

  getUsers: async (page: number = 1, limit: number = 20): Promise<{ users: AdminUser[]; pagination: PaginationMeta }> => {
    const response = await api.get<{ success: boolean; data: { users: AdminUser[]; pagination: PaginationMeta } }>(`/admin/users?page=${page}&limit=${limit}`);
    return response.data.data;
  },

  getScans: async (page: number = 1, limit: number = 20): Promise<{ scans: AdminScan[]; pagination: PaginationMeta }> => {
    const response = await api.get<{ success: boolean; data: { scans: AdminScan[]; pagination: PaginationMeta } }>(`/admin/scans?page=${page}&limit=${limit}`);
    return response.data.data;
  },

  getReports: async (page: number = 1, limit: number = 20): Promise<{ reports: AdminReport[]; pagination: PaginationMeta }> => {
    const response = await api.get<{ success: boolean; data: { reports: AdminReport[]; pagination: PaginationMeta } }>(`/admin/reports?page=${page}&limit=${limit}`);
    return response.data.data;
  },
};
