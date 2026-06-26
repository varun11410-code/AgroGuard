import api from './api';

export interface TreatmentPlan {
  tier: "budget" | "standard" | "premium";
  title: string;
  description: string;
  estimatedCost: string;
}

export interface HistoryScan {
  id: string;
  crop_name: string;
  image_url: string | null;
  predicted_disease: string;
  confidence_score: number;
  ai_summary?: string | null;
  treatment_plans?: TreatmentPlan[] | null;
  risk_level?: string | null;
  created_at: string;
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
    const formData = new FormData();
    formData.append("image", file);
    formData.append("crop", cropId);

    try {
      const response = await api.post('/scans', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      const responseData = response.data;
      console.log("API Response:", responseData);

      if (!responseData.success || !responseData.data) {
        throw new ScanUploadError(responseData.message || "Failed to retrieve prediction results.");
      }

      const backendData = responseData.data;
      const data: ScanResponse = {
        scanId: backendData.scan_id || `scan_${Date.now()}`,
        status: "completed",
        prediction: {
          disease: backendData.disease,
          confidence: backendData.confidence,
          crop: backendData.crop,
          pathogen: undefined,
          riskLevel: backendData.risk_level,
          aiSummary: backendData.ai_summary,
          treatmentPlans: backendData.treatment_plans || [],
          prediction_index: backendData.prediction_index !== undefined ? backendData.prediction_index : null,
          label: backendData.label !== undefined ? backendData.label : null,
          is_supported: backendData.is_supported !== undefined ? backendData.is_supported : true
        }
      };
      return data;
    } catch (error: any) {
      if (error instanceof ScanUploadError) {
        throw error;
      }
      if (error.response) {
        throw new ScanUploadError(
          error.response.data?.message || "Failed to upload scan.",
          error.response.status
        );
      }
      throw new ScanUploadError(
        error instanceof Error ? error.message : "A network error occurred while uploading."
      );
    }
  },

  async getHistory(): Promise<HistoryScan[]> {
    try {
      const response = await api.get('/scans');
      const responseData = response.data;

      if (!responseData.success) {
        throw new Error(responseData.message || "Failed to fetch scan history");
      }

      return responseData.data as HistoryScan[];
    } catch (error: any) {
      console.error("Error fetching scan history:", error);
      if (error.response) {
        throw new Error(error.response.data?.message || "Failed to fetch scan history");
      }
      throw error;
    }
  },

  async deleteScan(scanId: string): Promise<void> {
    try {
      const response = await api.delete(`/scans/${scanId}`);
      const responseData = response.data;

      if (!responseData.success) {
        throw new Error(responseData.message || "Failed to delete scan");
      }
    } catch (error: any) {
      console.error("Error deleting scan:", error);
      if (error.response) {
        throw new Error(error.response.data?.message || "Failed to delete scan.");
      }
      throw error;
    }
  }
};
