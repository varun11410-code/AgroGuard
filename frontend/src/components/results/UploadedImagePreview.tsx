"use client";

import { cn } from "@/lib/utils";
import Image from "next/image";

export interface UploadedImagePreviewProps {
  imageUrl?: string | null;
  disease?: string;
  className?: string;
}

export function UploadedImagePreview({
  imageUrl,
  disease,
  className,
}: UploadedImagePreviewProps) {
  return (
    <article
      aria-labelledby="preview-heading"
      className={cn(
        "glass-card p-8 transition-all duration-500 hover:-translate-y-1 hover:shadow-[0_20px_50px_rgba(34,197,94,0.05)] flex flex-col justify-between h-full min-h-[180px]",
        className
      )}
    >
      <div>
        <h3
          id="preview-heading"
          className="font-mono text-[0.7rem] uppercase tracking-[0.12em] text-white/35 mb-3"
        >
          Uploaded Image
        </h3>

        {!imageUrl ? (
          <div
            className="text-white/60 font-mono text-[0.9rem] mt-2"
            aria-label="Uploaded image preview unavailable"
          >
            Uploaded image preview unavailable.
          </div>
        ) : (
          <div className="relative w-full aspect-[4/3] rounded-lg overflow-hidden border border-white/10 bg-black/40 shadow-inner mt-2">
            <Image
              src={imageUrl}
              alt={disease ? `Uploaded crop image for ${disease}` : "Uploaded crop image"}
              fill
              className="object-contain"
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            />
          </div>
        )}
      </div>
    </article>
  );
}
