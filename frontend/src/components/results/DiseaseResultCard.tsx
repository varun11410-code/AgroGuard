"use client";

import { cn } from "@/lib/utils";

export interface DiseaseResultCardProps {
  prediction: {
    disease?: string;
    confidence?: number;
    crop?: string;
    label?: string | null;
    is_supported?: boolean;
  } | null | undefined;
  className?: string;
}

export function DiseaseResultCard({ prediction, className }: DiseaseResultCardProps) {
  if (!prediction) {
    return (
      <article
        role="region"
        aria-label="Disease Diagnosis Result"
        className={cn("glass-card p-8 text-center border border-white/[0.07] bg-white/[0.03]", className)}
      >
        <p className="text-white/60 font-mono text-[0.9rem]">
          Prediction results are currently unavailable.
        </p>
      </article>
    );
  }

  const isSupported = prediction.is_supported !== false;

  if (!isSupported) {
    const formattedConfidence = prediction.confidence !== undefined
      ? (prediction.confidence <= 1 ? prediction.confidence * 100 : prediction.confidence)
      : null;

    return (
      <article
        role="region"
        aria-label="Unsupported Prediction Alert"
        className={cn(
          "glass-card p-8 transition-all duration-500 hover:-translate-y-1 hover:shadow-[0_20px_50px_rgba(239,68,68,0.08)] border border-red-500/10 bg-red-500/[0.02] flex flex-col justify-between h-full min-h-[180px]",
          className
        )}
      >
        <div>
          <h3 className="font-mono text-[0.7rem] uppercase tracking-[0.12em] text-red-400/50 mb-3 flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse" />
            AI Diagnosis
          </h3>
          <h4 className="font-heading text-[1.6rem] font-extrabold tracking-[-0.02em] text-red-400 mb-2">
            Unsupported Prediction
          </h4>
          <p className="text-[0.85rem] text-white/60 leading-[1.6]">
            This image appears to be outside AgroGuard&apos;s currently supported crop disease categories.
          </p>
        </div>
        {formattedConfidence !== null && (
          <div className="mt-4 pt-3 border-t border-white/[0.05] text-[0.8rem] text-white/35 font-mono">
            Confidence Score: <span className="text-white/60">{formattedConfidence.toFixed(1)}%</span>
          </div>
        )}
      </article>
    );
  }

  // Supported State
  const { crop, disease, label } = prediction;

  return (
    <article
      role="region"
      aria-label="Disease Diagnosis Result"
      className={cn(
        "glass-card p-8 transition-all duration-500 hover:-translate-y-1 hover:shadow-[0_20px_50px_rgba(34,197,94,0.08)] flex flex-col justify-between h-full min-h-[180px]",
        className
      )}
    >
      <div>
        <h3 className="font-mono text-[0.7rem] uppercase tracking-[0.12em] text-white/35 mb-3 flex items-center gap-2">
          <span className="w-1.5 h-1.5 rounded-full bg-[#22c55e] animate-pulse" />
          Detected Disease
        </h3>
        <h4 className="font-heading text-[1.6rem] font-extrabold tracking-[-0.02em] text-[#86efac] mb-2 leading-tight">
          {disease}
        </h4>
        {crop && (
          <p className="text-[0.95rem] text-white/60 leading-[1.6]">
            Crop: <span className="font-medium text-white/80">{crop}</span>
          </p>
        )}
      </div>

      {label && (
        <div className="mt-4 pt-3 border-t border-white/[0.05] text-[0.8rem] text-white/35 font-mono">
          Label: <span className="text-white/60">{label}</span>
        </div>
      )}
    </article>
  );
}
