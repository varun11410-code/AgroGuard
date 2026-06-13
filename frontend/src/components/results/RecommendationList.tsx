import { cn } from "@/lib/utils";
import { TreatmentPlan } from "@/services/scan";

export interface RecommendationListProps {
  plans: TreatmentPlan[];
  className?: string;
}

export function RecommendationList({ plans, className }: RecommendationListProps) {
  if (!plans || plans.length === 0) return null;

  return (
    <div 
      className={cn("col-span-1 sm:col-span-2 lg:col-span-3 grid grid-cols-1 md:grid-cols-3 gap-4 mt-2", className)}
      role="list"
      aria-label="Treatment Recommendations"
    >
      {plans.map((plan, i) => {
        const isBudget = plan.tier === "budget";
        const isStandard = plan.tier === "standard";
        const isPremium = plan.tier === "premium";

        return (
          <div 
            key={i}
            role="listitem"
            className="p-7 rounded-[var(--radius-sm,0.25rem)] border border-white/[0.07] bg-white/[0.03] transition-all duration-300 hover:border-[#22c55e]/20 hover:-translate-y-1"
          >
            <div 
              className={cn(
                "inline-flex items-center gap-[6px] font-mono text-[0.68rem] tracking-[0.1em] uppercase px-[12px] py-[5px] rounded-full mb-4",
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
            
            <h3 className="font-heading text-[1rem] font-bold mb-[10px]">{plan.title}</h3>
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
          </div>
        );
      })}
    </div>
  );
}
