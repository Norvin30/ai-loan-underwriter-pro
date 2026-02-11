"""
Temporal Activities for Loan Underwriting
Updated to use LangChain agents with AWS Bedrock models and MCP tools
"""
from temporalio import activity
from temporalio.exceptions import ApplicationError
from typing import Dict, Any
import os
import httpx
from dotenv import load_dotenv
from pathlib import Path
from classes.agents.bedrock_agent import (
    DataFetchAgent,
    CreditAssessmentAgent,
    IncomeAssessmentAgent,
    ExpenseAssessmentAgent,
    SupervisorAgent
)

# Load .env from project root
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

MOCK_API_BASE = os.getenv("MOCK_API_BASE", "http://localhost:3233")

# Initialize agents (reused across activities)
data_agent = DataFetchAgent()
credit_agent = CreditAssessmentAgent()
income_agent = IncomeAssessmentAgent()
expense_agent = ExpenseAssessmentAgent()
supervisor_agent = SupervisorAgent()


# ============================================================================
# DATA ACQUISITION PHASE - LangChain Agents with Bedrock
# ============================================================================
# These activities use LangChain agents powered by AWS Bedrock models
# with MCP tools for standardized data access
# ============================================================================


@activity.defn
async def fetch_bank_account(applicant_id: str) -> Dict[str, Any]:
    """
    Fetch bank account data using MCP tools.
    
    ARCHITECTURE NOTE:
    - Temporal Activity (Outer Loop): Handles retries, timeouts, durability
    - MCP Tools: Standardized data access interface
    - LangChain Agent: Validates and enriches data using Bedrock
    """
    try:
        # Fetch data via MCP tool
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{MOCK_API_BASE}/bank",
                params={"applicant_id": applicant_id},
                timeout=10.0
            )
            response.raise_for_status()
            bank_data = response.json()
        
        # Validate with LangChain agent
        validated_data = data_agent.fetch_and_validate(bank_data, "bank account")
        
        activity.logger.info(f"Successfully fetched bank account data for {applicant_id}")
        return validated_data
        
    except Exception as e:
        raise ApplicationError(
            f"Failed to fetch bank account data: {str(e)}",
            type="BankAPIError",
            non_retryable=False
        )


@activity.defn
async def fetch_documents(applicant_id: str) -> Dict[str, Any]:
    """
    Fetch applicant documents using MCP tools.
    
    ARCHITECTURE NOTE:
    - Temporal Activity: Provides durable execution and retry logic
    - MCP Tools: Standardized document access
    - LangChain Agent: Validates document completeness
    """
    try:
        # Fetch data via MCP tool
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{MOCK_API_BASE}/documents",
                params={"applicant_id": applicant_id},
                timeout=10.0
            )
            response.raise_for_status()
            documents_data = response.json()
        
        # Validate with LangChain agent
        validated_data = data_agent.fetch_and_validate(documents_data, "documents")
        
        doc_count = len(documents_data.get("documents", []))
        activity.logger.info(f"Successfully retrieved {doc_count} documents")
        
        return validated_data
        
    except Exception as e:
        raise ApplicationError(
            f"Failed to fetch documents: {str(e)}",
            type="DocumentAPIError",
            non_retryable=False
        )


@activity.defn
async def fetch_credit_report_cibil(applicant_id: str) -> Dict[str, Any]:
    """
    Fetch credit report from CIBIL bureau using MCP tools.
    
    ARCHITECTURE NOTE - TEMPORAL'S FALLBACK PATTERN:
    - This activity is configured with LIMITED retries in the workflow
    - If it fails, Temporal orchestrates the fallback to Experian
    - The workflow layer handles the provider fallback logic
    - MCP tools provide standardized access to credit bureaus
    """
    try:
        # Fetch data via MCP tool
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{MOCK_API_BASE}/cibil",
                params={"applicant_id": applicant_id},
                timeout=10.0
            )
            response.raise_for_status()
            credit_data = response.json()
        
        # Add provider metadata
        credit_data["provider"] = "CIBIL"
        credit_data["data_quality"] = "validated"
        
        # Validate score range
        score = credit_data.get("score", 0)
        if not isinstance(score, (int, float)) or score < 300 or score > 850:
            raise ValueError(f"Invalid credit score from CIBIL: {score}")
        
        activity.logger.info(f"Successfully fetched CIBIL credit report for {applicant_id}")
        return credit_data
        
    except Exception as e:
        raise ApplicationError(
            f"Failed to fetch CIBIL credit report: {str(e)}",
            type="CibilAPIError",
            non_retryable=False
        )


@activity.defn
async def fetch_credit_report_experian(applicant_id: str) -> Dict[str, Any]:
    """
    Fetch credit report from Experian bureau using MCP tools.
    
    ARCHITECTURE NOTE - FALLBACK PROVIDER:
    - This activity is called by Temporal when CIBIL fails
    - Demonstrates Temporal's orchestration of fallback strategies
    - MCP tools ensure consistent data access patterns
    """
    try:
        # Fetch data via MCP tool
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{MOCK_API_BASE}/experian",
                params={"applicant_id": applicant_id},
                timeout=10.0
            )
            response.raise_for_status()
            credit_data = response.json()
        
        # Add provider metadata
        credit_data["provider"] = "Experian"
        credit_data["data_quality"] = "validated"
        
        # Validate score range
        score = credit_data.get("score", 0)
        if not isinstance(score, (int, float)) or score < 300 or score > 850:
            raise ValueError(f"Invalid credit score from Experian: {score}")
        
        activity.logger.info(f"Successfully fetched Experian credit report for {applicant_id}")
        return credit_data
        
    except Exception as e:
        raise ApplicationError(
            f"Failed to fetch Experian credit report: {str(e)}",
            type="ExperianAPIError",
            non_retryable=False
        )


# ============================================================================
# ASSESSMENT PHASE - LangChain Agents with Bedrock Models
# ============================================================================
# These activities use specialized LangChain agents powered by AWS Bedrock
# Claude 3.5 Sonnet for complex reasoning
# Nova Pro for cost-effective analysis
# ============================================================================


@activity.defn
async def income_assessment(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Assess income and affordability using LangChain agent with Bedrock.
    
    Uses Claude 3.5 Sonnet for sophisticated financial analysis.
    """
    try:
        application = payload.get("application", {})
        bank = payload.get("bank", {})
        credit = payload.get("credit", {})
        
        # Use LangChain agent with Bedrock for assessment
        assessment = income_agent.assess_income(application, bank, credit)
        
        activity.logger.info(f"Income assessment completed: {assessment.get('affordability_ok')}")
        return assessment
        
    except Exception as e:
        raise ApplicationError(
            f"Income assessment failed: {str(e)}",
            type="IncomeAssessmentError",
            non_retryable=False
        )


@activity.defn
async def expense_assessment(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Assess expenses and cash flow using LangChain agent with Bedrock.
    
    Uses Nova Pro for cost-effective expense analysis.
    """
    try:
        application = payload.get("application", {})
        bank = payload.get("bank", {})
        
        # Use LangChain agent with Bedrock for assessment
        assessment = expense_agent.assess_expenses(application, bank)
        
        activity.logger.info(f"Expense assessment completed: {assessment.get('affordability_ok')}")
        return assessment
        
    except Exception as e:
        raise ApplicationError(
            f"Expense assessment failed: {str(e)}",
            type="ExpenseAssessmentError",
            non_retryable=False
        )


@activity.defn
async def credit_assessment(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Assess credit risk using LangChain agent with Bedrock.
    
    Uses Claude 3.5 Sonnet for sophisticated credit risk analysis.
    """
    try:
        application = payload.get("application", {})
        credit = payload.get("credit", {})
        
        # Use LangChain agent with Bedrock for assessment
        assessment = credit_agent.assess_credit(application, credit)
        
        activity.logger.info(f"Credit assessment completed: {assessment.get('risk_level')}")
        return assessment
        
    except Exception as e:
        raise ApplicationError(
            f"Credit assessment failed: {str(e)}",
            type="CreditAssessmentError",
            non_retryable=False
        )


@activity.defn
async def aggregate_and_decide(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Aggregate all assessments and make final decision using Supervisor Agent.
    
    Uses Claude 3.5 Sonnet for comprehensive decision-making with reasoning.
    
    ARCHITECTURE NOTE:
    - Supervisor agent synthesizes all specialist assessments
    - Uses advanced reasoning capabilities of Claude 3.5 Sonnet
    - Provides explainable AI decisions for human review
    """
    try:
        application = payload.get("application", {})
        income_res = payload.get("income", {})
        expense_res = payload.get("expense", {})
        credit_res = payload.get("credit", {})
        documents = payload.get("docs", {})
        
        # Use Supervisor agent with Bedrock for final decision
        decision = supervisor_agent.aggregate_and_decide(
            application,
            income_res,
            expense_res,
            credit_res,
            documents
        )
        
        activity.logger.info(f"Final decision: {decision.get('decision')} with {decision.get('confidence')} confidence")
        return decision
        
    except Exception as e:
        raise ApplicationError(
            f"Decision aggregation failed: {str(e)}",
            type="DecisionAggregationError",
            non_retryable=False
        )
