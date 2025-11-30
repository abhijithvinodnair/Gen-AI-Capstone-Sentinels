#Internal tools for accessing company policies (The "Analyst" Toolkit).

from typing import Dict
from google.adk.tools import ToolContext

# Simulated internal policy database
# In production, this would connect to a vector database or document store
INTERNAL_POLICIES = {
    "data_retention": "All customer data must be retained for 5 years. Deletion requests processed in 30 days.",
    "access_control": "Multi-factor authentication is required for all production databases.",
    "encryption_standard": "All data at rest must be encrypted using AES-256."
}

def fetch_internal_policy(policy_id: str, context: ToolContext) -> Dict[str, str]:
    """
    Retrieves the full text of a specific internal company policy document.
    
    Args:
        policy_id: The unique identifier of the policy (e.g., 'data_retention').
        context: The ADK ToolContext object.
        
    Returns:
        A dictionary containing the 'status' and the 'policy_text' or an error message.
    """
    print(f" Accessing policy document: {policy_id}")
    
    policy_text = INTERNAL_POLICIES.get(policy_id.lower())
    
    if policy_text:
        return {
            "status": "success", 
            "policy_id": policy_id,
            "content": policy_text
        }
    else:
        return {
            "status": "error", 
            "message": f"Policy '{policy_id}' not found. Available: {list(INTERNAL_POLICIES.keys())}."
        }

def flag_compliance_risk(risk_level: str, description: str, context: ToolContext) -> Dict[str, str]:
    """
    Escalates a detected compliance violation for human review.
    
    Args:
        risk_level: 'LOW', 'MEDIUM', or 'CRITICAL'.
        description: A concise summary of the violation findings.
    """
    print(f" FLAGGING RISK: {risk_level} | {description}")
    return {"status": "escalated", "ticket_id": "INC-COMPLIANCE-001"}
