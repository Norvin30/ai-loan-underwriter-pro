"""
MCP Tools Integration for LangChain Agents
Provides LangChain-compatible tools that connect to the MCP server
"""
import json
import httpx
from typing import Dict, Any
from langchain.tools import Tool
import os
from dotenv import load_dotenv

load_dotenv()

MOCK_API_BASE = os.getenv("MOCK_API_BASE", "http://localhost:3233")


def fetch_credit_report_tool(applicant_id: str, provider: str = "cibil") -> str:
    """
    Fetch credit report from credit bureau.
    
    Args:
        applicant_id: Unique identifier for the applicant
        provider: Credit bureau provider (cibil or experian)
    
    Returns:
        JSON string with credit report data
    """
    try:
        response = httpx.get(
            f"{MOCK_API_BASE}/{provider}",
            params={"applicant_id": applicant_id},
            timeout=10.0
        )
        response.raise_for_status()
        data = response.json()
        data["provider"] = provider
        data["data_quality"] = "validated"
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "provider": provider})


def fetch_bank_account_tool(applicant_id: str) -> str:
    """
    Fetch bank account information.
    
    Args:
        applicant_id: Unique identifier for the applicant
    
    Returns:
        JSON string with bank account data
    """
    try:
        response = httpx.get(
            f"{MOCK_API_BASE}/bank",
            params={"applicant_id": applicant_id},
            timeout=10.0
        )
        response.raise_for_status()
        data = response.json()
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


def fetch_documents_tool(applicant_id: str) -> str:
    """
    Fetch document verification status.
    
    Args:
        applicant_id: Unique identifier for the applicant
    
    Returns:
        JSON string with document data
    """
    try:
        response = httpx.get(
            f"{MOCK_API_BASE}/documents",
            params={"applicant_id": applicant_id},
            timeout=10.0
        )
        response.raise_for_status()
        data = response.json()
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


def validate_credit_score_tool(score: float, minimum_required: float = 620) -> str:
    """
    Validate credit score against lending criteria.
    
    Args:
        score: Credit score to validate
        minimum_required: Minimum required score (default: 620)
    
    Returns:
        JSON string with validation result
    """
    is_valid = score >= minimum_required
    risk_level = "low" if score >= 750 else "medium" if score >= 650 else "high"
    
    result = {
        "score": score,
        "minimum_required": minimum_required,
        "is_valid": is_valid,
        "risk_level": risk_level,
        "recommendation": "approve" if is_valid else "reject"
    }
    
    return json.dumps(result, indent=2)


# Create LangChain Tool objects
credit_report_tool = Tool(
    name="fetch_credit_report",
    description="Fetch credit report from credit bureau (CIBIL or Experian). Input should be a JSON string with 'applicant_id' and 'provider' fields.",
    func=lambda x: fetch_credit_report_tool(**json.loads(x))
)

bank_account_tool = Tool(
    name="fetch_bank_account",
    description="Fetch bank account information for an applicant. Input should be a JSON string with 'applicant_id' field.",
    func=lambda x: fetch_bank_account_tool(**json.loads(x))
)

documents_tool = Tool(
    name="fetch_documents",
    description="Fetch document verification status for an applicant. Input should be a JSON string with 'applicant_id' field.",
    func=lambda x: fetch_documents_tool(**json.loads(x))
)

credit_validation_tool = Tool(
    name="validate_credit_score",
    description="Validate if a credit score meets lending criteria. Input should be a JSON string with 'score' and optional 'minimum_required' fields.",
    func=lambda x: validate_credit_score_tool(**json.loads(x))
)

# Export all tools as a list
MCP_TOOLS = [
    credit_report_tool,
    bank_account_tool,
    documents_tool,
    credit_validation_tool
]
