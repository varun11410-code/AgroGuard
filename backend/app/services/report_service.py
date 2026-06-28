"""
AgroGuard Backend - Report Generation Service

Pure business logic service for generating PDF reports.
"""
import io
import logging

from app.reports.pdf_template import create_report_template
from app.schemas.report_contract import ReportData
from app.core.exceptions import ReportGenerationError

logger = logging.getLogger(__name__)

def generate_report(data: ReportData) -> io.BytesIO:
    """
    Transforms a fully-populated ReportData payload into a PDF buffer.
    
    This is a pure generation function. It does not perform database
    lookups or network I/O.
    
    Args:
        data (ReportData): The validated payload for the report.
        
    Returns:
        io.BytesIO: The in-memory buffer containing the compiled PDF bytes.
        
        Exception: If the underlying ReportLab generation fails.
    """
    buffer = io.BytesIO()
    
    try:
        # Create the template and get the layout story
        doc, story = create_report_template(buffer, data)
        
        # Compile the PDF into the buffer
        doc.build(story)
        
        # Reset the buffer pointer to the beginning for downstream readers
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        logger.error(f"Failed to generate PDF report: {str(e)}", exc_info=True)
        raise ReportGenerationError(f"Critical failure during PDF compilation: {str(e)}") from e
