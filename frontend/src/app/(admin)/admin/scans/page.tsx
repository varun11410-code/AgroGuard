"use client";

import { useState, useEffect } from "react";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { DataTable, Column } from "@/components/admin/DataTable";
import { adminService, AdminScan, PaginationMeta } from "@/services/admin";

export default function AdminScansPage() {
  const [data, setData] = useState<AdminScan[]>([]);
  const [pagination, setPagination] = useState<PaginationMeta | undefined>();
  const [loading, setLoading] = useState(true);

  const fetchScans = async (page: number = 1) => {
    try {
      setLoading(true);
      const res = await adminService.getScans(page);
      setData(res.scans);
      setPagination(res.pagination);
    } catch (err) {
      console.error("Failed to fetch scans:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchScans();
  }, []);

  const columns: Column<AdminScan>[] = [
    { header: "Date", cell: (s) => new Date(s.created_at).toLocaleDateString() },
    { header: "User", accessorKey: "user_email" },
    { header: "Crop", accessorKey: "crop" },
    { header: "Disease", cell: (s) => (
      <span className="text-white/90">{s.disease || "Processing..."}</span>
    ) },
    { header: "Confidence", cell: (s) => (
      <span className="font-mono">{s.confidence ? `${(s.confidence * 100).toFixed(1)}%` : "N/A"}</span>
    ) },
  ];

  return (
    <ProtectedRoute requiredRoles={["ADMIN"]}>
      <div className="mb-6">
        <h1 className="font-heading text-2xl font-bold">Scan History</h1>
        <p className="text-white/50 text-sm">Review global crop scanning activity.</p>
      </div>
      <DataTable 
        title="Recent Scans" 
        columns={columns} 
        data={data} 
        loading={loading} 
        pagination={pagination} 
        onPageChange={fetchScans} 
      />
    </ProtectedRoute>
  );
}
