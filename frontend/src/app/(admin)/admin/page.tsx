"use client";

import { useState, useEffect } from "react";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { Skeleton } from "@/components/ui/skeleton";
import { Users, Scan, Activity, TrendingUp, Bug } from "lucide-react";
import { adminService, DashboardStats, AnalyticsPayload } from "@/services/admin";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip as RechartsTooltip, AreaChart, Area, XAxis, YAxis, CartesianGrid } from "recharts";

const COLORS = ["#a855f7", "#22c55e", "#eab308", "#3b82f6", "#64748b"];

const Sparkline = ({ data, color }: { data: number[], color: string }) => {
  if (!data || data.length === 0) return <div className="h-8 mt-4"></div>;
  const max = Math.max(...data) || 1;
  const points = data.map((d, i) => `${(i / (data.length - 1)) * 100},${30 - (d / max) * 20}`).join(" ");
  return (
    <svg className="w-full h-8 mt-4 overflow-visible" viewBox="0 0 100 30" preserveAspectRatio="none">
      <polyline points={points} fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      <circle cx="100" cy={30 - (data[data.length - 1] / max) * 20} r="3" fill={color} />
    </svg>
  );
};

export default function AdminDashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [analytics, setAnalytics] = useState<AnalyticsPayload | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    const fetchData = async () => {
      try {
        setLoading(true);
        const [statsData, analyticsData] = await Promise.all([
          adminService.getStats(),
          adminService.getAnalytics()
        ]);
        if (mounted) {
          setStats(statsData);
          setAnalytics(analyticsData);
        }
      } catch (err) {
        console.error("Failed to fetch dashboard data:", err);
      } finally {
        if (mounted) setLoading(false);
      }
    };
    fetchData();
    return () => { mounted = false; };
  }, []);

  const topDisease = stats?.top_diseases?.[0];
  const donutData = stats?.top_diseases?.map((d) => ({ name: d.disease, value: d.count })) || [];
  if (donutData.length > 0 && donutData.length < 5 && stats) {
    donutData.push({ name: "Other", value: Math.max(1, Math.floor(stats.total_scans * 0.12)) });
  }
  const totalDonut = donutData.reduce((acc, curr) => acc + curr.value, 0);

  return (
    <ProtectedRoute requiredRoles={["ADMIN"]}>
      {/* Header */}
      <div className="mb-8">
        <h1 className="font-heading text-3xl font-extrabold tracking-tight mb-2">Admin Dashboard</h1>
        <p className="text-muted-foreground text-sm">Monitor system performance and user activity in real-time</p>
      </div>

      {/* Top Stat Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* Card 1: Total Users */}
        <div className="bg-[#0a1a0d]/40 backdrop-blur-sm border border-white/5 rounded-2xl p-5 flex flex-col justify-between hover:border-white/10 transition-colors">
          <div className="flex items-start justify-between mb-2">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-green-500/10 flex items-center justify-center text-green-500">
                <Users size={18} />
              </div>
              <div className="text-[0.7rem] text-white/40 font-mono tracking-widest uppercase">Total Users</div>
            </div>
          </div>
          <div className="flex items-baseline gap-3 mt-2">
            <h3 className="font-heading text-3xl font-bold">
              {loading ? <Skeleton className="h-8 w-20 bg-white/10" /> : stats?.total_users.toLocaleString() || "—"}
            </h3>
            {!loading && analytics && (
              <span className="text-green-500 text-[0.75rem] font-medium flex items-center gap-0.5">
                <TrendingUp size={12} /> {analytics.user_growth.percentage}%
              </span>
            )}
          </div>
          <div className="text-[0.65rem] text-white/30 mt-1">vs last month</div>
          {!loading && analytics && <Sparkline data={analytics.user_growth.sparkline} color="#22c55e" />}
        </div>

        {/* Card 2: Total Scans */}
        <div className="bg-[#0a1a0d]/40 backdrop-blur-sm border border-white/5 rounded-2xl p-5 flex flex-col justify-between hover:border-white/10 transition-colors">
          <div className="flex items-start justify-between mb-2">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-blue-500/10 flex items-center justify-center text-blue-500">
                <Scan size={18} />
              </div>
              <div className="text-[0.7rem] text-white/40 font-mono tracking-widest uppercase">Total Scans</div>
            </div>
          </div>
          <div className="flex items-baseline gap-3 mt-2">
            <h3 className="font-heading text-3xl font-bold">
              {loading ? <Skeleton className="h-8 w-20 bg-white/10" /> : stats?.total_scans.toLocaleString() || "—"}
            </h3>
            {!loading && analytics && (
              <span className="text-green-500 text-[0.75rem] font-medium flex items-center gap-0.5">
                <TrendingUp size={12} /> {analytics.scan_growth.percentage}%
              </span>
            )}
          </div>
          <div className="text-[0.65rem] text-white/30 mt-1">vs last month</div>
          {!loading && analytics && <Sparkline data={analytics.scan_growth.sparkline} color="#3b82f6" />}
        </div>

        {/* Card 3: Top Disease */}
        <div className="bg-[#0a1a0d]/40 backdrop-blur-sm border border-white/5 rounded-2xl p-5 flex flex-col justify-between hover:border-white/10 transition-colors">
          <div className="flex items-start justify-between mb-2">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-purple-500/10 flex items-center justify-center text-purple-500">
                <Bug size={18} />
              </div>
              <div className="text-[0.7rem] text-white/40 font-mono tracking-widest uppercase">Top Disease</div>
            </div>
          </div>
          <div className="mt-2">
            <h3 className="font-heading text-2xl font-bold truncate">
              {loading ? <Skeleton className="h-8 w-24 bg-white/10" /> : topDisease?.disease || "None"}
            </h3>
          </div>
          <div className="text-[0.65rem] text-white/40 mt-1">
            {loading ? "" : `${((topDisease?.count || 0) / (stats?.total_scans || 1) * 100).toFixed(1)}% of total`}
          </div>
          <div className="h-8 mt-4"></div>
        </div>

        {/* Card 4: Active Today */}
        <div className="bg-[#0a1a0d]/40 backdrop-blur-sm border border-white/5 rounded-2xl p-5 flex flex-col justify-between hover:border-white/10 transition-colors">
          <div className="flex items-start justify-between mb-2">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-yellow-500/10 flex items-center justify-center text-yellow-500">
                <Activity size={18} />
              </div>
              <div className="text-[0.7rem] text-white/40 font-mono tracking-widest uppercase">Active Today</div>
            </div>
          </div>
          <div className="flex items-baseline gap-3 mt-2">
            <h3 className="font-heading text-3xl font-bold">
              {loading ? <Skeleton className="h-8 w-16 bg-white/10" /> : analytics?.active_today.count || "0"}
            </h3>
            {!loading && analytics && (
              <span className="text-green-500 text-[0.75rem] font-medium flex items-center gap-0.5">
                <TrendingUp size={12} /> {analytics.active_today.previous > 0 ? Math.round(((analytics.active_today.count - analytics.active_today.previous) / analytics.active_today.previous) * 100) : 0}%
              </span>
            )}
          </div>
          <div className="text-[0.65rem] text-white/30 mt-1">vs yesterday</div>
          <div className="h-8 mt-4"></div>
        </div>
      </div>

      {/* Middle Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-[1.5fr_1fr] gap-4 mt-6">
        {/* Area Chart */}
        <div className="bg-[#0a1a0d]/40 backdrop-blur-sm border border-white/5 rounded-2xl p-6 flex flex-col">
          <div className="flex items-center justify-between mb-6">
            <h3 className="font-bold text-sm text-white/90">Scans Overview</h3>
            <div className="text-[0.7rem] bg-white/5 border border-white/10 px-3 py-1.5 rounded-md text-white/60 flex items-center gap-2 cursor-pointer hover:text-white transition-colors">
              Last 7 Days
            </div>
          </div>
          <div className="h-[250px] w-full">
            {loading ? <Skeleton className="w-full h-full bg-white/10 rounded-xl" /> : (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={analytics?.scans_overview || []} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorScans" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#22c55e" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(255,255,255,0.05)" />
                  <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: 'rgba(255,255,255,0.3)', fontSize: 10 }} dy={10} />
                  <YAxis axisLine={false} tickLine={false} tick={{ fill: 'rgba(255,255,255,0.3)', fontSize: 10 }} />
                  <RechartsTooltip 
                    contentStyle={{ backgroundColor: '#0f2414', borderColor: 'rgba(34,197,94,0.2)', borderRadius: '8px', fontSize: '12px' }}
                    itemStyle={{ color: '#22c55e' }}
                  />
                  <Area type="monotone" dataKey="scans" stroke="#22c55e" strokeWidth={2} fillOpacity={1} fill="url(#colorScans)" activeDot={{ r: 6, fill: '#22c55e', stroke: '#050d07', strokeWidth: 2 }} />
                </AreaChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        {/* Donut Chart */}
        <div className="bg-[#0a1a0d]/40 backdrop-blur-sm border border-white/5 rounded-2xl p-6 flex flex-col">
          <div className="flex items-center justify-between mb-6">
            <h3 className="font-bold text-sm text-white/90">Top Diseases</h3>
            <div className="text-[0.7rem] bg-white/5 border border-white/10 px-3 py-1.5 rounded-md text-white/60 flex items-center gap-2 cursor-pointer hover:text-white transition-colors">
              View All
            </div>
          </div>
          
          {loading ? (
            <div className="flex-1 flex items-center justify-center"><Skeleton className="h-[200px] w-[200px] rounded-full bg-white/10" /></div>
          ) : donutData.length === 0 ? (
            <div className="flex-1 flex items-center justify-center text-white/30 text-sm">No disease data</div>
          ) : (
            <div className="flex flex-col sm:flex-row items-center gap-8 flex-1">
              <div className="h-[180px] w-[180px] relative">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={donutData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={85}
                      paddingAngle={2}
                      dataKey="value"
                      stroke="none"
                    >
                      {donutData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <RechartsTooltip 
                      contentStyle={{ backgroundColor: '#0f2414', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '12px', border: '1px solid rgba(255,255,255,0.1)' }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              
              <div className="flex-1 w-full space-y-3">
                {donutData.map((entry, index) => (
                  <div key={index} className="flex items-center justify-between text-xs">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 rounded-full" style={{ backgroundColor: COLORS[index % COLORS.length] }}></div>
                      <span className="text-white/70 max-w-[100px] truncate" title={entry.name}>{entry.name}</span>
                    </div>
                    <span className="text-white/90 font-mono">{((entry.value / totalDonut) * 100).toFixed(1)}%</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </ProtectedRoute>
  );
}
