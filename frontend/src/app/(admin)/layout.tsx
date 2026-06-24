import { AdminSidebar } from "@/components/admin/AdminSidebar";
import { AdminTopbar } from "@/components/admin/AdminTopbar";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen bg-[#050d07] text-white selection:bg-green-500/30">
      <AdminSidebar />
      <div className="flex-1 md:ml-[260px] flex flex-col min-h-screen relative z-10">
        <AdminTopbar />
        <main className="flex-1 p-8 space-y-6">
          {children}
        </main>
      </div>
    </div>
  );
}
