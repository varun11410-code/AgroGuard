"use client";

import { cn } from "@/lib/utils";

export interface AISummarySectionProps {
  summary?: string | null;
  className?: string;
}

export function AISummarySection({
  summary,
  className,
}: AISummarySectionProps) {
  const isAvailable = summary !== undefined && summary !== null && summary.trim().length > 0;

  return (
    <article
      aria-labelledby="ai-summary-heading"
      className={cn(
        "glass-card p-[36px] transition-all duration-500 hover:shadow-[0_20px_50px_rgba(34,197,94,0.02)]",
        className
      )}
    >
      <div>
        <div
          id="ai-summary-heading"
          className={cn(
            "inline-flex items-center gap-[8px] font-mono text-[0.68rem] tracking-[0.1em] px-[14px] py-[6px] rounded-full mb-[20px]",
            isAvailable
              ? "bg-[#22c55e]/[0.08] border border-[#22c55e]/20 text-[#22c55e]"
              : "bg-white/[0.03] border border-white/[0.08] text-white/50"
          )}
        >
          <span aria-hidden="true">🤖</span> AI Insights
        </div>

        {isAvailable ? (
          <p className="text-[0.95rem] text-white/60 leading-[1.85] font-sans">
            {summary}
          </p>
        ) : (
          <p className="text-[0.95rem] text-white/45 leading-[1.85] font-sans">
            AI-generated insights will be displayed here once recommendation services are enabled. The diagnosis was completed successfully.
          </p>
        )}
      </div>
    </article>
  );
}
