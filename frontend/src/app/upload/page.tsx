"use client";

import { useState } from "react";
import { CropSelectionCards } from "@/components/upload/CropSelectionCards";
import { DragDropUploader } from "@/components/upload/DragDropUploader";
import { AnalysisLoading } from "@/components/upload/AnalysisLoading";
import { PredictionResults } from "@/components/results/PredictionResults";
import { useScanUpload } from "@/hooks/useScanUpload";
import { cn } from "@/lib/utils";

export default function UploadWorkflowPage() {
  const [selectedCrop, setSelectedCrop] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const {
    isUploading,
    error,
    scanResult,
    executeUpload,
  } = useScanUpload();

  const prediction = scanResult;
  console.log("Page Prediction:", prediction);

  const handleAnalyze = () => {
    if (!selectedCrop || !selectedFile || isUploading) return;
    executeUpload(selectedFile, selectedCrop);
  };

  const isAnalyzeDisabled = !selectedCrop || !selectedFile || isUploading;

  return (
    <div className="min-h-screen pt-24 pb-20">
      <style>{`
        @keyframes btnShimmer {
          from { left: -60%; }
          to { left: 120%; }
        }
      `}</style>
      <div className="container mx-auto px-6">
        
        {/* Header Section */}
        <div className="flex flex-col items-center text-center mb-16 max-w-2xl mx-auto">
          <div className="inline-flex items-center gap-[8px] font-mono text-[0.8rem] tracking-[0.1em] uppercase px-[16px] py-[8px] rounded-full mb-[24px] bg-white/[0.03] border border-white/[0.08] text-white/70">
            AI Diagnosis Workflow
          </div>
          <h2 className="font-heading text-4xl md:text-5xl font-extrabold tracking-[-0.03em] mb-6">
            Scan your crop
          </h2>
          <p className="text-[1.1rem] md:text-[1.2rem] text-white/60 leading-[1.6]">
            Select your crop type and upload a clear photo of the infected leaf. Our ML models will analyze the pathogen signatures instantly.
          </p>
        </div>

        {/* Upload Workflow Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto mb-12">
          <div>
            <h3 className="font-mono text-[0.72rem] uppercase tracking-[0.12em] text-white/35 mb-[14px]">
              Step 1 — Select Crop
            </h3>
            <CropSelectionCards onSelect={setSelectedCrop} />
          </div>
          
          <div>
            <h3 className="font-mono text-[0.72rem] uppercase tracking-[0.12em] text-white/35 mb-[14px]">
              Step 2 — Upload Image
            </h3>
            <div className={cn(isUploading && "pointer-events-none opacity-60 transition-opacity")}>
              <DragDropUploader onFileSelect={setSelectedFile} />
            </div>
          </div>
        </div>

        {/* Global Error Message from Hook */}
        {error && (
          <div 
            className="max-w-md mx-auto mb-8 p-4 rounded-[var(--radius-sm,0.25rem)] border border-red-500/30 bg-red-500/10 text-red-400 text-sm text-center font-mono"
            aria-live="polite"
          >
            {error}
          </div>
        )}

        {/* Analyze Button and Loading Sequence */}
        {!scanResult && (
          <div className="mt-[24px] text-center">
            <button
              onClick={handleAnalyze}
              disabled={isAnalyzeDisabled}
              aria-disabled={isAnalyzeDisabled}
              className={cn(
                "font-heading px-[60px] py-[20px] text-[1.05rem] font-bold text-white rounded-full transition-all duration-300 relative overflow-hidden tracking-[0.01em]",
                "bg-gradient-to-br from-[#166534] to-[#22c55e]",
                "hover:-translate-y-1 hover:shadow-[0_20px_60px_rgba(34,197,94,0.55)]",
                "disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:hover:shadow-none disabled:shadow-none",
                !isAnalyzeDisabled && "shadow-[0_16px_50px_rgba(34,197,94,0.4),0_0_0_1px_rgba(34,197,94,0.2)]"
              )}
            >
              {!isAnalyzeDisabled && (
                <div className="absolute top-[-50%] left-[-60%] w-[40%] h-[200%] bg-gradient-to-r from-transparent via-white/20 to-transparent -skew-x-[20deg] animate-[btnShimmer_3s_linear_infinite]" />
              )}
              <span className="relative z-10">
                {isUploading ? "Analyzing..." : "⚡ Analyze with AI"}
              </span>
            </button>

            <AnalysisLoading isVisible={isUploading} className="mt-8" />
          </div>
        )}

        {/* Prediction Results */}
        {scanResult && (
           <div className="animate-in fade-in slide-in-from-bottom-8 duration-700 fill-mode-both">
             <div className="h-[1px] w-full bg-white/[0.05] my-16 max-w-5xl mx-auto" />
             <PredictionResults result={scanResult} />
             
             {/* Action to reset and do another scan */}
             <div className="text-center mt-12 pb-12">
               <button 
                 onClick={() => window.location.reload()}
                 className="text-white/50 hover:text-white transition-colors text-[0.85rem] font-mono"
               >
                 ← Run another scan
               </button>
             </div>
           </div>
        )}
      </div>
    </div>
  );
}
