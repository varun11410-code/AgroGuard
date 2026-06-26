def calculate_risk(disease: str, confidence: float, is_supported: bool) -> str:
    """
    Calculates the risk level deterministically based on the disease, confidence, and supported status.
    This replaces the AI-generated risk level to prevent hallucinations and ensure consistency.

    Args:
        disease (str): The predicted disease name.
        confidence (float): The ML confidence score (0.0 to 1.0).
        is_supported (bool): Whether the prediction is supported.

    Returns:
        str: "Low", "Medium", "High", or "Unknown".
    """
    if not is_supported or disease.lower() == "unsupported":
        return "Unknown"

    if disease.lower() == "healthy":
        return "Low"

    # For supported diseases:
    if confidence >= 0.80:
        return "High"
    else:
        return "Medium"
