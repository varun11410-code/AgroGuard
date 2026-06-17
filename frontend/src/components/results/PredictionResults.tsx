import { ScanResponse } from "@/services/scan";
import { ConfidenceDisplay } from "./ConfidenceDisplay";
import { RecommendationList } from "./RecommendationList";
import { DiseaseResultCard } from "./DiseaseResultCard";
import { UploadedImagePreview } from "./UploadedImagePreview";
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
        {aiSummary && (
          <div className="glass-card p-[36px] col-span-1 sm:col-span-2 lg:col-span-3 transition-all duration-500">
            <div className="inline-flex items-center gap-[8px] font-mono text-[0.68rem] tracking-[0.1em] px-[14px] py-[6px] rounded-full mb-[20px] bg-[#22c55e]/[0.08] border border-[#22c55e]/20 text-[#22c55e]">
              <span aria-hidden="true">🤖</span> Gemini AI Summary
            </div>
            <p className="text-[0.95rem] text-white/60 leading-[1.85]">
              {aiSummary}
            </p>
          </div>
        )}

        {/* Recommendations */}
        {treatmentPlans && treatmentPlans.length > 0 && (
          <RecommendationList plans={treatmentPlans} />
        )}
      </div>
    </section>
  );
}
