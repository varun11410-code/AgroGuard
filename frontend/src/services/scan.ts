export interface TreatmentPlan {
  tier: "budget" | "standard" | "premium";
  title: string;
  description: string;
  estimatedCost: string;
}

export interface HistoryScan {
  id: string;
  crop_name: string;
  predicted_disease: string;
  confidence_score: number;
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
    const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5001";
    const cleanBaseUrl = API_BASE_URL.replace(/\/$/, "");
    const endpoint = cleanBaseUrl.endsWith("/api")
      ? `${cleanBaseUrl}/scans`
      : `${cleanBaseUrl}/api/scans`;

    console.log("Upload endpoint:", endpoint);

    const formData = new FormData();
    formData.append("image", file);
    formData.append("crop", cropId);

    const headers: HeadersInit = {};
    const token = localStorage.getItem("auth_token");
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers,
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
  },

  async getHistory(): Promise<HistoryScan[]> {
    const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5001";
    const cleanBaseUrl = API_BASE_URL.replace(/\/$/, "");
    const endpoint = cleanBaseUrl.endsWith("/api")
      ? `${cleanBaseUrl}/scans`
      : `${cleanBaseUrl}/api/scans`;

    const token = localStorage.getItem("auth_token");
    if (!token) {
      return [];
    }

    try {
      const response = await fetch(endpoint, {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      });

      if (!response.ok) {
        throw new Error("Failed to fetch scan history");
      }

      const responseData = await response.json();
      if (!responseData.success) {
        throw new Error(responseData.message || "Failed to fetch scan history");
      }

      return responseData.data as HistoryScan[];
    } catch (error) {
      console.error("Error fetching scan history:", error);
      throw error;
    }
  },

  async deleteScan(scanId: string): Promise<void> {
    const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5001";
    const cleanBaseUrl = API_BASE_URL.replace(/\/$/, "");
    const endpoint = cleanBaseUrl.endsWith("/api")
      ? `${cleanBaseUrl}/scans/${scanId}`
      : `${cleanBaseUrl}/api/scans/${scanId}`;

    const token = localStorage.getItem("auth_token");
    if (!token) {
      throw new Error("Unauthorized");
    }

    try {
      const response = await fetch(endpoint, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      });

      if (!response.ok) {
        let errorMessage = "Failed to delete scan.";
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || errorMessage;
        } catch {
          errorMessage = response.statusText || errorMessage;
        }
        throw new Error(errorMessage);
      }

      const responseData = await response.json();
      if (!responseData.success) {
        throw new Error(responseData.message || "Failed to delete scan");
      }
    } catch (error) {
      console.error("Error deleting scan:", error);
      throw error;
    }
  }
};
