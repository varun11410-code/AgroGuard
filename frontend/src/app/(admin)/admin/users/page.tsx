"use client";

import { useState, useEffect } from "react";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { DataTable, Column } from "@/components/admin/DataTable";
import { adminService, AdminUser, PaginationMeta } from "@/services/admin";

export default function AdminUsersPage() {
  const [data, setData] = useState<AdminUser[]>([]);
  const [pagination, setPagination] = useState<PaginationMeta | undefined>();
  const [loading, setLoading] = useState(true);

  const fetchUsers = async (page: number = 1) => {
    try {
      setLoading(true);
      const res = await adminService.getUsers(page);
      setData(res.users);
      setPagination(res.pagination);
    } catch (err) {
      console.error("Failed to fetch users:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const columns: Column<AdminUser>[] = [
    { header: "Name", accessorKey: "name" },
    { header: "Email", accessorKey: "email" },
    { header: "Role", cell: (u) => (
      <span className={`px-2 py-1 rounded text-[0.65rem] font-mono border ${u.role === 'ADMIN' ? 'bg-purple-500/10 text-purple-400 border-purple-500/20' : 'bg-green-500/10 text-green-400 border-green-500/20'}`}>
        {u.role}
      </span>
    ) },
    { header: "Created At", cell: (u) => new Date(u.created_at).toLocaleDateString() },
  ];

  return (
    <ProtectedRoute requiredRoles={["ADMIN"]}>
      <div className="mb-6">
        <h1 className="font-heading text-2xl font-bold">User Management</h1>
        <p className="text-white/50 text-sm">View and manage registered users.</p>
      </div>
      <DataTable 
        title="All Users" 
        columns={columns} 
        data={data} 
        loading={loading} 
        pagination={pagination} 
        onPageChange={fetchUsers} 
      />
    </ProtectedRoute>
  );
}
