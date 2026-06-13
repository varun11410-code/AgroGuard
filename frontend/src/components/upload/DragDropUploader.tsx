"use client";

import { useState, useRef, ChangeEvent, DragEvent, useEffect } from "react";
import Image from "next/image";
import { cn } from "@/lib/utils";

export interface DragDropUploaderProps {
  onFileSelect?: (file: File | null) => void;
  className?: string;
}

export function DragDropUploader({ onFileSelect, className }: DragDropUploaderProps) {
  const [dragOver, setDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Cleanup object URLs to avoid memory leaks
  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      processFile(file);
    }
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      processFile(file);
    }
  };

  const processFile = (file: File) => {
    if (!file.type.startsWith("image/")) {
      return; // Basic filtering for images only
    }
    
    // Revoke old URL if exists
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    
    setSelectedFile(file);
    const objectUrl = URL.createObjectURL(file);
    setPreviewUrl(objectUrl);
    if (onFileSelect) {
      onFileSelect(file);
    }
  };

  const handleRemove = (e?: React.MouseEvent | React.KeyboardEvent) => {
    if (e) {
      e.stopPropagation();
    }
    setSelectedFile(null);
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setPreviewUrl(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
    if (onFileSelect) {
      onFileSelect(null);
    }
  };

  const handleClick = () => {
    if (!selectedFile && fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      handleClick();
    }
  };

  // Base ghost button classes matching template.html `.btn-ghost`
  const btnGhostClass = "px-[26px] py-[12px] font-sans rounded-full text-[0.9rem] font-semibold transition-all duration-300 border border-white/15 bg-transparent text-white/80 hover:bg-white/[0.06] hover:border-white/25 hover:-translate-y-[3px] active:-translate-y-[1px]";

  return (
    <div className={cn("w-full", className)}>
      <div
        className={cn(
          "glass-card relative overflow-hidden p-[60px_40px] text-center border-2 border-dashed transition-all duration-300 outline-none focus-visible:ring-2 focus-visible:ring-primary/50",
          dragOver 
            ? "!border-[#22c55e]/40 !bg-[#22c55e]/[0.04]" 
            : selectedFile 
              ? "!border-[#22c55e]/20" 
              : "!border-white/10 hover:!border-[#22c55e]/40 hover:!bg-[#22c55e]/[0.04]",
          !selectedFile && "cursor-pointer"
        )}
        onClick={handleClick}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        role="button"
        tabIndex={0}
        onKeyDown={handleKeyDown}
        aria-label={selectedFile ? "Selected file preview area" : "Upload image area"}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept="image/*"
          className="hidden"
          aria-hidden="true"
          tabIndex={-1}
        />

        {!selectedFile ? (
          <div className="flex flex-col items-center pointer-events-none">
            <span className="text-[64px] mb-[20px] block opacity-60 leading-none" aria-hidden="true">📷</span>
            <h3 className="font-heading text-[1.2rem] font-bold mb-[10px] text-foreground">
              Drag & Drop your image
            </h3>
            <p className="text-[0.85rem] text-white/40 mb-[24px] font-sans">
              JPG, PNG, WEBP · Max 10MB
            </p>
            <button
              type="button"
              className={cn(btnGhostClass, "relative z-10 pointer-events-auto")}
              onClick={(e) => {
                e.stopPropagation();
                fileInputRef.current?.click();
              }}
              tabIndex={-1} // The outer div handles keyboard focus to simplify a11y
            >
              Browse Files
            </button>
          </div>
        ) : (
          <div className="flex flex-col items-center">
            <div className="relative w-full max-w-[320px] aspect-[4/3] rounded-lg overflow-hidden border border-white/10 mb-5 bg-black/40 shadow-xl pointer-events-none">
              {previewUrl && (
                <Image
                  src={previewUrl}
                  alt="Selected crop image preview"
                  fill
                  className="object-contain"
                />
              )}
            </div>
            <div className="flex flex-col items-center gap-4">
              <span className="font-mono text-[0.85rem] text-[#22c55e] truncate max-w-[300px] px-4 py-1.5 rounded-full bg-[#22c55e]/10 border border-[#22c55e]/20">
                {selectedFile.name}
              </span>
              <div className="flex flex-wrap justify-center gap-3 mt-1 z-10 relative">
                <button
                  type="button"
                  className={cn(btnGhostClass, "px-5 py-2 text-[0.8rem]")}
                  onClick={(e) => {
                    e.stopPropagation();
                    fileInputRef.current?.click();
                  }}
                  aria-label="Replace selected image"
                >
                  Replace
                </button>
                <button
                  type="button"
                  className={cn(
                    btnGhostClass, 
                    "px-5 py-2 text-[0.8rem] !border-red-500/30 !bg-red-500/10 !text-red-400 hover:!bg-red-500/20"
                  )}
                  onClick={handleRemove}
                  aria-label="Remove selected image"
                >
                  Remove
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
