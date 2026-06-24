"use client";

import { useState, useEffect } from "react";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { DataTable, Column } from "@/components/admin/DataTable";
import { adminService, AdminReport, PaginationMeta } from "@/services/admin";

export default function AdminReportsPage() {
  const [data, setData] = useState<AdminReport[]>([]);
  const [pagination, setPagination] = useState<PaginationMeta | undefined>();
  const [loading, setLoading] = useState(true);

  const fetchReports = async (page: number = 1) => {
    try {
      setLoading(true);
      const res = await adminService.getReports(page);
      setData(res.reports);
      setPagination(res.pagination);
    } catch (err) {
      console.error("Failed to fetch reports:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const columns: Column<AdminReport>[] = [
    { header: "Generated At", cell: (r) => new Date(r.generated_at).toLocaleString() },
    { header: "User", accessorKey: "user_email" },
    { header: "Scan ID", cell: (r) => <span className="font-mono text-[0.65rem] text-white/50">{r.scan_id}</span> },
    { header: "Report ID", cell: (r) => <span className="font-mono text-[0.65rem] text-white/50">{r.id}</span> },
  ];

  return (
    <ProtectedRoute requiredRoles={["ADMIN"]}>
      <div className="mb-6">
        <h1 className="font-heading text-2xl font-bold">Reports Archive</h1>
        <p className="text-white/50 text-sm">View generated PDF reports.</p>
      </div>
      <DataTable 
        title="All Reports" 
        columns={columns} 
        data={data} 
        loading={loading} 
        pagination={pagination} 
        onPageChange={fetchReports} 
      />
    </ProtectedRoute>
  );
}
