"use client";

import { useState } from "react";
import { CropSelectionCards } from "@/components/upload/CropSelectionCards";
import { DragDropUploader } from "@/components/upload/DragDropUploader";
import { AnalysisLoading } from "@/components/upload/AnalysisLoading";

export default function CropSelectionPreviewPage() {
    const [isSimulating, setIsSimulating] = useState(false);

    return (
        <main className="min-h-screen flex flex-col items-center justify-center p-6 gap-8">
            <div className="w-full max-w-4xl grid grid-cols-1 md:grid-cols-2 gap-6">
                <CropSelectionCards />
                <DragDropUploader />
            </div>
            
            <div className="flex flex-col items-center gap-4 mt-8 w-full">
                <button 
                  onClick={() => setIsSimulating(!isSimulating)}
                  className="px-6 py-2 bg-green-600/20 text-green-400 border border-green-500/30 rounded-full font-bold hover:bg-green-600/30 transition-all text-sm"
                >
                  {isSimulating ? "Stop Loading Simulation" : "Start Loading Simulation"}
                </button>
                
                <AnalysisLoading isVisible={isSimulating} />
            </div>
        </main>
    );
}