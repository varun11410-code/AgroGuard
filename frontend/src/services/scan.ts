export interface ScanResponse {
  scanId: string;
  status: string;
  prediction?: {
    disease: string;
    confidence: number;
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
    const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "";
    const endpoint = `${API_BASE_URL}/api/scans`;

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

      const data: ScanResponse = await response.json();
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
