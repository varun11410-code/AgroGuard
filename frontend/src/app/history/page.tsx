"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { scanService, HistoryScan } from "@/services/scan";
import { reportService, ReportDataPayload } from "@/services/report";
import { useAuth } from "@/contexts/AuthContext";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { cn } from "@/lib/utils";

const CROP_EMOJIS: Record<string, string> = {
  "Tomato": "🍅",
  "Potato": "🥔"
};

export default function HistoryPage() {
  const router = useRouter();
  const { status: authStatus } = useAuth();
  const [scans, setScans] = useState<HistoryScan[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [downloadingId, setDownloadingId] = useState<string | null>(null);

  useEffect(() => {
    if (authStatus === "authenticated") {
      const fetchHistory = async () => {
        try {
          const data = await scanService.getHistory();
          setScans(data);
        } catch (err: unknown) {
          setError(err instanceof Error ? err.message : "Failed to load history");
        } finally {
          setLoading(false);
        }
      };

      fetchHistory();
    }
  }, [authStatus]);

  const handleViewReport = async (scan: HistoryScan) => {
    if (downloadingId) return;
    
    setDownloadingId(scan.id);
    try {
      const payload: ReportDataPayload = {
        crop: scan.crop_name,
        disease: scan.predicted_disease || "Unsupported",
        confidence: scan.confidence_score || 0.0,
        selected_plan: null,
        image_stream: null,
        ai_summary: null,
        treatment_recommendations: [],
        prevention_suggestions: []
      };
      
      await reportService.downloadReport(payload);
    } catch (err) {
      console.error("Failed to download report:", err);
      alert("Failed to download report. Please try again.");
    } finally {
      setDownloadingId(null);
    }
  };

  if (authStatus === "loading" || loading) {
    return (
      <ProtectedRoute>
        <main className="pt-[140px] pb-[80px] min-h-screen flex items-center justify-center">
          <div className="w-full max-w-4xl px-6">
            <div className="flex flex-col items-center justify-center p-12 glass rounded-2xl">
              <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin mb-4"></div>
              <p className="text-muted-foreground">Loading your past diagnoses...</p>
            </div>
          </div>
        </main>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
    <main className="pt-[140px] pb-[80px] min-h-screen relative">
      <div className="container mx-auto px-6 max-w-[800px]">
        
        <div className="text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-primary/10 border border-primary/20 text-primary font-mono text-sm mb-4">
            Platform Features
          </div>
          <h1 className="font-heading text-4xl md:text-5xl font-extrabold tracking-tight mb-4">
            Scan History
          </h1>
          <p className="text-muted-foreground text-lg mb-10">
            Review historical scans, compare results, and track crop health over time.
          </p>
        </div>

        {error ? (
          <div className="glass p-8 text-center text-red-400 border border-red-500/20">
            {error}
          </div>
        ) : scans.length === 0 ? (
          <div className="glass p-12 text-center rounded-2xl">
            <div className="text-5xl mb-4">📝</div>
            <h3 className="font-heading text-2xl font-bold mb-2">No History Found</h3>
            <p className="text-white/40 font-mono text-sm">
              You haven&apos;t analyzed any crops yet. Upload an image to get started.
            </p>
            <button 
              onClick={() => router.push("/upload")}
              className="mt-6 px-6 py-3 rounded-xl bg-primary/10 border border-primary/20 text-primary font-bold hover:bg-primary/20 transition-all"
            >
              Start Scanning
            </button>
          </div>
        ) : (
          <div className="history-list mt-[50px] flex flex-col gap-[16px]">
            {scans.map((scan) => {
              const emoji = CROP_EMOJIS[scan.crop_name] || "🌿";
              const confidencePct = scan.confidence_score ? (scan.confidence_score * 100).toFixed(1) : "0.0";
              const isDownloading = downloadingId === scan.id;

              return (
                <div key={scan.id} className="glass history-item p-[24px_28px] grid grid-cols-[auto_1fr_auto_auto] items-center gap-[24px] transition-all duration-300 hover:translate-x-[6px] rounded-2xl">
                  <div className="hist-crop text-[1.8rem] leading-none">
                    {emoji}
                  </div>
                  
                  <div className="hist-info flex flex-col">
                    <h4 className="font-heading font-bold text-[0.95rem] mb-[4px]">{scan.crop_name}</h4>
                    <p className="text-[0.8rem] text-white/35 font-mono m-0">{scan.predicted_disease || "Analysis Pending"}</p>
                  </div>
                  
                  <div className="hist-conf text-center col-start-2 row-start-2 md:col-start-auto md:row-start-auto">
                    <div className="conf-num font-heading text-[1.2rem] font-extrabold text-[#22c55e]">
                      {confidencePct}%
                    </div>
                    <div className="conf-label text-[0.7rem] text-white/35 font-mono tracking-widest uppercase mt-1">
                      Confidence
                    </div>
                  </div>
                  
                  <div className="hist-actions flex gap-[10px] col-start-2 row-start-3 md:col-start-auto md:row-start-auto justify-start">
                    <button 
                      onClick={() => handleViewReport(scan)}
                      disabled={isDownloading}
                      className={cn(
                        "hist-btn p-[8px_16px] rounded-[8px] text-[0.8rem] font-semibold cursor-pointer transition-all duration-200 font-sans border",
                        isDownloading 
                          ? "bg-white/10 border-white/20 text-white/50" 
                          : "bg-white/5 border-white/10 text-white/70 hover:bg-white/10 hover:text-white"
                      )}
                    >
                      {isDownloading ? "Generating..." : "View Report"}
                    </button>
                    <button 
                      onClick={async () => {
                        if (!window.confirm("Are you sure you want to delete this scan? This action cannot be undone.")) return;
                        
                        // Optimistic update
                        const previousScans = [...scans];
                        setScans(scans.filter(s => s.id !== scan.id));
                        
                        try {
                          await scanService.deleteScan(scan.id);
                        } catch (err) {
                          setScans(previousScans);
                          alert("Failed to delete scan. Please try again.");
                        }
                      }}
                      className="hist-btn danger p-[8px_16px] rounded-[8px] text-[0.8rem] font-semibold cursor-pointer transition-all duration-200 font-sans border bg-red-500/10 border-red-500/20 text-red-400 hover:bg-red-500/20 hover:text-red-300"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </main>
    </ProtectedRoute>
  );
}
