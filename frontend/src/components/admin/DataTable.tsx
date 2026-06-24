"use client";

import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import { PaginationMeta } from "@/services/admin";
import { ReactNode } from "react";

export interface Column<T> {
  header: string;
  accessorKey?: keyof T;
  cell?: (item: T) => ReactNode;
  align?: "left" | "center" | "right";
}

interface DataTableProps<T> {
  title: string;
  description?: string;
  columns: Column<T>[];
  data: T[];
  loading: boolean;
  pagination?: PaginationMeta;
  onPageChange?: (page: number) => void;
  emptyMessage?: string;
}

export function DataTable<T>({
  title,
  description,
  columns,
  data,
  loading,
  pagination,
  onPageChange,
  emptyMessage = "No data found."
}: DataTableProps<T>) {
  return (
    <div className="bg-[#0a1a0d]/40 backdrop-blur-sm border border-white/5 rounded-2xl overflow-hidden mt-6">
      <div className="p-5 border-b border-white/5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h3 className="font-bold text-sm text-white/90">{title}</h3>
          {description && <p className="text-[0.75rem] text-white/50 mt-1">{description}</p>}
        </div>
      </div>
      
      <div className="overflow-x-auto w-full">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-white/5 text-[0.65rem] font-mono text-white/40 uppercase tracking-widest bg-white/[0.01]">
              {columns.map((col, i) => (
                <th key={i} className={`font-normal px-6 py-4 text-${col.align || 'left'}`}>
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading ? (
              [...Array(5)].map((_, i) => (
                <tr key={i} className="border-b border-white/5">
                  {columns.map((_, j) => (
                    <td key={j} className="px-6 py-4">
                      <Skeleton className="h-4 w-full bg-white/10" />
                    </td>
                  ))}
                </tr>
              ))
            ) : data.length === 0 ? (
              <tr>
                <td colSpan={columns.length} className="px-6 py-12 text-center text-white/30 text-sm">
                  {emptyMessage}
                </td>
              </tr>
            ) : (
              data.map((item, i) => (
                <tr key={i} className="border-b border-white/5 hover:bg-white/[0.02] transition-colors group">
                  {columns.map((col, j) => (
                    <td key={j} className={`px-6 py-4 text-xs text-white/70 text-${col.align || 'left'}`}>
                      {col.cell ? col.cell(item) : col.accessorKey ? String(item[col.accessorKey]) : null}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {pagination && onPageChange && (
        <div className="p-4 border-t border-white/5 flex items-center justify-between text-xs bg-white/[0.01]">
          <div className="text-white/40">
            Showing {data.length} results (Page {pagination.page} of {pagination.total_pages})
          </div>
          <div className="flex items-center gap-1 font-mono text-white/50">
            <Button 
              variant="ghost" 
              size="sm" 
              className="h-7 w-7 p-0 hover:bg-white/10 hover:text-white text-white/40"
              onClick={() => onPageChange(Math.max(1, pagination.page - 1))}
              disabled={pagination.page <= 1}
            >
              &lt;
            </Button>
            
            <Button variant="ghost" size="sm" className="h-7 w-7 p-0 border border-green-500/50 text-green-400 bg-green-500/10">
              {pagination.page}
            </Button>
            
            <Button 
              variant="ghost" 
              size="sm" 
              className="h-7 w-7 p-0 hover:bg-white/10 hover:text-white text-white/40"
              onClick={() => onPageChange(Math.min(pagination.total_pages, pagination.page + 1))}
              disabled={pagination.page >= pagination.total_pages}
            >
              &gt;
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
