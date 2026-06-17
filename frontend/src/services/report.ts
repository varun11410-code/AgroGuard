// Report service
import api from './api';

export interface ReportDataPayload {
  crop: string;
  disease: string;
  confidence: number;
  selected_plan: string | null;
  image_stream: string | null;
  ai_summary: string | null;
  treatment_recommendations: string[];
  prevention_suggestions: string[];
}

export const reportService = {
  /**
   * Generates and downloads a PDF report.
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
      // Axios error parsing for blob responses is tricky because the response is a blob
      // If it's an API error, we might need to read the blob to get the JSON message
      if (error.response && error.response.data instanceof Blob) {
        try {
          const text = await error.response.data.text();
          const json = JSON.parse(text);
          throw new Error(json.message || 'Failed to generate report');
        } catch (e) {
          throw new Error('Failed to generate report due to a server error');
        }
      }
      throw new Error('Network error or failed to generate report');
    }
  }
};
