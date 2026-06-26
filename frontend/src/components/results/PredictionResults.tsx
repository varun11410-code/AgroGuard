import { useState } from "react";
import { ScanResponse } from "@/services/scan";
import { reportService, buildReportPayload } from "@/services/report";
import { ConfidenceDisplay } from "./ConfidenceDisplay";
import { TreatmentPlanCards, PlanTier } from "./TreatmentPlanCards";
import { DiseaseResultCard } from "./DiseaseResultCard";
import { UploadedImagePreview } from "./UploadedImagePreview";
import { AISummarySection } from "./AISummarySection";
import { cn } from "@/lib/utils";

export interface PredictionResultsProps {
  result: ScanResponse;
  imageUrl?: string | null;
  className?: string;
}

export function PredictionResults({ result, imageUrl, className }: PredictionResultsProps) {
  const [selectedPlan, setSelectedPlan] = useState<PlanTier | null>(null);
  const [isDownloading, setIsDownloading] = useState(false);
  const [downloadError, setDownloadError] = useState<string | null>(null);

  if (!result.prediction) {
    return (
      <section 
        id="dashboard" 
        className={cn("w-full container mx-auto mt-[60px]", className)}
        aria-label="AI Diagnosis Results"
      >
        <div className="glass-card p-8 text-center border border-white/[0.07] bg-white/[0.03]">
          <p className="text-white/60 font-mono text-[0.9rem]">
            Prediction results are currently unavailable.
          </p>
        </div>
      </section>
    );
  }

  const {
    disease,
    confidence,
    crop,
    pathogen,
    riskLevel,
    aiSummary,
    treatmentPlans,
    label,
    is_supported
  } = result.prediction;

  const urlToBase64 = async (url: string): Promise<string> => {
    const response = await fetch(url);
    const blob = await response.blob();
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result as string);
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  };

  const handleDownload = async () => {
    setIsDownloading(true);
    setDownloadError(null);

    try {
      let imageStreamData = imageUrl || null;
      if (imageUrl && imageUrl.startsWith('blob:')) {
        imageStreamData = await urlToBase64(imageUrl);
      }

      const payload = buildReportPayload({
        scan_id: result.scanId,
        crop_name: crop ?? "Unknown Crop",
        predicted_disease: disease ?? "Unknown Disease",
        confidence_score: confidence ?? 0.0,
        selected_plan: selectedPlan,
        image_url: imageStreamData,
        ai_summary: aiSummary,
        risk_level: riskLevel,
        treatment_plans: treatmentPlans
      });

      await reportService.downloadReport(payload);
    } catch (error: any) {
      setDownloadError(error.message || "Failed to download the report.");
    } finally {
      setIsDownloading(false);
    }
  };

  return (
    <section 
      id="dashboard" 
      className={cn("w-full container mx-auto mt-[60px]", className)}
      aria-label="AI Diagnosis Results"
    >
      <div className="mb-[60px] flex flex-col md:flex-row md:items-start justify-between gap-4">
        <div>
          <div className="inline-block font-mono text-[0.8rem] tracking-[0.1em] text-[#22c55e] uppercase mb-3">
            AI Diagnosis
          </div>
          <h2 className="font-heading text-3xl font-bold mb-2">Results Dashboard</h2>
          <p className="text-white/60">
            AI-generated diagnosis with confidence scoring and treatment recommendations.
          </p>
        </div>
        
        <div className="flex flex-col items-end">
          <button
            onClick={handleDownload}
            disabled={isDownloading}
            className={cn(
              "font-heading px-[24px] py-[12px] text-[0.95rem] font-bold text-white rounded-full transition-all duration-300 relative overflow-hidden tracking-[0.01em]",
              "bg-gradient-to-br from-[#166534] to-[#22c55e]",
              "hover:-translate-y-1 hover:shadow-[0_10px_30px_rgba(34,197,94,0.4)]",
              "disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:hover:shadow-none"
            )}
          >
            {isDownloading ? "Generating PDF..." : "Download PDF Report"}
          </button>
          
          {downloadError && (
            <div className="mt-4 p-3 rounded-[var(--radius-sm,0.25rem)] border border-red-500/30 bg-red-500/10 text-red-400 text-xs text-right font-mono max-w-xs">
              {downloadError}
            </div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {/* Detected Disease */}
        <DiseaseResultCard 
          prediction={{
            disease,
            confidence,
            crop,
            label,
            is_supported
          }}
          className="transition-all duration-500 hover:-translate-y-1"
        />

        {/* Confidence Score */}
        <ConfidenceDisplay 
          confidence={confidence} 
          isSupported={is_supported}
          className="transition-all duration-500 hover:-translate-y-1 delay-100" 
        />

        {/* Risk Level */}
        <div className="glass-card p-8 transition-all duration-500 hover:-translate-y-1 delay-200">
          <h3 className="font-mono text-[0.7rem] uppercase tracking-[0.12em] text-white/35 mb-3">
            Risk Level
          </h3>
          <div className="font-heading text-[1.6rem] font-extrabold tracking-[-0.02em] text-red-500">
            {riskLevel || "Unknown"} <span aria-hidden="true">⚠</span>
          </div>
          <div className="mt-3 text-[0.8rem] text-red-500/60">
            {riskLevel === "High" ? "Immediate treatment recommended" : "Monitor closely"}
          </div>
        </div>

        {/* Uploaded Image Preview */}
        <UploadedImagePreview 
          imageUrl={imageUrl} 
          disease={disease}
          className="transition-all duration-500 hover:-translate-y-1 delay-300" 
        />

        {/* AI Summary */}
        <AISummarySection 
          summary={aiSummary} 
          className="col-span-1 sm:col-span-2 lg:col-span-3 transition-all duration-500 font-sans" 
        />

        {/* Recommendations */}
        <TreatmentPlanCards 
          plans={treatmentPlans} 
          selectedPlan={selectedPlan}
          onPlanSelect={setSelectedPlan}
        />
      </div>
    </section>
  );
}
