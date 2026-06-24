"use client";

import { useState, useEffect } from "react";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import { Users, Scan, AlertTriangle, Activity } from "lucide-react";
import { adminService, DashboardStats, PaginatedLogs } from "@/services/admin";

export default function AdminDashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [statsLoading, setStatsLoading] = useState(true);
  const [error, setError] = useState(false);

  // Activity Logs State
  const [logData, setLogData] = useState<PaginatedLogs | null>(null);
  const [logsLoading, setLogsLoading] = useState(true);
  const [logsError, setLogsError] = useState(false);
  const [page, setPage] = useState(1);

  useEffect(() => {
    let mounted = true;
    
    const fetchStats = async () => {
      try {
        setStatsLoading(true);
        setError(false);
        const data = await adminService.getStats();
        if (mounted) {
          setStats(data);
        }
      } catch (err) {
        console.error("Failed to fetch admin stats:", err);
        if (mounted) {
          setError(true);
        }
      } finally {
        if (mounted) {
          setStatsLoading(false);
        }
      }
    };

    fetchStats();

    return () => {
      mounted = false;
    };
  }, []);

  useEffect(() => {
    let mounted = true;

    const fetchLogs = async () => {
      try {
        setLogsLoading(true);
        setLogsError(false);
        const data = await adminService.getLogs(page, 20);
        if (mounted) {
          setLogData(data);
        }
      } catch (err) {
        console.error("Failed to fetch admin logs:", err);
        if (mounted) {
          setLogsError(true);
        }
      } finally {
        if (mounted) {
          setLogsLoading(false);
        }
      }
    };

    fetchLogs();

    return () => {
      mounted = false;
    };
  }, [page]);

  const topDisease = stats?.top_diseases?.[0];

  return (
    <ProtectedRoute requiredRoles={["ADMIN"]}>
      <main className="pt-[140px] pb-[80px] min-h-screen relative">
        <div className="container mx-auto px-6 max-w-[1400px] space-y-12">
          
          {/* Header */}
          <div className="section-title">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-green-500/10 border border-green-500/20 text-green-500 font-mono text-sm mb-4">
              <div className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse" />
              Overview
            </div>
            <h2 className="font-heading text-4xl md:text-5xl font-extrabold tracking-tight mb-4">
              Admin Dashboard
            </h2>
            <p className="text-muted-foreground text-lg max-w-[520px] leading-[1.8]">
              Platform statistics and user activity monitoring.
            </p>
          </div>

          {/* Stats Grid Injection Zone */}
          <div id="admin-stats-container" className="grid grid-cols-1 md:grid-cols-3 gap-6 relative z-10">
            {/* Stat Card: Total Users */}
            <div className="glass-strong p-[28px_24px] relative overflow-hidden group hover:border-green-400/50 transition-colors">
              <div className="text-[1.4rem] mb-[10px] text-green-500 opacity-80">
                <Users />
              </div>
              <h3 className="font-display text-[2.2rem] font-extrabold text-green-500 tracking-[-0.03em] bg-gradient-to-br from-green-400 to-green-200 bg-clip-text text-transparent mb-2">
                {statsLoading ? (
                  <Skeleton className="h-10 w-24" />
                ) : error || !stats ? (
                  "—"
                ) : (
                  stats.total_users.toLocaleString()
                )}
              </h3>
              <div className="text-white/45 text-[0.85rem] tracking-[0.02em] font-mono flex items-center gap-2">
                TOTAL USERS
              </div>
            </div>

            {/* Stat Card Placeholder 2 */}
            <div className="glass-strong p-[28px_24px] relative overflow-hidden group hover:border-green-400/50 transition-colors">
              <div className="text-[1.4rem] mb-[10px] text-green-500 opacity-80">
                <Scan />
              </div>
              <h3 className="font-display text-[2.2rem] font-extrabold text-green-500 tracking-[-0.03em] bg-gradient-to-br from-green-400 to-green-200 bg-clip-text text-transparent mb-2">
                {statsLoading ? (
                  <Skeleton className="h-10 w-24" />
                ) : error || !stats ? (
                  "—"
                ) : (
                  stats.total_scans.toLocaleString()
                )}
              </h3>
              <div className="text-white/45 text-[0.85rem] tracking-[0.02em] font-mono flex items-center gap-2">
                TOTAL SCANS
              </div>
            </div>

            {/* Stat Card Placeholder 3 */}
            <div className="glass-strong p-[28px_24px] relative overflow-hidden group hover:border-green-400/50 transition-colors">
              <div className="text-[1.4rem] mb-[10px] text-orange-400 opacity-80">
                <AlertTriangle />
              </div>
              <h3 className="font-display text-[2.2rem] font-extrabold text-green-500 tracking-[-0.03em] bg-gradient-to-br from-green-400 to-green-200 bg-clip-text text-transparent mb-2 flex items-center gap-2">
                {statsLoading ? (
                  <Skeleton className="h-10 w-32" />
                ) : error || !stats ? (
                  "—"
                ) : topDisease ? (
                  topDisease.disease
                ) : (
                  "No Data"
                )}
              </h3>
              <div className="text-white/45 text-[0.85rem] tracking-[0.02em] font-mono flex flex-col gap-2">
                TOP DISEASE
                {statsLoading ? (
                  <Skeleton className="h-4 w-20" />
                ) : error || !stats || !topDisease ? null : (
                  <span>{topDisease.count.toLocaleString()} cases</span>
                )}
              </div>
            </div>
          </div>

          {/* Activity Log Section */}
          <div className="space-y-6 pt-8 border-t border-white/5">
            <div className="flex items-center gap-3">
              <Activity className="text-green-500 w-6 h-6" />
              <h3 className="font-display text-2xl font-bold">Activity Feed</h3>
            </div>

            {/* Activity Table Injection Zone */}
            <div id="admin-activity-container" className="overflow-x-auto w-full glass rounded-[var(--radius)] border border-white/10">
              <div className="min-w-[800px] w-full p-4 space-y-3">
                {/* Table Header */}
                <div className="grid grid-cols-4 gap-4 px-4 py-3 border-b border-white/10 text-xs font-mono text-white/50 uppercase tracking-wider">
                  <div>Type</div>
                  <div>User</div>
                  <div>Details</div>
                  <div className="text-right">Time</div>
                </div>
                
                {/* Table Body */}
                {logsLoading ? (
                  // Loading Skeletons
                  [...Array(5)].map((_, i) => (
                    <div key={i} className="grid grid-cols-4 gap-4 px-4 py-4 border-b border-white/5 items-center hover:bg-white/5 transition-colors rounded-md">
                      <div><Skeleton className="h-6 w-24 rounded-full" /></div>
                      <div><Skeleton className="h-5 w-48" /></div>
                      <div><Skeleton className="h-5 w-full" /></div>
                      <div className="flex justify-end"><Skeleton className="h-5 w-32" /></div>
                    </div>
                  ))
                ) : logsError ? (
                  // Error State
                  <div className="px-4 py-8 text-center text-red-400/80 font-mono text-sm">
                    Failed to load activity logs.
                  </div>
                ) : !logData || logData.logs.length === 0 ? (
                  // Empty State
                  <div className="px-4 py-8 text-center text-white/40 font-mono text-sm">
                    No activity logs found.
                  </div>
                ) : (
                  // Render Logs
                  logData.logs.map((log) => (
                    <div key={log.id} className="grid grid-cols-4 gap-4 px-4 py-4 border-b border-white/5 items-center hover:bg-white/5 transition-colors rounded-md">
                      <div>
                        <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-mono bg-white/5 text-white/70">
                          {log.activity_type.replace(/_/g, ' ')}
                        </span>
                      </div>
                      <div className="text-sm text-white/90 truncate pr-4">
                        {log.user_email}
                      </div>
                      <div className="flex flex-col gap-1 text-[0.8rem] text-white/70">
                        {Object.entries(log.details || {}).map(([key, value]) => (
                          <span key={key} className="truncate max-w-[300px]">
                            <strong className="capitalize text-white/90">{key.replace(/_/g, ' ')}:</strong> {String(value)}
                          </span>
                        ))}
                      </div>
                      <div className="text-right text-xs text-white/50 font-mono">
                        {new Date(log.timestamp).toLocaleString()}
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Pagination Injection Zone */}
            <div id="admin-pagination-container" className="flex items-center justify-between mt-6 px-2">
              {logsLoading ? (
                <Skeleton className="h-5 w-32" />
              ) : logData ? (
                <div className="text-sm text-white/50 font-mono">
                  Showing page {logData.pagination.page} of {Math.max(1, logData.pagination.total_pages)}
                </div>
              ) : (
                <div />
              )}
              
              <div className="flex gap-2">
                {logsLoading ? (
                  <>
                    <Skeleton className="h-9 w-24 rounded-md" />
                    <Skeleton className="h-9 w-24 rounded-md" />
                  </>
                ) : (
                  <>
                    <Button 
                      variant="outline" 
                      onClick={() => setPage(p => Math.max(1, p - 1))}
                      disabled={!logData || page <= 1 || logsLoading}
                      className="border-white/10 hover:bg-white/5 hover:text-white text-white/70"
                    >
                      Previous
                    </Button>
                    <Button 
                      variant="outline" 
                      onClick={() => setPage(p => logData ? Math.min(logData.pagination.total_pages, p + 1) : p)}
                      disabled={!logData || page >= logData.pagination.total_pages || logsLoading}
                      className="border-white/10 hover:bg-white/5 hover:text-white text-white/70"
                    >
                      Next
                    </Button>
                  </>
                )}
              </div>
            </div>
          </div>

        </div>
      </main>
    </ProtectedRoute>
  );
}
