"""
MCP Server for Loan Underwriting Tools
Provides standardized tools for credit reports, bank data, and document verification
"""
import os
import json
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import httpx
from dotenv import load_dotenv

load_dotenv()

# Mock API base URL (Mockoon)
MOCK_API_BASE = os.getenv("MOCK_API_BASE", "http://localhost:3233")

app = Server("loan-underwriting-mcp")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools for loan underwriting."""
    return [
        Tool(
            name="fetch_credit_report",
            description="Fetch credit report from credit bureau (CIBIL or Experian)",
            inputSchema={
                "type": "object",
                "properties": {
                    "applicant_id": {
                        "type": "string",
                        "description": "Unique identifier for the applicant"
                    },
                    "provider": {
                        "type": "string",
                        "enum": ["cibil", "experian"],
                        "description": "Credit bureau provider"
                    }
                },
                "required": ["applicant_id", "provider"]
            }
        ),
        Tool(
            name="fetch_bank_account",
            description="Fetch bank account information for an applicant",
            inputSchema={
                "type": "object",
                "properties": {
                    "applicant_id": {
                        "type": "string",
                        "description": "Unique identifier for the applicant"
                    }
                },
                "required": ["applicant_id"]
            }
        ),
        Tool(
            name="fetch_documents",
            description="Fetch document verification status for an applicant",
            inputSchema={
                "type": "object",
                "properties": {
                    "applicant_id": {
                        "type": "string",
                        "description": "Unique identifier for the applicant"
                    }
                },
                "required": ["applicant_id"]
            }
        ),
        Tool(
            name="validate_credit_score",
            description="Validate if a credit score meets lending criteria",
            inputSchema={
                "type": "object",
                "properties": {
                    "score": {
                        "type": "number",
                        "description": "Credit score to validate"
                    },
                    "minimum_required": {
                        "type": "number",
                        "description": "Minimum required score",
                        "default": 620
                    }
                },
                "required": ["score"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls from agents."""
    
    if name == "fetch_credit_report":
        applicant_id = arguments["applicant_id"]
        provider = arguments["provider"]
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{MOCK_API_BASE}/{provider}",
                    params={"applicant_id": applicant_id},
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                # Add provider metadata
                data["provider"] = provider
                data["data_quality"] = "validated"
                
                return [TextContent(
                    type="text",
                    text=json.dumps(data, indent=2)
                )]
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": str(e), "provider": provider})
                )]
    
    elif name == "fetch_bank_account":
        applicant_id = arguments["applicant_id"]
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{MOCK_API_BASE}/bank",
                    params={"applicant_id": applicant_id},
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                return [TextContent(
                    type="text",
                    text=json.dumps(data, indent=2)
                )]
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": str(e)})
                )]
    
    elif name == "fetch_documents":
        applicant_id = arguments["applicant_id"]
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{MOCK_API_BASE}/documents",
                    params={"applicant_id": applicant_id},
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                return [TextContent(
                    type="text",
                    text=json.dumps(data, indent=2)
                )]
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": str(e)})
                )]
    
    elif name == "validate_credit_score":
        score = arguments["score"]
        minimum_required = arguments.get("minimum_required", 620)
        
        is_valid = score >= minimum_required
        risk_level = "low" if score >= 750 else "medium" if score >= 650 else "high"
        
        result = {
            "score": score,
            "minimum_required": minimum_required,
            "is_valid": is_valid,
            "risk_level": risk_level,
            "recommendation": "approve" if is_valid else "reject"
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    else:
        return [TextContent(
            type="text",
            text=json.dumps({"error": f"Unknown tool: {name}"})
        )]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
