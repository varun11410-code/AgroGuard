import logging
from typing import Dict, Any
from flask import current_app

from app.ai.provider_factory import AIProviderFactory
from app.ai.prompts.diagnosis_prompt import build_enrichment_prompt
from app.ai.exceptions import AIProviderError

logger = logging.getLogger(__name__)

class AIEnrichmentService:
    @staticmethod
    def enrich_prediction(crop: str, disease: str, confidence: float) -> Dict[str, Any]:
        """
        Calls the active AI provider to generate AI summary, treatment plans, and risk level.
        Returns a dictionary with 'ai_summary', 'treatment_plans', and 'risk_level'.
        Falls back to default values if the provider fails (e.g., rate limits) or validates poorly.
        """
        prompt = build_enrichment_prompt(crop, disease, confidence)

        try:
            # 1. Resolve Provider
            provider = AIProviderFactory.get_provider(current_app.config)
            
            # 2. Execute Transport (Guarantees Dictionary Output)
            data = provider.generate_structured_json(prompt)
            
            # 3. Business Logic Validation
            # Ensure required keys exist and contain non-empty, valid values.
            if not data.get("ai_summary") or not isinstance(data.get("ai_summary"), str):
                raise AIProviderError("Missing or invalid 'ai_summary' in provider response.", error_code="AI_MISSING_SUMMARY")
                
            treatment_plans = data.get("treatment_plans")
            if not treatment_plans or not isinstance(treatment_plans, list) or len(treatment_plans) == 0:
                raise AIProviderError("Missing or invalid 'treatment_plans' in provider response.", error_code="AI_MISSING_TREATMENT_PLANS")
                
            return {
                "ai_summary": data["ai_summary"],
                "treatment_plans": data["treatment_plans"]
            }
            
        except (AIProviderError, ValueError, Exception) as e:
            logger.error(f"AI Enrichment failed (fallback applied): {str(e)}")
            return AIEnrichmentService.get_fallback_enrichment(crop, disease)

    @staticmethod
    def get_fallback_enrichment(crop: str, disease: str) -> Dict[str, Any]:
        """
        Provides fallback data when the AI provider is unavailable or exhausted.
        """
        is_healthy = disease.lower() == "healthy"
        
        if is_healthy:
            return {
                "ai_summary": f"Your {crop} appears to be completely healthy based on the visual analysis.",
                "treatment_plans": [
                    {
                        "tier": "budget",
                        "title": "Basic Maintenance",
                        "description": "Continue regular watering and observe plant health.",
                        "estimatedCost": "$0"
                    },
                    {
                        "tier": "standard",
                        "title": "Standard Care",
                        "description": "Apply standard seasonal fertilizer.",
                        "estimatedCost": "$10"
                    },
                    {
                        "tier": "premium",
                        "title": "Preventative Care",
                        "description": "Implement an organic protective spray schedule to prevent future diseases.",
                        "estimatedCost": "$25"
                    }
                ]
            }
        else:
            return {
                "ai_summary": f"Your {crop} shows signs of {disease}. Immediate action is recommended to prevent spreading.",
                "treatment_plans": [
                    {
                        "tier": "budget",
                        "title": "Immediate Pruning",
                        "description": "Remove affected leaves manually and improve air circulation.",
                        "estimatedCost": "$0"
                    },
                    {
                        "tier": "standard",
                        "title": "Chemical Fungicide",
                        "description": "Apply a targeted commercial fungicide according to label directions.",
                        "estimatedCost": "$15"
                    },
                    {
                        "tier": "premium",
                        "title": "Comprehensive Treatment",
                        "description": "Combine organic fungicides, soil amendments, and professional consultation.",
                        "estimatedCost": "$50"
                    }
                ]
            }
