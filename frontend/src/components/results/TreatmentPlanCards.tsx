"use client";

import { cn } from "@/lib/utils";
import { TreatmentPlan } from "@/services/scan";

export type PlanTier = "budget" | "standard" | "premium";

export interface TreatmentPlanCardsProps {
  plans?: TreatmentPlan[];
  className?: string;
  selectedPlan?: PlanTier | null;
  onPlanSelect?: (plan: PlanTier) => void;
}

export function TreatmentPlanCards({
  plans,
  className,
  selectedPlan,
  onPlanSelect,
}: TreatmentPlanCardsProps) {
  const hasLivePlans = plans && plans.length > 0;

  const handleKeyDown = (e: React.KeyboardEvent, tier: PlanTier) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      onPlanSelect?.(tier);
    }
  };

  // Render Live Plans Mode
  if (hasLivePlans) {
    return (
      <div
        className={cn(
          "col-span-1 sm:col-span-2 lg:col-span-3 grid grid-cols-1 md:grid-cols-3 gap-4 mt-2",
          className
        )}
        role="radiogroup"
        aria-label="Select a treatment plan"
      >
        {plans.map((plan, i) => {
          const isBudget = plan.tier === "budget";
          const isStandard = plan.tier === "standard";
          const isPremium = plan.tier === "premium";
          const isSelected = selectedPlan === plan.tier;

          return (
            <article
              key={i}
              role="radio"
              aria-checked={isSelected}
              tabIndex={0}
              onClick={() => onPlanSelect?.(plan.tier)}
              onKeyDown={(e) => handleKeyDown(e, plan.tier)}
              className={cn(
                "p-7 rounded-[var(--radius-sm,12px)] border transition-all duration-300 hover:-translate-y-1 focus-visible:ring-2 focus-visible:ring-[#22c55e]/50 outline-none cursor-pointer",
                isSelected
                  ? "border-[#22c55e]/40 bg-[#22c55e]/5 hover:border-[#22c55e]/50"
                  : "border-white/[0.07] bg-white/[0.03] hover:border-[#22c55e]/20"
              )}
            >
              <div className="flex items-center justify-between mb-4">
                <div
                  className={cn(
                    "inline-flex items-center gap-[6px] font-mono text-[0.68rem] tracking-[0.1em] uppercase px-[12px] py-[5px] rounded-full",
                    isBudget && "bg-[#22c55e]/[0.08] text-[#86efac] border border-[#22c55e]/15",
                    isStandard && "bg-blue-500/[0.08] text-blue-300 border border-blue-500/15",
                    isPremium && "bg-purple-500/[0.08] text-purple-300 border border-purple-500/15"
                  )}
                >
                  <span aria-hidden="true">
                    {isBudget && "💰"}
                    {isStandard && "🌿"}
                    {isPremium && "⭐"}
                  </span>
                  <span>
                    {isBudget && "Budget Plan"}
                    {isStandard && "Standard Plan"}
                    {isPremium && "Premium Plan"}
                  </span>
                </div>

                <div
                  className={cn(
                    "w-[22px] h-[22px] rounded-full border-2 flex items-center justify-center text-[0.7rem] shrink-0 transition-all duration-300",
                    isSelected
                      ? "bg-[#22c55e] border-[#22c55e] shadow-[0_0_12px_rgba(34,197,94,0.5)] text-white"
                      : "border-white/20 text-transparent"
                  )}
                  aria-hidden="true"
                >
                  ✓
                </div>
              </div>

              <h4 id={`plan-heading-${plan.tier}`} className="font-heading text-[1.1rem] font-bold mb-[10px] text-white">
                {plan.title}
              </h4>
              <p className="text-[0.85rem] text-white/45 leading-[1.7]">{plan.description}</p>

              <div
                className={cn(
                  "mt-[14px] font-mono text-[0.78rem]",
                  isBudget && "text-[#22c55e]/60",
                  isStandard && "text-blue-300/60",
                  isPremium && "text-purple-300/60"
                )}
              >
                {plan.estimatedCost}
              </div>
            </article>
          );
        })}
      </div>
    );
  }

  // Render Placeholder Mode
  const placeholderTiers = [
    {
      tier: "budget" as PlanTier,
      emoji: "💰",
      label: "Budget Plan",
      title: "Budget",
      badgeStyle: "bg-[#22c55e]/[0.08] text-[#86efac] border border-[#22c55e]/15",
    },
    {
      tier: "standard" as PlanTier,
      emoji: "🌿",
      label: "Standard Plan",
      title: "Standard",
      badgeStyle: "bg-blue-500/[0.08] text-blue-300 border border-blue-500/15",
    },
    {
      tier: "premium" as PlanTier,
      emoji: "⭐",
      label: "Premium Plan",
      title: "Premium",
      badgeStyle: "bg-purple-500/[0.08] text-purple-300 border border-purple-500/15",
    },
  ];

  return (
    <div
      className={cn(
        "col-span-1 sm:col-span-2 lg:col-span-3 grid grid-cols-1 md:grid-cols-3 gap-4 mt-2",
        className
      )}
      role="radiogroup"
      aria-label="Select a treatment plan (AI Pending)"
    >
      {placeholderTiers.map((tierInfo) => {
        const isSelected = selectedPlan === tierInfo.tier;

        return (
          <article
            key={tierInfo.tier}
            role="radio"
            aria-checked={isSelected}
            tabIndex={0}
            onClick={() => onPlanSelect?.(tierInfo.tier)}
            onKeyDown={(e) => handleKeyDown(e, tierInfo.tier)}
            className={cn(
              "p-7 rounded-[var(--radius-sm,12px)] border transition-all duration-300 hover:-translate-y-1 focus-visible:ring-2 focus-visible:ring-[#22c55e]/50 outline-none cursor-pointer",
              isSelected
                ? "border-[#22c55e]/40 bg-[#22c55e]/5 hover:border-[#22c55e]/50"
                : "border-white/[0.07] bg-white/[0.03] hover:border-[#22c55e]/20"
            )}
          >
            <div className="flex items-center justify-between mb-4">
              <div
                className={cn(
                  "inline-flex items-center gap-[6px] font-mono text-[0.68rem] tracking-[0.1em] uppercase px-[12px] py-[5px] rounded-full",
                  tierInfo.badgeStyle
                )}
              >
                <span aria-hidden="true">{tierInfo.emoji}</span>
                <span>{tierInfo.label}</span>
              </div>

              <div
                className={cn(
                  "w-[22px] h-[22px] rounded-full border-2 flex items-center justify-center text-[0.7rem] shrink-0 transition-all duration-300",
                  isSelected
                    ? "bg-[#22c55e] border-[#22c55e] shadow-[0_0_12px_rgba(34,197,94,0.5)] text-white"
                    : "border-white/20 text-transparent"
                )}
                aria-hidden="true"
              >
                ✓
              </div>
            </div>

            <h4 id={`plan-heading-${tierInfo.tier}`} className="font-heading text-[1.1rem] font-bold mb-[10px] text-white">
              {tierInfo.title}
            </h4>
            <p className="text-[0.85rem] text-white/45 leading-[1.7] font-sans">
              Treatment recommendations for this plan tier will become available once AI recommendation services are enabled. The diagnosis was completed successfully.
            </p>
          </article>
        );
      })}
    </div>
  );
}
