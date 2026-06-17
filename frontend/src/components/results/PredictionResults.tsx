import { ScanResponse } from "@/services/scan";
import { ConfidenceDisplay } from "./ConfidenceDisplay";
import { TreatmentPlanCards } from "./TreatmentPlanCards";
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

  return (
    <section 
      id="dashboard" 
      className={cn("w-full container mx-auto mt-[60px]", className)}
      aria-label="AI Diagnosis Results"
    >
      <div className="mb-[60px]">
        <div className="inline-block font-mono text-[0.8rem] tracking-[0.1em] text-[#22c55e] uppercase mb-3">
          AI Diagnosis
        </div>
        <h2 className="font-heading text-3xl font-bold mb-2">Results Dashboard</h2>
        <p className="text-white/60">
          AI-generated diagnosis with confidence scoring and treatment recommendations.
        </p>
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
        <TreatmentPlanCards plans={treatmentPlans} />
      </div>
    </section>
  );
}
