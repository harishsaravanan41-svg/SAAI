import re
from typing import Dict, Any, Optional
from backend.database.models import User

def validate_and_sanitize_response(
    response_text: str,
    tool_executed: Optional[str],
    tool_result: Optional[Dict[str, Any]],
    current_user: User
) -> str:
    """
    Validates model output to ensure privacy compliance and prevent hallucination during empty returns.
    """
    if not response_text:
        return "I'm sorry, I couldn't generate a response. Please try asking again."

    # Guardrail: Prevent leaking other registration numbers (except current user's)
    matches = re.findall(r"\b2223\d{5}\b", response_text)
    user_reg_str = str(current_user.register_number) if current_user.register_number else ""

    for match in matches:
        if match != user_reg_str:
            response_text = response_text.replace(match, "[REDACTED_REG_NO]")

    return response_text.strip()
