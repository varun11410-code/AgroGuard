"""
AgroGuard Backend - PDF Template Definition

Defines the report layout and styling using ReportLab.
"""
import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle

from app.schemas.report_contract import ReportData

def get_report_styles():
    """Defines the styling configurations for the report."""
    styles = getSampleStyleSheet()
    
    # Custom Styles
    styles.add(ParagraphStyle(
        name='ReportTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor("#166534"), # AgroGuard Green
        spaceAfter=20,
        alignment=1 # Center
    ))
    
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor("#0f2414"),
        spaceBefore=15,
        spaceAfter=10,
        borderPadding=5,
        borderWidth=1,
        borderColor=colors.HexColor("#22C55E"),
        borderRadius=5
    ))
    
    styles.add(ParagraphStyle(
        name='AgroGuardBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=10,
        leading=14
    ))
    
    styles.add(ParagraphStyle(
        name='PlaceholderText',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.gray,
        fontName='Helvetica-Oblique',
        spaceAfter=10
    ))
    
    return styles

def build_report_story(data: ReportData) -> list:
    """
    Constructs the ReportLab Story (list of flowables) based on ReportData.
    """
    styles = get_report_styles()
    story = []
    
    # Header
    story.append(Paragraph("AgroGuard Diagnostic Report", styles['ReportTitle']))
    story.append(Paragraph(f"Generated at: {data.generated_at.strftime('%Y-%m-%d %H:%M:%S UTC')}", styles['AgroGuardBody']))
    story.append(Spacer(1, 20))
    
    # Diagnosis Section
    story.append(Paragraph("1. Diagnosis Information", styles['SectionHeader']))
    
    diagnosis_data = [
        ["Crop:", data.crop],
        ["Predicted Disease:", data.disease],
        ["Confidence Score:", f"{data.confidence * 100:.2f}%"]
    ]
    
    if data.selected_plan:
        diagnosis_data.append(["Selected Plan:", data.selected_plan])
        
    t = Table(diagnosis_data, colWidths=[150, 300])
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    
    # Image Section
    story.append(Paragraph("2. Scanned Image", styles['SectionHeader']))
    if data.image_stream:
        # Check if it's a file path string and exists, or if it's a file-like object
        if (isinstance(data.image_stream, str) and os.path.exists(data.image_stream)) or isinstance(data.image_stream, io.BytesIO):
            story.append(Image(data.image_stream, width=250, height=250, kind='proportional'))
        else:
            story.append(Paragraph("Image stream invalid.", styles['PlaceholderText']))
    else:
        story.append(Paragraph("No image provided.", styles['PlaceholderText']))
    story.append(Spacer(1, 20))
    
    # AI Summary Section
    story.append(Paragraph("3. AI Diagnostic Summary", styles['SectionHeader']))
    if data.ai_summary:
        story.append(Paragraph(data.ai_summary, styles['AgroGuardBody']))
    else:
        story.append(Paragraph("Available after AI enrichment (Phase 9).", styles['PlaceholderText']))
    story.append(Spacer(1, 20))
    
    # Treatment Recommendations Section
    story.append(Paragraph("4. Treatment Recommendations", styles['SectionHeader']))
    if data.treatment_recommendations:
        for rec in data.treatment_recommendations:
            story.append(Paragraph(f"• {rec}", styles['AgroGuardBody']))
    else:
        story.append(Paragraph("Available after AI enrichment (Phase 9).", styles['PlaceholderText']))
    story.append(Spacer(1, 20))
        
    # Prevention Suggestions Section
    story.append(Paragraph("5. Prevention Suggestions", styles['SectionHeader']))
    if data.prevention_suggestions:
        for prev in data.prevention_suggestions:
            story.append(Paragraph(f"• {prev}", styles['AgroGuardBody']))
    else:
        story.append(Paragraph("Available after AI enrichment (Phase 9).", styles['PlaceholderText']))
        
    return story

def create_report_template(buffer, data: ReportData):
    """
    Returns an unbuilt SimpleDocTemplate and the Story.
    The caller (Task 8.2 service) must execute doc.build(story).
    
    Args:
        buffer: A file-like object or path string where the PDF should be written.
        data: ReportData instance.
        
    Returns:
        tuple: (SimpleDocTemplate, list of flowables)
    """
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    story = build_report_story(data)
    
    return doc, story
