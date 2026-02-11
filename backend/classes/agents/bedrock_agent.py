"""
Simplified Bedrock Agent - Direct LLM calls without complex LangChain agents
Works with any LangChain version
"""
import os
import json
from typing import Any, Dict, List, Optional
from langchain_aws import ChatBedrock
import boto3
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root (3 levels up from this file)
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Debug: Print AWS credential status (masked)
aws_key = os.getenv("AWS_ACCESS_KEY_ID", "")
aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY", "")
aws_region = os.getenv("AWS_REGION", "us-east-1")
print(f"[BEDROCK AGENT] AWS Credentials Status:")
print(f"  - Access Key: {'✓ Found (' + aws_key[:8] + '...)' if aws_key else '✗ NOT FOUND'}")
print(f"  - Secret Key: {'✓ Found (' + ('*' * 20) + ')' if aws_secret else '✗ NOT FOUND'}")
print(f"  - Region: {aws_region}")


class BedrockAgentBase:
    """Base class for Bedrock-powered LangChain agents."""
    
    def __init__(
        self,
        model_id: Optional[str] = None,
        system_prompt: Optional[str] = None,
        tools: Optional[List] = None,
        temperature: float = 0.1
    ):
        """
        Initialize Bedrock agent with LangChain.
        
        Args:
            model_id: Bedrock model ID (defaults to Claude 3.5 Sonnet)
            system_prompt: System instructions for the agent
            tools: List of LangChain tools the agent can use
            temperature: Model temperature (0-1)
        """
        self.model_id = model_id or os.getenv(
            "BEDROCK_MODEL_CLAUDE",
            "amazon.titan-text-premier-v1:0"
        )
        self.region = os.getenv("AWS_REGION", "us-east-1")
        
        # Get AWS credentials explicitly
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        
        # Initialize Bedrock client with explicit credentials
        self.bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name=self.region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        
        print(f"[BEDROCK AGENT] Initialized with model: {self.model_id}, region: {self.region}")
        
        # Initialize ChatBedrock
        self.llm = ChatBedrock(
            client=self.bedrock_client,
            model_id=self.model_id,
            model_kwargs={
                "temperature": temperature,
                "max_tokens": 4096
            }
        )
        
        self.system_prompt = system_prompt or "You are a helpful AI assistant."
        self.tools = tools or []
    
    def invoke(self, input_text: str) -> str:
        """
        Invoke the LLM with input text (simplified - no complex agents).
        
        Args:
            input_text: User input or task description
            
        Returns:
            LLM's response as string
        """
        # Direct LLM call - simpler and more reliable
        full_prompt = f"{self.system_prompt}\n\nUser: {input_text}\n\nAssistant:"
        response = self.llm.invoke(full_prompt)
        
        # Extract text from response
        if hasattr(response, 'content'):
            return response.content
        elif isinstance(response, str):
            return response
        else:
            return str(response)
    
    def structured_output(self, schema: type, input_text: str) -> Any:
        """
        Get structured output from the agent.
        
        Args:
            schema: Pydantic model class for output structure
            input_text: Input text to process
            
        Returns:
            Parsed object matching the schema
        """
        structured_llm = self.llm.with_structured_output(schema)
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=input_text)
        ]
        return structured_llm.invoke(messages)


class DataFetchAgent(BedrockAgentBase):
    """Agent for fetching and validating data from external sources."""
    
    def __init__(self):
        system_prompt = """You are a data acquisition specialist for a loan underwriting system.

Your responsibilities:
1. Fetch data from external APIs using available tools
2. Validate response data structure and quality
3. Extract relevant information for loan assessment
4. Handle errors gracefully with detailed context
5. Return clean, structured data

Always validate that responses contain expected fields and report any data quality issues."""
        
        super().__init__(
            model_id=os.getenv("BEDROCK_MODEL_NOVA", "amazon.nova-pro-v1:0"),
            system_prompt=system_prompt,
            temperature=0.1
        )
    
    def fetch_and_validate(self, data: Dict[str, Any], data_type: str) -> Dict[str, Any]:
        """
        Validate fetched data using the agent.
        
        Args:
            data: Raw data from API
            data_type: Type of data (bank, credit, documents)
            
        Returns:
            Validated and enriched data
        """
        prompt = f"""Validate this {data_type} data and extract key information:

Data: {json.dumps(data, indent=2)}

Ensure all required fields are present and values are valid. Return a summary of the validation."""
        
        validation_result = self.invoke(prompt)
        
        # Add validation metadata
        data["validation_status"] = "validated"
        data["validation_notes"] = validation_result
        
        return data


class CreditAssessmentAgent(BedrockAgentBase):
    """Agent for credit risk assessment."""
    
    def __init__(self):
        system_prompt = """You are a credit risk assessment specialist for loan underwriting.

Your responsibilities:
1. Analyze credit reports and scores
2. Evaluate credit history and payment patterns
3. Assess credit utilization and debt levels
4. Determine credit risk level (low, medium, high)
5. Provide clear recommendations with reasoning

Use industry-standard criteria:
- Score >= 750: Excellent (low risk)
- Score 650-749: Good (medium risk)
- Score 620-649: Fair (medium-high risk)
- Score < 620: Poor (high risk)"""
        
        super().__init__(
            model_id=os.getenv("BEDROCK_MODEL_CLAUDE"),
            system_prompt=system_prompt,
            temperature=0.1
        )
    
    def assess_credit(self, application: Dict, credit_data: Dict) -> Dict[str, Any]:
        """Assess credit risk based on credit report."""
        prompt = f"""Analyze this credit information for loan application:

Applicant: {application.get('name')}
Loan Amount: ${application.get('amount')}
Credit Score: {credit_data.get('score')}
Credit Report: {json.dumps(credit_data, indent=2)}

Provide:
1. Credit risk level
2. Key factors affecting the decision
3. Recommendation (approve/reject/review)
4. Reasoning for your assessment"""
        
        assessment = self.invoke(prompt)
        
        return {
            "credit_score": credit_data.get("score"),
            "risk_level": self._determine_risk_level(credit_data.get("score", 0)),
            "assessment": assessment,
            "provider": credit_data.get("provider", "unknown")
        }
    
    def _determine_risk_level(self, score: float) -> str:
        """Determine risk level from credit score."""
        if score >= 750:
            return "low"
        elif score >= 650:
            return "medium"
        elif score >= 620:
            return "medium-high"
        else:
            return "high"


class IncomeAssessmentAgent(BedrockAgentBase):
    """Agent for income and affordability assessment."""
    
    def __init__(self):
        system_prompt = """You are an income verification and affordability specialist.

Your responsibilities:
1. Verify income sources and stability
2. Calculate debt-to-income ratios
3. Assess loan affordability
4. Evaluate financial stability
5. Provide clear recommendations

Key metrics:
- DTI Ratio < 36%: Excellent
- DTI Ratio 36-43%: Acceptable
- DTI Ratio > 43%: High risk
- Annual income should be at least 2.5x the loan amount
- Loan amount should not exceed 40% of annual income"""
        
        super().__init__(
            model_id=os.getenv("BEDROCK_MODEL_CLAUDE"),
            system_prompt=system_prompt,
            temperature=0.1
        )
    
    def assess_income(
        self,
        application: Dict,
        bank_data: Dict,
        credit_data: Dict
    ) -> Dict[str, Any]:
        """Assess income and affordability."""
        prompt = f"""Analyze income and affordability for this loan application:

Applicant: {application.get('name')}
Declared Income: ${application.get('income')}
Loan Amount: ${application.get('amount')}
Bank Data: {json.dumps(bank_data, indent=2)}
Credit Data: {json.dumps(credit_data, indent=2)}

Calculate and assess:
1. Income verification
2. Debt-to-income ratio
3. Loan affordability
4. Financial stability
5. Recommendation with reasoning"""
        
        assessment = self.invoke(prompt)
        
        income = application.get("income", 0)
        amount = application.get("amount", 0)
        
        # Calculate annual income vs loan amount (more realistic)
        annual_income = income * 12
        income_ratio = annual_income / amount if amount > 0 else 0
        
        # Loan should be <= 40% of annual income (industry standard)
        affordability_ok = income_ratio >= 2.5  # Annual income should be 2.5x loan amount
        
        return {
            "income": income,
            "loan_amount": amount,
            "annual_income": annual_income,
            "income_to_loan_ratio": round(income_ratio, 2),
            "affordability_ok": affordability_ok,
            "assessment": assessment
        }


class ExpenseAssessmentAgent(BedrockAgentBase):
    """Agent for expense and cash flow assessment."""
    
    def __init__(self):
        system_prompt = """You are an expense analysis and cash flow specialist.

Your responsibilities:
1. Analyze monthly expenses and spending patterns
2. Calculate disposable income
3. Assess cash flow stability
4. Evaluate financial obligations
5. Determine repayment capacity

Key considerations:
- Disposable income should cover loan payment + 20% buffer
- Expense patterns should be stable
- No signs of financial distress"""
        
        super().__init__(
            model_id=os.getenv("BEDROCK_MODEL_NOVA", "amazon.nova-pro-v1:0"),
            system_prompt=system_prompt,
            temperature=0.1
        )
    
    def assess_expenses(self, application: Dict, bank_data: Dict) -> Dict[str, Any]:
        """Assess expenses and cash flow."""
        prompt = f"""Analyze expenses and cash flow for this loan application:

Applicant: {application.get('name')}
Monthly Income: ${application.get('income')}
Declared Expenses: ${application.get('expenses')}
Bank Data: {json.dumps(bank_data, indent=2)}

Assess:
1. Expense patterns and stability
2. Disposable income
3. Cash flow adequacy
4. Repayment capacity
5. Recommendation with reasoning"""
        
        assessment = self.invoke(prompt)
        
        income = application.get("income", 0)
        expenses = application.get("expenses", 0)
        disposable = income - expenses
        
        return {
            "monthly_income": income,
            "monthly_expenses": expenses,
            "disposable_income": disposable,
            "affordability_ok": disposable > 0,
            "assessment": assessment
        }


class SupervisorAgent(BedrockAgentBase):
    """Supervisor agent for final decision aggregation."""
    
    def __init__(self):
        system_prompt = """You are a senior loan underwriting supervisor with final decision authority.

Your responsibilities:
1. Review all specialist assessments (credit, income, expenses)
2. Synthesize information into a coherent analysis
3. Make final loan recommendation
4. Provide clear, actionable reasoning
5. Highlight key risk factors and strengths

Decision criteria:
- All assessments must be favorable for approval
- Any high-risk factors require rejection or manual review
- Borderline cases should be flagged for human review

Provide structured output with:
- Decision: approve/reject/review
- Confidence: high/medium/low
- Key factors supporting the decision
- Risk summary
- Detailed reasoning"""
        
        super().__init__(
            model_id=os.getenv("BEDROCK_MODEL_CLAUDE"),
            system_prompt=system_prompt,
            temperature=0.2
        )
    
    def aggregate_and_decide(
        self,
        application: Dict,
        income_assessment: Dict,
        expense_assessment: Dict,
        credit_assessment: Dict,
        documents: Dict
    ) -> Dict[str, Any]:
        """Make final loan decision based on all assessments."""
        prompt = f"""Review this complete loan application and make a final decision:

APPLICATION:
{json.dumps(application, indent=2)}

CREDIT ASSESSMENT:
{json.dumps(credit_assessment, indent=2)}

INCOME ASSESSMENT:
{json.dumps(income_assessment, indent=2)}

EXPENSE ASSESSMENT:
{json.dumps(expense_assessment, indent=2)}

DOCUMENTS:
{json.dumps(documents, indent=2)}

Provide your final decision with comprehensive reasoning."""
        
        decision_text = self.invoke(prompt)
        
        # Determine decision based on assessments
        credit_ok = credit_assessment.get("risk_level") in ["low", "medium"]
        income_ok = income_assessment.get("affordability_ok", False)
        expense_ok = expense_assessment.get("affordability_ok", False)
        
        if credit_ok and income_ok and expense_ok:
            decision = "approve"
            confidence = "high"
        elif not credit_ok or not income_ok:
            decision = "reject"
            confidence = "high"
        else:
            decision = "review"
            confidence = "medium"
        
        return {
            "decision": decision,
            "confidence": confidence,
            "reasoning": decision_text,
            "credit_risk": credit_assessment.get("risk_level"),
            "income_adequate": income_ok,
            "expenses_manageable": expense_ok
        }
