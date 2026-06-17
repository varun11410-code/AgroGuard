export interface TreatmentPlan {
  tier: "budget" | "standard" | "premium";
  title: string;
  description: string;
  estimatedCost: string;
}

export interface ScanResponse {
  scanId: string;
  status: string;
  prediction?: {
    disease: string;
    confidence: number;
    // The following fields are not strictly guaranteed by the core ML response
    // and may be populated downstream by reports or chat APIs.
    crop?: string;
    pathogen?: string;
    riskLevel?: "Low" | "Medium" | "High";
    aiSummary?: string;
    treatmentPlans?: TreatmentPlan[];
    prediction_index?: number | null;
    label?: string | null;
    is_supported?: boolean;
  };
}

export class ScanUploadError extends Error {
  constructor(message: string, public status?: number) {
    super(message);
    this.name = "ScanUploadError";
  }
}

export const scanService = {
  async uploadScan(file: File, cropId: string): Promise<ScanResponse> {
    const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5001";
    const cleanBaseUrl = API_BASE_URL.replace(/\/$/, "");
    const endpoint = cleanBaseUrl.endsWith("/api")
      ? `${cleanBaseUrl}/scans`
      : `${cleanBaseUrl}/api/scans`;

    console.log("Upload endpoint:", endpoint);

    const formData = new FormData();
    formData.append("image", file);
    formData.append("crop", cropId);

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        let errorMessage = "Failed to upload scan.";
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || errorMessage;
        } catch {
          errorMessage = response.statusText || errorMessage;
        }
        throw new ScanUploadError(errorMessage, response.status);
      }

      const responseData = await response.json();
      console.log("API Response:", responseData);

      if (!responseData.success || !responseData.data) {
        throw new ScanUploadError(responseData.message || "Failed to retrieve prediction results.");
      }

      const backendData = responseData.data;
      const data: ScanResponse = {
        scanId: `scan_${Date.now()}`,
        status: "completed",
        prediction: {
          disease: backendData.disease,
          confidence: backendData.confidence,
          crop: backendData.crop,
          pathogen: undefined,
          riskLevel: undefined,
          aiSummary: undefined,
          treatmentPlans: [],
          prediction_index: backendData.prediction_index !== undefined ? backendData.prediction_index : null,
          label: backendData.label !== undefined ? backendData.label : null,
          is_supported: backendData.is_supported !== undefined ? backendData.is_supported : true
        }
      };
      return data;
    } catch (error) {
      if (error instanceof ScanUploadError) {
        throw error;
      }
      throw new ScanUploadError(
        error instanceof Error ? error.message : "A network error occurred while uploading."
      );
    }
  }
};
