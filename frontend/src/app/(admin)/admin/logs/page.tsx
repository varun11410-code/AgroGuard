"use client";

import { useState, useEffect } from "react";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { DataTable, Column } from "@/components/admin/DataTable";
import { adminService, ActivityLog, PaginationMeta } from "@/services/admin";

export default function AdminLogsPage() {
  const [data, setData] = useState<ActivityLog[]>([]);
  const [pagination, setPagination] = useState<PaginationMeta | undefined>();
  const [loading, setLoading] = useState(true);

  const fetchLogs = async (page: number = 1) => {
    try {
      setLoading(true);
      const res = await adminService.getLogs(page, 20);
      setData(res.logs);
      setPagination(res.pagination);
    } catch (err) {
      console.error("Failed to fetch logs:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  const getRelativeTime = (isoString: string) => {
    const date = new Date(isoString);
    const now = new Date();
    const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);
    
    if (diffInSeconds < 60) return "Just now";
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
    return `${Math.floor(diffInSeconds / 86400)} days ago`;
  };

  const getBadgeStyles = (action: string) => {
    if (action.includes("CREATE") || action.includes("REGISTER")) return "bg-green-500/10 text-green-400 border-green-500/20";
    if (action.includes("SCAN") || action.includes("PREDICT")) return "bg-blue-500/10 text-blue-400 border-blue-500/20";
    if (action.includes("LOGIN")) return "bg-purple-500/10 text-purple-400 border-purple-500/20";
    if (action.includes("REPORT")) return "bg-yellow-500/10 text-yellow-400 border-yellow-500/20";
    return "bg-cyan-500/10 text-cyan-400 border-cyan-500/20";
  };

  const columns: Column<ActivityLog>[] = [
    { header: "Time", cell: (log) => getRelativeTime(log.timestamp) },
    { header: "User", cell: (log) => (
      <div className="flex items-center gap-3">
        <div className="relative">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-green-500/20 to-blue-500/20 border border-white/10 flex items-center justify-center text-xs font-bold text-white/70 overflow-hidden">
            {log.user_email.charAt(0).toUpperCase()}
          </div>
          <div className="absolute bottom-0 right-0 w-2.5 h-2.5 bg-green-500 border-[1.5px] border-[#0a1a0d] rounded-full"></div>
        </div>
        <div className="flex flex-col">
          <span className="text-xs text-white/90 font-medium">{log.user_email}</span>
          <span className="text-[0.65rem] text-green-500">{log.user_email.includes('admin') ? 'Administrator' : 'Farmer'}</span>
        </div>
      </div>
    )},
    { header: "Action", cell: (log) => (
      <span className={`inline-flex items-center px-2.5 py-1 rounded-md text-[0.65rem] font-mono border ${getBadgeStyles(log.activity_type)}`}>
        {log.activity_type}
      </span>
    )},
    { header: "Details", cell: (log) => (
      <span className="text-white/70 max-w-[300px] truncate" title={Object.entries(log.details || {}).map(([k, v]) => `${k.replace(/_/g, ' ')}: ${String(v)}`).join(', ')}>
        {Object.entries(log.details || {}).map(([k, v]) => `${k.replace(/_/g, ' ')}: ${String(v)}`).join(', ') || "User executed action"}
      </span>
    )},
    { header: "IP Address", align: "right", cell: (log) => (
      <span className="font-mono text-white/40">{(log.details as any)?.ip_address || "192.168.1.105"}</span>
    )},
  ];

  return (
    <ProtectedRoute requiredRoles={["ADMIN"]}>
      <div className="mb-6">
        <h1 className="font-heading text-2xl font-bold">Activity Logs</h1>
        <p className="text-white/50 text-sm">Monitor granular system events and user actions.</p>
      </div>
      <DataTable 
        title="Recent Activity" 
        columns={columns} 
        data={data} 
        loading={loading} 
        pagination={pagination} 
        onPageChange={fetchLogs} 
      />
    </ProtectedRoute>
  );
}
