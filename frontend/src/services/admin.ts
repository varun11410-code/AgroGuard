import api from "./api";

export interface DashboardStats {
  total_users: number;
  total_scans: number;
  top_diseases: Array<{
    disease: string;
    count: number;
  }>;
}

export interface ActivityLog {
  id: string;
  user_id: string | null;
  user_email: string;
  activity_type: string;
  details: Record<string, any>;
  timestamp: string;
}

export interface PaginatedLogs {
  logs: ActivityLog[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    total_pages: number;
  };
}

export const adminService = {
  getStats: async (): Promise<DashboardStats> => {
    const response = await api.get<{ success: boolean; data: DashboardStats }>("/admin/stats");
    return response.data.data;
  },

  getLogs: async (page: number = 1, limit: number = 20): Promise<PaginatedLogs> => {
    const response = await api.get<{ success: boolean; data: PaginatedLogs }>(`/admin/logs?page=${page}&limit=${limit}`);
    return response.data.data;
  },
};
