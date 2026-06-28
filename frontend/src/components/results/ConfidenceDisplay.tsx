"use client";

import { cn } from "@/lib/utils";
import { useEffect, useState } from "react";

export interface ConfidenceDisplayProps {
  confidence?: number;
  className?: string;
}

import { normalizeConfidence, getConfidenceTheme } from "@/lib/theme";

export function ConfidenceDisplay({
  confidence,
  className,
}: ConfidenceDisplayProps) {
  const [width, setWidth] = useState(0);

  const normalized = normalizeConfidence(confidence);
  const theme = getConfidenceTheme(confidence);

  useEffect(() => {
    if (normalized !== null) {
      // Delay slightly to ensure CSS transition fires on mount
      const timer = setTimeout(() => {
        setWidth(normalized);
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [normalized]);

  return (
    <article
      aria-labelledby="confidence-heading"
      className={cn(
        "glass-card p-8 transition-all duration-500 hover:-translate-y-1 flex flex-col justify-between min-h-[180px]",
        className
      )}
    >
      <div>
        <h3
          id="confidence-heading"
          className="font-mono text-[0.7rem] uppercase tracking-[0.12em] text-white/35 mb-3"
        >
          Prediction Confidence
        </h3>

        {normalized === null ? (
          <div
            className="text-white/60 font-mono text-[0.9rem] mt-2"
            aria-label="Confidence information unavailable"
          >
            Confidence information unavailable.
          </div>
        ) : (
          <>
            <div
              className={`font-heading text-[1.6rem] font-extrabold tracking-[-0.02em] bg-gradient-to-br ${theme.text} bg-clip-text text-transparent w-fit`}
              aria-hidden="true"
            >
              {normalized.toFixed(1)}%
            </div>

            <div className="confidence-bar mt-4">
              <div
                className="conf-track h-[6px] bg-white/[0.08] rounded-full overflow-hidden"
                role="progressbar"
                aria-valuemin={0}
                aria-valuemax={100}
                aria-valuenow={normalized}
                aria-valuetext={`${normalized.toFixed(1)}% confidence`}
                aria-label={`Prediction confidence ${normalized.toFixed(1)}%`}
              >
                <div
                  className={`conf-fill h-full bg-gradient-to-r ${theme.bar} rounded-full transition-all duration-[1500ms] ease-[cubic-bezier(0.16,1,0.3,1)]`}
                  style={{ width: `${width}%` }}
                />
              </div>
            </div>
          </>
        )}
      </div>
    </article>
  );
}
