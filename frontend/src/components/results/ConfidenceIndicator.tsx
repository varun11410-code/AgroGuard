"use client";

import { cn } from "@/lib/utils";
import { useEffect, useState } from "react";

export interface ConfidenceIndicatorProps {
  confidence: number;
  className?: string;
}

export function ConfidenceIndicator({ confidence, className }: ConfidenceIndicatorProps) {
  const [width, setWidth] = useState(0);

  const normalizedConfidence = confidence <= 1 ? confidence * 100 : confidence;
  const clampedConfidence = Math.max(0, Math.min(100, normalizedConfidence));

  useEffect(() => {
    // Delay slightly to ensure CSS transition fires on mount
    const timer = setTimeout(() => {
      setWidth(clampedConfidence);
    }, 100);
    return () => clearTimeout(timer);
  }, [clampedConfidence]);

  return (
    <div className={cn("glass-card p-8", className)}>
      <h3 className="font-mono text-[0.7rem] uppercase tracking-[0.12em] text-white/35 mb-3">
        Confidence Score
      </h3>
      <div 
        className="font-heading text-[1.6rem] font-extrabold tracking-[-0.02em] bg-gradient-to-br from-[#22c55e] to-[#86efac] bg-clip-text text-transparent w-fit"
        aria-hidden="true"
      >
        {clampedConfidence.toFixed(1)}%
      </div>
      <div className="mt-4" aria-label={`Confidence score: ${clampedConfidence.toFixed(1)} percent`}>
        <div className="h-[6px] bg-white/[0.08] rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-[#166534] to-[#22c55e] rounded-full transition-all duration-[1500ms] ease-[cubic-bezier(0.16,1,0.3,1)]"
            style={{ width: `${width}%` }}
            role="progressbar"
            aria-valuenow={clampedConfidence}
            aria-valuemin={0}
            aria-valuemax={100}
          />
        </div>
      </div>
    </div>
  );
}
