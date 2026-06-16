import { useState } from "react";
import { scanService, ScanResponse, ScanUploadError } from "@/services/scan";
import { validateImageFile } from "@/lib/validators/uploadValidation";

export interface UseScanUploadResult {
  isUploading: boolean;
  error: string | null;
  scanResult: ScanResponse | null;
  executeUpload: (file: File | null, cropId: string | null | undefined) => Promise<void>;
  reset: () => void;
}

export function useScanUpload(): UseScanUploadResult {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [scanResult, setScanResult] = useState<ScanResponse | null>(null);

  const reset = () => {
    setIsUploading(false);
    setError(null);
    setScanResult(null);
  };

  const executeUpload = async (file: File | null, cropId: string | null | undefined) => {
    reset();

    if (!cropId) {
      setError("Please select a crop before uploading.");
      return;
    }

    if (!file) {
      setError("Please select an image file to upload.");
      return;
    }

    const validation = validateImageFile(file);
    if (!validation.isValid) {
      setError(validation.errors[0] || "Invalid file.");
      return;
    }

    setIsUploading(true);
    try {
      const result = await scanService.uploadScan(file, cropId);
      console.log("Hook Result:", result);
      setScanResult(result);
    } catch (err) {
      if (err instanceof ScanUploadError) {
        setError(err.message);
      } else {
        setError("An unexpected error occurred during upload.");
      }
    } finally {
      setIsUploading(false);
    }
  };

  return {
    isUploading,
    error,
    scanResult,
    executeUpload,
    reset,
  };
}
