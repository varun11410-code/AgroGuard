"""
AgroGuard Backend - AI Utilities

Shared helpers used across multiple AI provider implementations.
"""


def strip_markdown_json(raw: str) -> str:
    """
    Strips markdown code fences from a raw string that may wrap a JSON payload.

    Some AI providers return JSON enclosed in markdown fences such as::

        ```json
        {"key": "value"}
        ```

    or simply::

        ```
        {"key": "value"}
        ```

    This function removes those fences and returns the bare JSON string,
    ready for ``json.loads()``.

    Args:
        raw: The raw string response from an AI provider.

    Returns:
        The cleaned string with leading/trailing whitespace and markdown
        code fences removed.
    """
    cleaned = raw.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    return cleaned.strip()
