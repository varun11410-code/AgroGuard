// Report service
import api from './api';
import { TreatmentPlan } from './scan';

export interface ReportDataPayload {
  scan_id?: string | null;
  crop: string;
  disease: string;
  confidence: number;
  selected_plan: string | null;
  image_stream: string | null;
  ai_summary: string | null;
  risk_level: string | null;
  treatment_plans: TreatmentPlan[];
  treatment_recommendations: string[];
  prevention_suggestions: string[];
}

/**
 * Shared payload builder to ensure active generation and historical generation use the exact same schema.
 */
export const buildReportPayload = (
  data: {
    scan_id?: string | null;
    crop_name: string;
    predicted_disease?: string | null;
    confidence_score?: number | null;
    selected_plan?: string | null;
    image_url?: string | null;
    ai_summary?: string | null;
    risk_level?: string | null;
    treatment_plans?: TreatmentPlan[] | null;
  }
): ReportDataPayload => {
  return {
    scan_id: data.scan_id || null,
    crop: data.crop_name || "Unknown Crop",
    disease: data.predicted_disease || "Unknown Disease",
    confidence: data.confidence_score || 0.0,
    selected_plan: data.selected_plan || null,
    image_stream: data.image_url || null,
    ai_summary: data.ai_summary || null,
    risk_level: data.risk_level || null,
    treatment_plans: data.treatment_plans || [],
    treatment_recommendations: [],
    prevention_suggestions: []
  };
};

export interface ReportMetadata {
  id: string;
  scan_id: string;
  report_version: string;
  generated_at: string;
  scan: {
    crop_name: string;
    predicted_disease: string;
    confidence_score: number;
  };
}

export const reportService = {
  /**
   * Generates and downloads a new PDF report.
   * @param data The exactly formatted ReportData payload
   */
  downloadReport: async (data: ReportDataPayload): Promise<void> => {
    try {
      const response = await api.post('/reports/generate', data, {
        responseType: 'blob',
      });

      // Extract filename from Content-Disposition header if possible
      let filename = 'AgroGuard_Report.pdf';
      const disposition = response.headers['content-disposition'];
      
      if (disposition && disposition.indexOf('filename=') !== -1) {
        const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
        const matches = filenameRegex.exec(disposition);
        if (matches != null && matches[1]) {
          filename = matches[1].replace(/['"]/g, '');
        }
      }

      // Create blob URL and trigger download
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = URL.createObjectURL(blob);
      
      const anchor = document.createElement('a');
      anchor.href = url;
      anchor.download = filename;
      document.body.appendChild(anchor);
      anchor.click();
      document.body.removeChild(anchor);
      
      // Cleanup object URL
      setTimeout(() => {
        URL.revokeObjectURL(url);
      }, 100);

    } catch (error: any) {
      if (error.response && error.response.data instanceof Blob) {
        try {
          const text = await error.response.data.text();
          const json = JSON.parse(text);
          throw new Error(json.message || 'Failed to generate report');
        } catch {
          throw new Error('Failed to generate report due to a server error');
        }
      }
      throw new Error('Network error or failed to generate report');
    }
  },

  /**
   * Retrieves the authenticated user's explicitly generated reports.
   */
  getHistory: async (): Promise<ReportMetadata[]> => {
    try {
      const response = await api.get('/reports');
      if (response.data.success) {
        return response.data.data;
      }
      throw new Error(response.data.message || 'Failed to fetch report history');
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Network error fetching report history');
    }
  },

  /**
   * Reconstructs and downloads a historical report.
   */
  downloadHistoricalReport: async (report_id: string): Promise<void> => {
    try {
      const response = await api.get(`/reports/${report_id}/download`, {
        responseType: 'blob',
      });

      let filename = `AgroGuard_Historical_Report_${report_id.substring(0, 8)}.pdf`;
      const disposition = response.headers['content-disposition'];
      
      if (disposition && disposition.indexOf('filename=') !== -1) {
        const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
        const matches = filenameRegex.exec(disposition);
        if (matches != null && matches[1]) {
          filename = matches[1].replace(/['"]/g, '');
        }
      }

      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = URL.createObjectURL(blob);
      
      const anchor = document.createElement('a');
      anchor.href = url;
      anchor.download = filename;
      document.body.appendChild(anchor);
      anchor.click();
      document.body.removeChild(anchor);
      
      setTimeout(() => {
        URL.revokeObjectURL(url);
      }, 100);

    } catch (error: any) {
      if (error.response && error.response.data instanceof Blob) {
        try {
          const text = await error.response.data.text();
          const json = JSON.parse(text);
          throw new Error(json.message || 'Failed to download report');
        } catch {
          throw new Error('Failed to download report due to a server error');
        }
      }
      throw new Error('Network error or failed to download report');
    }
  }
};
