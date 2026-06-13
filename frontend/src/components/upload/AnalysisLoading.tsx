"use client";

import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";

export interface AnalysisLoadingProps {
  isVisible: boolean;
  className?: string;
}

const STAGES = [
  "Uploading Image...",
  "Analyzing Disease...",
  "Generating Recommendations...",
  "Preparing Results...",
];

export function AnalysisLoading({ isVisible, className }: AnalysisLoadingProps) {
  const [currentStage, setCurrentStage] = useState(0);

  useEffect(() => {
    if (!isVisible) {
      setCurrentStage(0);
      return;
    }

    // Simulate progress through analysis stages
    const interval = setInterval(() => {
      setCurrentStage((prev) => {
        if (prev >= STAGES.length - 1) {
          return prev;
        }
        return prev + 1;
      });
    }, 1500);

    return () => clearInterval(interval);
  }, [isVisible]);

  if (!isVisible) return null;

  return (
    <div 
      className={cn("flex flex-col gap-[12px] mx-auto mt-[24px] w-full max-w-[380px]", className)}
      aria-live="polite"
      aria-busy="true"
    >
      {/* Screen reader only status update */}
      <div className="sr-only">
        {`Analysis in progress: ${STAGES[currentStage]}`}
      </div>
      
      {STAGES.map((stageName, index) => {
        const isActive = index === currentStage;
        const isDone = index < currentStage;
        
        return (
          <div
            key={stageName}
            className={cn(
              "flex items-center gap-[14px] p-[14px_20px] rounded-[var(--radius-sm,0.25rem)] transition-all duration-500 font-mono text-[0.85rem]",
              "bg-white/[0.03] border border-white/[0.07] opacity-30",
              isActive && "opacity-100 border-[#22c55e]/30 bg-[#22c55e]/[0.06]",
              isDone && "opacity-70 text-white/50"
            )}
            aria-hidden="true" // Hide decorative steps from SR to avoid redundant reading
          >
            <div 
              className={cn(
                "w-[8px] h-[8px] rounded-full shrink-0 bg-white/20 transition-all duration-300",
                isActive && "bg-[#22c55e] shadow-[0_0_8px_rgba(34,197,94,0.6)] animate-pulse [animation-duration:0.8s]",
                isDone && "bg-[#22c55e]"
              )}
            />
            {stageName}
          </div>
        );
      })}
    </div>
  );
}
