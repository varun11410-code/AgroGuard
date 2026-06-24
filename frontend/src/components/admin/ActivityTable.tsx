"use client";

import { ActivityLog } from "@/services/admin";

interface ActivityTableProps {
  logs: ActivityLog[];
}

export function ActivityTable({ logs }: ActivityTableProps) {
  if (logs.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground border rounded-[var(--radius)] border-white/10 bg-background/50 backdrop-blur-sm">
        No activity logs found.
      </div>
    );
  }

  return (
    <div className="rounded-[var(--radius)] border border-white/10 bg-background/50 backdrop-blur-sm overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="text-xs text-muted-foreground uppercase bg-white/5 border-b border-white/10">
            <tr>
              <th scope="col" className="px-6 py-4 font-medium">Type</th>
              <th scope="col" className="px-6 py-4 font-medium">User</th>
              <th scope="col" className="px-6 py-4 font-medium">Details</th>
              <th scope="col" className="px-6 py-4 font-medium text-right">Time</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td className="px-6 py-4">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary/10 text-primary border border-primary/20">
                    {log.activity_type}
                  </span>
                </td>
                <td className="px-6 py-4 font-medium text-foreground">
                  {log.user_email}
                </td>
                <td className="px-6 py-4 text-muted-foreground max-w-xs truncate">
                  {JSON.stringify(log.details).replace(/[{}""]/g, " ").trim() || "-"}
                </td>
                <td className="px-6 py-4 text-right text-muted-foreground whitespace-nowrap">
                  {new Date(log.timestamp).toLocaleString("en-US", {
                    month: "short",
                    day: "numeric",
                    year: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
