"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { DashboardStats } from "@/services/admin";
import { Users, Scan, AlertTriangle } from "lucide-react";

interface StatsCardsProps {
  stats: DashboardStats;
}

export function StatsCards({ stats }: StatsCardsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <Card className="bg-background/50 backdrop-blur-sm border-white/10">
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">Total Users</CardTitle>
          <Users className="h-4 w-4 text-primary" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.total_users}</div>
        </CardContent>
      </Card>

      <Card className="bg-background/50 backdrop-blur-sm border-white/10">
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">Total Scans</CardTitle>
          <Scan className="h-4 w-4 text-primary" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.total_scans}</div>
        </CardContent>
      </Card>

      <Card className="bg-background/50 backdrop-blur-sm border-white/10">
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">Top Disease</CardTitle>
          <AlertTriangle className="h-4 w-4 text-orange-400" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold truncate">
            {stats.top_diseases.length > 0 ? stats.top_diseases[0].disease : "N/A"}
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            {stats.top_diseases.length > 0 ? `${stats.top_diseases[0].count} occurrences` : "No data"}
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
