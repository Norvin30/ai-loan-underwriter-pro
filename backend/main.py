"""
FastAPI Backend for Loan Underwriting System
Updated to use LangChain agents with AWS Bedrock models
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from temporalio.client import Client
import os
from dotenv import load_dotenv
from typing import Optional
import sys
from pathlib import Path

# Load .env from project root
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from backend.classes.agents.bedrock_agent import BedrockAgentBase

app = FastAPI(
    title="Loan Underwriting API",
    description="AI-powered loan underwriting with AWS Bedrock and Temporal",
    version="2.0.0"
)

# Add CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMPORAL_NAMESPACE = os.getenv("TEMPORAL_NAMESPACE", "default")
TASK_QUEUE = os.getenv("TEMPORAL_TASK_QUEUE", "loan-underwriter-queue")

# Initialize Bedrock agent for validation
try:
    validation_agent = BedrockAgentBase(
        system_prompt="You are a data validation assistant. Validate and structure loan application data."
    )
    bedrock_enabled = True
    print("✅ AWS Bedrock agent initialized successfully")
except Exception as e:
    print(f"⚠️  Warning: Failed to initialize Bedrock agent: {e}")
    validation_agent = None
    bedrock_enabled = False


class LoanApplication(BaseModel):
    """Loan application data model for processing loan requests."""
    applicant_id: str = Field(description="Unique identifier for the loan applicant")
    name: str = Field(description="Full name of the loan applicant")
    amount: float = Field(description="Requested loan amount")
    income: Optional[float] = Field(default=None, description="Monthly income of the applicant")
    expenses: Optional[float] = Field(default=None, description="Monthly expenses of the applicant")


class ReviewRequest(BaseModel):
    """Human review request for loan application processing."""
    action: str = Field(description="Review action to take (approve, reject, etc.)")
    note: str = Field(default="", description="Optional review notes or comments")


class EmailNotification(BaseModel):
    """Email notification request for loan status updates."""
    workflow_id: str = Field(description="Workflow ID for the loan application")
    email: EmailStr = Field(description="Email address to send notification")
    applicant_name: str = Field(description="Name of the applicant")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "Loan Underwriting API",
        "version": "2.0.0",
        "status": "healthy",
        "bedrock_enabled": bedrock_enabled,
        "models": {
            "claude": os.getenv("BEDROCK_MODEL_CLAUDE", "anthropic.claude-3-5-sonnet-20241022-v2:0"),
            "nova": os.getenv("BEDROCK_MODEL_NOVA", "amazon.nova-pro-v1:0")
        }
    }


@app.post("/submit")
async def submit_application(app_data: dict):
    """
    Submit a new loan application.
    
    Creates a Temporal workflow for processing the loan application
    with AI-powered assessment using AWS Bedrock models.
    """
    try:
        # Validate with Bedrock if available, otherwise use direct Pydantic validation
        if bedrock_enabled and validation_agent:
            try:
                validated_data = validation_agent.structured_output(
                    LoanApplication,
                    f"Validate this loan application data: {app_data}"
                )
                print(f"✅ Application validated via Bedrock: {validated_data.applicant_id}")
            except Exception as bedrock_error:
                print(f"⚠️  Bedrock validation failed, using direct validation: {bedrock_error}")
                validated_data = LoanApplication(**app_data)
        else:
            validated_data = LoanApplication(**app_data)
        
        # Connect to Temporal
        client = await Client.connect("localhost:7233", namespace=TEMPORAL_NAMESPACE)
        print(f"✅ Connected to Temporal")
        
        # Start workflow
        handle = await client.start_workflow(
            "SupervisorWorkflow",
            validated_data.model_dump(),
            id=f"loan-{validated_data.applicant_id}",
            task_queue=TASK_QUEUE,
        )
        
        print(f"✅ Workflow started: {handle.id}")
        return {
            "workflow_id": handle.id,
            "run_id": handle.run_id,
            "applicant_id": validated_data.applicant_id,
            "status": "processing"
        }
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status/{workflow_id}")
async def status(workflow_id: str):
    """Get workflow status and metadata."""
    client = await Client.connect("localhost:7233", namespace=TEMPORAL_NAMESPACE)
    try:
        wf = client.get_workflow_handle(workflow_id)
        
        # Query workflow for summary and final result
        summary = None
        final = None
        
        try:
            summary = await wf.query("get_summary")
        except Exception:
            summary = None
        
        try:
            final = await wf.query("get_final_result")
        except Exception:
            final = None
        
        # Get workflow description
        try:
            desc = await wf.describe()
            status_info = {
                "status": desc.status.name,
                "start_time": desc.start_time.isoformat() if desc.start_time else None,
                "close_time": desc.close_time.isoformat() if desc.close_time else None,
            }
        except Exception:
            status_info = {"status": "unknown"}
        
        return {
            "workflow_id": workflow_id,
            "summary": summary,
            "final_result": final,
            **status_info
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflow/{workflow_id}/summary")
async def get_summary(workflow_id: str):
    """Get workflow summary for human review."""
    client = await Client.connect("localhost:7233", namespace=TEMPORAL_NAMESPACE)
    try:
        wf = client.get_workflow_handle(workflow_id)
        summary = await wf.query("get_summary")
        
        return {
            "workflow_id": workflow_id,
            "summary": summary if summary is not None else {"status": "pending"}
        }
        
    except Exception as e:
        print(f"❌ Error in get_summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/workflow/{workflow_id}/review")
async def human_review(workflow_id: str, review: dict):
    """
    Submit human review decision for a loan application.
    
    Sends a signal to the Temporal workflow to continue processing
    with the human decision.
    """
    try:
        # Validate review with Bedrock if available
        if bedrock_enabled and validation_agent:
            try:
                validated_review = validation_agent.structured_output(
                    ReviewRequest,
                    f"Validate this review request data: {review}"
                )
                print(f"✅ Review validated via Bedrock: {validated_review.action}")
            except Exception as bedrock_error:
                print(f"⚠️  Bedrock validation failed, using direct validation: {bedrock_error}")
                validated_review = ReviewRequest(**review)
        else:
            validated_review = ReviewRequest(**review)
        
        # Connect to Temporal and send signal
        client = await Client.connect("localhost:7233", namespace=TEMPORAL_NAMESPACE)
        wf = client.get_workflow_handle(workflow_id)
        await wf.signal("human_review", validated_review.model_dump())
        
        print(f"✅ Review signal sent: {workflow_id} - {validated_review.action}")
        return {
            "workflow_id": workflow_id,
            "signaled": True,
            "action": validated_review.action
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflow/{workflow_id}/final")
async def get_final_result(workflow_id: str):
    """Get final workflow result after human review."""
    client = await Client.connect("localhost:7233", namespace=TEMPORAL_NAMESPACE)
    try:
        wf = client.get_workflow_handle(workflow_id)
        final = await wf.query("get_final_result")
        
        return {
            "workflow_id": workflow_id,
            "final_result": final if final is not None else {"status": "not_ready"}
        }
        
    except Exception as e:
        print(f"❌ Error in get_final_result: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflows")
async def list_workflows():
    """List all loan workflows with their status, summary, and metadata."""
    client = await Client.connect("localhost:7233", namespace=TEMPORAL_NAMESPACE)
    try:
        workflows_list = []
        
        # List workflows - filter by loan workflows
        async for workflow in client.list_workflows("WorkflowType='SupervisorWorkflow'"):
            try:
                wf = client.get_workflow_handle(workflow.id)
                summary = None
                final_result = None
                
                try:
                    summary = await wf.query("get_summary")
                except Exception:
                    summary = None
                
                try:
                    final_result = await wf.query("get_final_result")
                except Exception:
                    final_result = None
                
                # Extract key information
                workflow_info = {
                    "workflow_id": workflow.id,
                    "run_id": workflow.run_id,
                    "status": workflow.status.name,
                    "start_time": workflow.start_time.isoformat() if workflow.start_time else None,
                    "close_time": workflow.close_time.isoformat() if workflow.close_time else None,
                    "applicant_name": summary.get("application", {}).get("name") if summary else "Unknown",
                    "applicant_id": summary.get("application", {}).get("applicant_id") if summary else "Unknown",
                    "loan_amount": summary.get("application", {}).get("amount") if summary else 0,
                    "ai_recommendation": summary.get("suggested_decision", {}).get("decision") if summary else "Pending",
                    "ai_summary": summary.get("suggested_decision", {}).get("reasoning") if summary else "Processing...",
                    "human_decision": final_result.get("human_decision", {}).get("action") if final_result else None,
                    "summary": summary,
                    "final_result": final_result
                }
                
                workflows_list.append(workflow_info)
                
            except Exception as e:
                print(f"⚠️  Error processing workflow {workflow.id}: {e}")
                continue
        
        return {"workflows": workflows_list, "count": len(workflows_list)}
        
    except Exception as e:
        print(f"❌ Error listing workflows: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


@app.post("/notify")
async def send_notification(notification: EmailNotification):
    """
    Send email notification for loan status (simulated).
    
    In production, this would integrate with services like:
    - AWS SES (Simple Email Service)
    - SendGrid
    - Mailgun
    
    For now, it logs the notification.
    """
    try:
        # Simulate email sending
        print(f"📧 Email Notification Sent!")
        print(f"   To: {notification.email}")
        print(f"   Applicant: {notification.applicant_name}")
        print(f"   Workflow ID: {notification.workflow_id}")
        print(f"   Subject: Loan Application Status Update")
        
        return {
            "success": True,
            "message": f"Notification sent to {notification.email}",
            "workflow_id": notification.workflow_id,
            "note": "This is a simulated notification. In production, integrate with AWS SES or SendGrid."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def get_statistics():
    """
    Get system statistics and metrics.
    
    NEW FEATURE by Norvin Samson Anthony:
    Provides overview of loan processing statistics.
    """
    client = await Client.connect("localhost:7233", namespace=TEMPORAL_NAMESPACE)
    try:
        workflows_list = []
        
        async for workflow in client.list_workflows("WorkflowType='SupervisorWorkflow'"):
            try:
                wf = client.get_workflow_handle(workflow.id)
                summary = None
                
                try:
                    summary = await wf.query("get_summary")
                except Exception:
                    pass
                
                workflows_list.append({
                    "status": workflow.status.name,
                    "decision": summary.get("suggested_decision", {}).get("decision") if summary else None
                })
                
            except Exception:
                continue
        
        # Calculate statistics
        total = len(workflows_list)
        running = len([w for w in workflows_list if w["status"] == "RUNNING"])
        completed = len([w for w in workflows_list if w["status"] == "COMPLETED"])
        approved = len([w for w in workflows_list if w.get("decision") == "approve"])
        rejected = len([w for w in workflows_list if w.get("decision") == "reject"])
        
        return {
            "total_applications": total,
            "running": running,
            "completed": completed,
            "approved": approved,
            "rejected": rejected,
            "approval_rate": round((approved / total * 100) if total > 0 else 0, 1),
            "system_info": {
                "bedrock_enabled": bedrock_enabled,
                "models": {
                    "claude": os.getenv("BEDROCK_MODEL_CLAUDE"),
                    "nova": os.getenv("BEDROCK_MODEL_NOVA")
                },
                "version": "2.0.0",
                "developer": "Norvin Samson Anthony"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
