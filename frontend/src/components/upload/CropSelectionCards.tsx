"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";

export interface Crop {
  id: string;
  name: string;
  emoji: string;
  description: string;
  isV1Supported: boolean;
}

const CROPS: Crop[] = [
  {
    id: "tomato",
    name: "Tomato",
    emoji: "🍅",
    description: "Detects 3 disease classes",
    isV1Supported: true,
  },
  {
    id: "potato",
    name: "Potato",
    emoji: "🥔",
    description: "Detects Healthy Potato",
    isV1Supported: true,
  }
];

export interface CropSelectionCardsProps {
  onSelect?: (cropId: string) => void;
  selectedCropId?: string;
  className?: string;
}

export function CropSelectionCards({ onSelect, selectedCropId, className }: CropSelectionCardsProps) {
  const [internalSelected, setInternalSelected] = useState<string | null>(null);

  const selectedId = selectedCropId !== undefined ? selectedCropId : internalSelected;

  const handleSelect = (id: string) => {
    setInternalSelected(id);
    if (onSelect) {
      onSelect(id);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent, id: string) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      handleSelect(id);
    }
  };

  return (
    <div
      className={cn("flex flex-col gap-[14px]", className)}
      role="radiogroup"
      aria-label="Select a crop"
    >
      {CROPS.map((crop) => {
        const isActive = selectedId === crop.id;

        return (
          <div
            key={crop.id}
            onClick={() => handleSelect(crop.id)}
            onKeyDown={(e) => handleKeyDown(e, crop.id)}
            role="radio"
            aria-checked={isActive}
            tabIndex={0}
            className={cn(
              "glass-card p-[24px] flex items-center gap-[16px] cursor-pointer transition-all duration-300 outline-none focus-visible:ring-2 focus-visible:ring-primary/50",
              "border !border-white/5 hover:!border-[#22c55e]/20",
              isActive && "!border-[#22c55e]/40 !bg-[#22c55e]/5"
            )}
          >
            <div className="text-[2.5rem] leading-none" aria-hidden="true">{crop.emoji}</div>

            <div className="flex flex-col flex-1">
              <h4 className="font-heading font-bold mb-1 text-foreground text-base sm:text-lg">{crop.name}</h4>
              <div className="flex flex-wrap items-center gap-3">
                <p className="text-[0.82rem] text-white/40 font-sans m-0">{crop.description}</p>
                {crop.isV1Supported && (
                  <span className="inline-flex items-center gap-1.5 px-[10px] py-[4px] rounded-full text-[0.65rem] sm:text-[0.75rem] font-mono bg-[#22c55e]/10 border border-[#22c55e]/20 text-[#22c55e]">
                    Supported in V1
                  </span>
                )}
              </div>
            </div>

            <div
              className={cn(
                "ml-auto w-[22px] h-[22px] rounded-full border-2 flex items-center justify-center text-[0.7rem] shrink-0 transition-all duration-300",
                isActive
                  ? "bg-[#22c55e] border-[#22c55e] shadow-[0_0_12px_rgba(34,197,94,0.5)] text-white"
                  : "border-white/20 text-transparent"
              )}
              aria-hidden="true"
            >
              ✓
            </div>
          </div>
        );
      })}
    </div>
  );
}
