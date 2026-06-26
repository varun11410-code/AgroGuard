"""
AgroGuard Backend - Diagnosis Prompts

Defines prompt generation functions for the disease diagnosis and 
enrichment workflow. Pure text generation only. No SDKs or network calls.
"""

def build_enrichment_prompt(crop: str, disease: str, confidence: float) -> str:
    """
    Constructs the prompt instructing the AI to generate a structured 
    agricultural diagnosis and treatment JSON.
    """
    return (
        f"You are an expert agricultural AI assistant. Provide a brief analysis for a {crop} plant "
        f"diagnosed with '{disease}' (Confidence: {confidence:.2f}).\n\n"
        "Return EXACTLY a JSON object with the following structure (do NOT include Markdown backticks like ```json):\n"
        "{\n"
        '  "ai_summary": "A 2-3 sentence explanation of the disease and its impact.",\n'
        '  "treatment_plans": [\n'
        '    {\n'
        '      "tier": "budget",\n'
        '      "title": "Low Cost Plan",\n'
        '      "description": "...",\n'
        '      "estimatedCost": "$..."\n'
        '    },\n'
        '    {\n'
        '      "tier": "standard",\n'
        '      "title": "Standard Plan",\n'
        '      "description": "...",\n'
        '      "estimatedCost": "$..."\n'
        '    },\n'
        '    {\n'
        '      "tier": "premium",\n'
        '      "title": "Premium Plan",\n'
        '      "description": "...",\n'
        '      "estimatedCost": "$..."\n'
        '    }\n'
        '  ]\n'
        "}"
    )
