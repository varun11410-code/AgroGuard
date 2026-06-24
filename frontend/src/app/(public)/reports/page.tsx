"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { useAuth } from "@/contexts/AuthContext";
import { reportService, ReportMetadata } from "@/services/report";
import { FileText, Download, ArrowRight, Activity, AlertCircle } from "lucide-react";

export default function ReportsHistoryPage() {
  const { status: authStatus } = useAuth();
  const [reports, setReports] = useState<ReportMetadata[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [downloadingId, setDownloadingId] = useState<string | null>(null);

  useEffect(() => {
    if (authStatus === "authenticated") {
      fetchReports();
    }
  }, [authStatus]);

  const fetchReports = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await reportService.getHistory();
      setReports(data);
    } catch (err: any) {
      setError(err.message || "Failed to load report history.");
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (reportId: string) => {
    if (downloadingId) return;
    setDownloadingId(reportId);
    try {
      await reportService.downloadHistoricalReport(reportId);
    } catch (err: any) {
      alert(err.message || "Failed to download report");
    } finally {
      setDownloadingId(null);
    }
  };

  // Helper to format date
  const formatDate = (isoString?: string) => {
    if (!isoString) return "Unknown date";
    const date = new Date(isoString);
    return date.toLocaleDateString(undefined, {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  if (authStatus === "loading" || loading) {
    return (
      <ProtectedRoute>
        <main className="max-w-4xl mx-auto pt-[140px] pb-[80px] px-6 min-h-screen relative">
          <h1 className="text-3xl font-bold font-heading mb-8">Report History</h1>
          <div className="flex flex-col items-center justify-center p-12 glass rounded-2xl">
            <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin mb-4"></div>
            <p className="text-muted-foreground">Loading your reports...</p>
          </div>
        </main>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <main className="max-w-4xl mx-auto pt-[140px] pb-[80px] px-6 min-h-screen relative">
        <h1 className="text-3xl font-bold font-heading mb-8 flex items-center gap-3">
          <FileText className="w-8 h-8 text-primary" />
          Report History
        </h1>

        {error ? (
          <div className="glass p-8 text-center rounded-2xl flex flex-col items-center gap-4">
            <AlertCircle className="w-12 h-12 text-destructive" />
            <div className="text-destructive font-medium">{error}</div>
            <button
              onClick={fetchReports}
              className="mt-4 px-4 py-2 bg-primary text-primary-foreground rounded-full text-sm font-medium hover:bg-primary/90 transition-colors"
            >
              Try Again
            </button>
          </div>
        ) : reports.length === 0 ? (
          <div className="glass p-12 text-center rounded-2xl flex flex-col items-center gap-4">
            <FileText className="w-16 h-16 text-muted-foreground opacity-50 mb-2" />
            <h2 className="text-xl font-bold font-heading">No Reports Found</h2>
            <p className="text-muted-foreground max-w-md">
              You haven't generated any detailed AI advisory reports yet. 
              Go to your Scan History, select a scan, and click "View Report" to generate one.
            </p>
            <Link 
              href="/history"
              className="mt-6 flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-full font-medium hover:bg-primary/90 transition-colors shadow-lg hover:shadow-xl"
            >
              View Scan History <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        ) : (
          <div className="history-list space-y-4">
            {reports.map((report) => (
              <div key={report.id} className="history-item glass p-4 rounded-xl flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between hover:bg-white/10 transition-colors border border-white/10">
                <div className="flex items-center gap-4 flex-1">
                  <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center shrink-0">
                    <FileText className="w-6 h-6 text-primary" />
                  </div>
                  <div className="hist-info">
                    <h3 className="font-bold text-lg font-heading">{report.scan.crop_name}</h3>
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <Activity className="w-3 h-3 text-destructive" />
                        {report.scan.predicted_disease}
                      </span>
                      <span>•</span>
                      <span>{Math.round(report.scan.confidence_score * 100)}% Match</span>
                    </div>
                    <p className="text-xs text-muted-foreground mt-1">{formatDate(report.generated_at)}</p>
                  </div>
                </div>
                
                <div className="hist-actions w-full sm:w-auto flex justify-end">
                  <button
                    onClick={() => handleDownload(report.id)}
                    disabled={downloadingId === report.id}
                    className="flex items-center justify-center gap-2 px-4 py-2 bg-secondary text-secondary-foreground rounded-full text-sm font-medium hover:bg-secondary/80 transition-colors w-full sm:w-auto disabled:opacity-50"
                  >
                    {downloadingId === report.id ? (
                      <>
                        <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></div>
                        <span>Downloading...</span>
                      </>
                    ) : (
                      <>
                        <Download className="w-4 h-4" />
                        <span>Download PDF</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </ProtectedRoute>
  );
}
