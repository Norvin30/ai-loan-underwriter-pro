# AI-Powered Loan Underwriting System - Complete Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Technologies Used](#technologies-used)
4. [How It Works](#how-it-works)
5. [System Components](#system-components)
6. [Workflow Process](#workflow-process)
7. [Setup Requirements](#setup-requirements)
8. [Expected Behavior](#expected-behavior)
9. [Troubleshooting](#troubleshooting)

---

## Project Overview

This is an **AI-powered loan underwriting system** that automates the loan approval process using:
- **Temporal** for durable workflow orchestration
- **AWS Bedrock** for AI-powered decision making
- **LangChain** for agent framework
- **Next.js** for modern web interface
- **FastAPI** for backend API
- **Mockoon** for simulating external banking APIs

### What Does It Do?

The system takes a loan application and automatically:
1. Fetches applicant data from multiple sources (bank, credit bureaus, documents)
2. Uses AI agents to analyze income, expenses, and credit risk
3. Makes an intelligent loan approval decision with detailed reasoning
4. Provides explainable AI decisions for human review

---

## Architecture

### High-Level Architecture

```
┌─────────────────┐
│   Next.js UI    │ ← User submits loan application
│  (Port 3000)    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  FastAPI Backend│ ← Receives application, starts Temporal workflow
│  (Port 8000)    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Temporal Server │ ← Orchestrates durable workflow
│  (Port 7233)    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Temporal Worker │ ← Executes activities (data fetch + AI analysis)
│  (Python)       │
└────────┬────────┘
         │
         ├──────────────────┐
         ↓                  ↓
┌─────────────────┐  ┌──────────────────┐
│  AWS Bedrock    │  │  Mockoon APIs    │
│  AI Models      │  │  (Port 3233)     │
│  - Titan        │  │  - Bank API      │
│  - Nova Lite    │  │  - Credit APIs   │
└─────────────────┘  └──────────────────┘
```

### Component Interaction Flow

```
User → Frontend → Backend → Temporal → Worker → AI Agents → Decision
                                ↓
                          Mock APIs (Bank/Credit)
```

---

## Technologies Used

### 1. **Temporal Workflow Engine**
- **Purpose**: Durable workflow orchestration
- **Why**: Ensures loan processing completes even if services crash
- **Features**:
  - Automatic retries on failures
  - Workflow state persistence
  - Fallback strategies (e.g., CIBIL → Experian)
  - Activity timeouts and error handling

### 2. **AWS Bedrock (AI Models)**
- **Purpose**: AI-powered decision making
- **Models Used**:
  - **Amazon Titan Text Premier**: Main reasoning model
  - **Amazon Nova Lite**: Cost-effective analysis
- **Why**: Provides sophisticated AI analysis without managing infrastructure
- **Cost**: Pay-per-use, ~$0.01-0.05 per loan application

### 3. **LangChain**
- **Purpose**: AI agent framework
- **Why**: Simplifies integration with Bedrock models
- **Features**:
  - Structured prompts for each agent
  - Model abstraction layer
  - Easy model switching

### 4. **Next.js (Frontend)**
- **Purpose**: Modern web interface
- **Features**:
  - React-based UI
  - Server-side rendering
  - TypeScript for type safety
  - Tailwind CSS for styling
- **Port**: 3000

### 5. **FastAPI (Backend)**
- **Purpose**: REST API for workflow management
- **Endpoints**:
  - `POST /workflows/start` - Start loan workflow
  - `GET /workflows/{id}` - Get workflow status
  - `GET /workflows` - List all workflows
- **Port**: 8000

### 6. **Mockoon**
- **Purpose**: Simulate external banking APIs
- **APIs Provided**:
  - `/bank` - Bank account data
  - `/cibil` - CIBIL credit report
  - `/experian` - Experian credit report (fallback)
  - `/documents` - Applicant documents
- **Port**: 3233

---

## How It Works

### Step-by-Step Process

#### 1. **User Submits Application**
- User fills form on Next.js frontend (http://localhost:3000)
- Form includes: Name, Amount, Income, Expenses, Applicant ID
- Frontend sends POST request to FastAPI backend

#### 2. **Backend Starts Temporal Workflow**
- FastAPI receives application
- Connects to Temporal server
- Starts `SupervisorWorkflow` with application data
- Returns workflow ID to frontend

#### 3. **Temporal Orchestrates Workflow**
- Temporal server manages workflow execution
- Ensures durability (survives crashes)
- Coordinates activity execution
- Handles retries and timeouts

#### 4. **Worker Executes Activities**

**Phase 1: Data Acquisition**
```
fetch_bank_account(applicant_id)
  ↓ Calls Mockoon API
  ↓ Returns bank account data

fetch_documents(applicant_id)
  ↓ Calls Mockoon API
  ↓ Returns document list

fetch_credit_report_cibil(applicant_id)
  ↓ Calls Mockoon API
  ↓ Returns credit score & history
  ↓ If fails → fallback to Experian
```

**Phase 2: AI Analysis**
```
income_assessment(application, bank, credit)
  ↓ AI Agent analyzes income vs loan amount
  ↓ Calculates debt-to-income ratio
  ↓ Returns affordability assessment

expense_assessment(application, bank)
  ↓ AI Agent analyzes spending patterns
  ↓ Calculates disposable income
  ↓ Returns cash flow assessment

credit_assessment(application, credit)
  ↓ AI Agent evaluates credit risk
  ↓ Analyzes credit score & history
  ↓ Returns risk level (low/medium/high)
```

**Phase 3: Final Decision**
```
aggregate_and_decide(all_assessments)
  ↓ Supervisor AI Agent reviews all data
  ↓ Synthesizes information
  ↓ Makes final decision: approve/reject/review
  ↓ Provides detailed reasoning
```

#### 5. **Results Returned**
- Workflow completes with decision
- Backend stores result
- Frontend displays decision in "Review Workflows" tab

---

## System Components

### Backend Components

#### 1. **Temporal Worker** (`backend/worker.py`)
- Connects to Temporal server
- Registers workflows and activities
- Polls for tasks to execute
- Loads environment variables

#### 2. **Activities** (`backend/activities.py`)
- `fetch_bank_account` - Get bank data
- `fetch_documents` - Get documents
- `fetch_credit_report_cibil` - Get CIBIL report
- `fetch_credit_report_experian` - Fallback credit report
- `income_assessment` - AI income analysis
- `expense_assessment` - AI expense analysis
- `credit_assessment` - AI credit analysis
- `aggregate_and_decide` - Final AI decision

#### 3. **Workflows** (`backend/workflows.py`)
- `SupervisorWorkflow` - Main orchestration logic
- Defines execution order
- Handles fallback strategies
- Manages error handling

#### 4. **AI Agents** (`backend/classes/agents/bedrock_agent.py`)

**BedrockAgentBase**
- Base class for all agents
- Initializes AWS Bedrock client
- Handles model invocation
- Manages credentials

**DataFetchAgent**
- Validates fetched data
- Ensures data quality
- Uses Nova Lite model

**IncomeAssessmentAgent**
- Analyzes income vs loan amount
- Calculates affordability
- Uses Titan model

**ExpenseAssessmentAgent**
- Analyzes spending patterns
- Calculates disposable income
- Uses Nova Lite model

**CreditAssessmentAgent**
- Evaluates credit risk
- Analyzes credit history
- Uses Titan model

**SupervisorAgent**
- Makes final decision
- Synthesizes all assessments
- Provides reasoning
- Uses Titan model

#### 5. **FastAPI Backend** (`backend/main.py`)
- REST API endpoints
- Temporal client integration
- CORS configuration
- Workflow management

### Frontend Components

#### 1. **Main Page** (`frontend/app/page.tsx`)
- Tab-based interface
- Three tabs: Submit, Review, All Workflows
- State management

#### 2. **SubmitApplication** (`frontend/components/SubmitApplication.tsx`)
- Loan application form
- Form validation
- API integration
- Success/error handling

#### 3. **ReviewWorkflow** (`frontend/components/ReviewWorkflow.tsx`)
- Single workflow details
- Decision display
- Assessment breakdown
- Reasoning visualization

#### 4. **WorkflowsList** (`frontend/components/WorkflowsList.tsx`)
- All workflows table
- Status indicators
- Quick view of decisions

---

## Workflow Process

### Detailed Workflow Diagram

```
START
  ↓
[User Submits Application]
  ↓
[Backend Receives Request]
  ↓
[Start Temporal Workflow]
  ↓
┌─────────────────────────────┐
│  PHASE 1: DATA ACQUISITION  │
└─────────────────────────────┘
  ↓
[Fetch Bank Account] ──→ Mockoon API
  ↓
[Fetch Documents] ──→ Mockoon API
  ↓
[Fetch Credit Report (CIBIL)] ──→ Mockoon API
  ↓ (if fails)
[Fetch Credit Report (Experian)] ──→ Mockoon API
  ↓
┌─────────────────────────────┐
│   PHASE 2: AI ANALYSIS      │
└─────────────────────────────┘
  ↓
[Income Assessment] ──→ AWS Bedrock (Titan)
  ↓ Analyzes: Income/Loan ratio, DTI
  ↓
[Expense Assessment] ──→ AWS Bedrock (Nova)
  ↓ Analyzes: Cash flow, disposable income
  ↓
[Credit Assessment] ──→ AWS Bedrock (Titan)
  ↓ Analyzes: Credit score, risk level
  ↓
┌─────────────────────────────┐
│  PHASE 3: FINAL DECISION    │
└─────────────────────────────┘
  ↓
[Supervisor Agent] ──→ AWS Bedrock (Titan)
  ↓ Synthesizes all assessments
  ↓ Makes decision: approve/reject/review
  ↓ Provides detailed reasoning
  ↓
[Return Decision to Backend]
  ↓
[Store Result]
  ↓
[Display in Frontend]
  ↓
END
```


### Decision Logic

**Approval Criteria:**
- Credit score ≥ 650 (low/medium risk)
- Income to loan ratio ≥ 2:1
- Positive disposable income
- All documents present

**Rejection Criteria:**
- Credit score < 620 (high risk)
- Income to loan ratio < 1.5:1
- Negative cash flow

**Review Criteria:**
- Borderline cases
- Mixed signals from assessments
- Requires human judgment

---

## Setup Requirements

### Prerequisites

1. **Python 3.11+**
   - Virtual environment
   - Dependencies from `requirements.txt`

2. **Node.js 18+**
   - npm or yarn
   - Next.js dependencies

3. **Temporal CLI**
   - Windows: `temporal.exe`
   - Must be in PATH or run from directory

4. **Mockoon**
   - Desktop application
   - Import `mockoon/bankAPI.json`

5. **AWS Account**
   - Valid payment method (even with credits)
   - Bedrock access in us-east-1
   - Access keys configured

### Environment Variables (`.env`)

```env
# AWS Bedrock Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key

# Bedrock Model IDs
BEDROCK_MODEL_CLAUDE=amazon.titan-text-premier-v1:0
BEDROCK_MODEL_NOVA=amazon.nova-lite-v1:0

# Temporal Configuration
TEMPORAL_NAMESPACE=default
TEMPORAL_TASK_QUEUE=loan-underwriter-queue

# API Configuration
BACKEND_PORT=8000
FRONTEND_PORT=3000
MOCK_API_BASE=http://localhost:3233
```

### Running the System

**5 Services Must Be Running:**

1. **Temporal Server** (Tab 1)
   ```cmd
   temporal server start-dev
   ```

2. **Mockoon** (Separate App)
   - Open Mockoon
   - Import `mockoon/bankAPI.json`
   - Click green play button
   - Verify port 3233

3. **Worker** (Tab 3)
   ```cmd
   .venv\Scripts\activate
   python backend/worker.py
   ```

4. **Backend** (Tab 4)
   ```cmd
   .venv\Scripts\activate
   python backend/main.py
   ```

5. **Frontend** (Tab 5)
   ```cmd
   cd frontend
   npm run dev
   ```

---

## Expected Behavior

### When Everything Works Correctly

#### 1. **Application Submission**
- User fills form at http://localhost:3000
- Clicks "Submit Application"
- Sees success message: "Application submitted! Workflow ID: loan-xxxxx"

#### 2. **Worker Terminal Output**
```
[BEDROCK AGENT] AWS Credentials Status:
  - Access Key: ✓ Found (AKIAV47R...)
  - Secret Key: ✓ Found (********************)
  - Region: us-east-1
[BEDROCK AGENT] Initialized with model: amazon.titan-text-premier-v1:0
Worker started, polling task queue: loan-underwriter-queue

INFO: Successfully fetched bank account data for APP001
INFO: Successfully retrieved 3 documents
INFO: Successfully fetched CIBIL credit report for APP001
INFO: Income assessment completed: True
INFO: Expense assessment completed: True
INFO: Credit assessment completed: low
INFO: Final decision: approve with high confidence
```

#### 3. **Review Workflows Tab**
- Shows workflow in table
- Status: "completed"
- Decision: "approve" (green) or "reject" (red)
- Click "View Details" to see full analysis

#### 4. **Workflow Details**
```
Decision: APPROVE
Confidence: High

Credit Assessment:
- Score: 750
- Risk Level: Low
- Provider: CIBIL

Income Assessment:
- Monthly Income: $100,000
- Loan Amount: $50,000
- Income to Loan Ratio: 2.0
- Affordability: ✓ OK

Expense Assessment:
- Monthly Expenses: $30,000
- Disposable Income: $70,000
- Cash Flow: ✓ Positive

AI Reasoning:
"The applicant demonstrates strong financial stability with excellent credit score (750), healthy income-to-loan ratio (2:1), and positive cash flow. All risk factors are favorable. Recommendation: APPROVE with standard terms."
```

### Cost Per Test Run

- **Data Fetch Activities**: Free (mock APIs)
- **AI Analysis (4 agents)**: ~$0.01-0.03
- **Total per application**: ~$0.01-0.05

With $67 in credits, you can test **1,000+ applications**.

---

## Troubleshooting

### Common Issues

#### 1. **AWS Credentials Not Found**
**Symptom**: `✗ NOT FOUND` in worker output

**Solution**:
- Check `.env` file has correct keys
- Restart worker after updating `.env`
- Verify `.env` is in project root

#### 2. **Invalid Payment Instrument**
**Symptom**: `AccessDeniedException: INVALID_PAYMENT_INSTRUMENT`

**Solution**:
- Add credit/debit card to AWS account
- Go to Billing → Payment Methods
- Wait 2 minutes after adding card

#### 3. **Model Access Denied**
**Symptom**: `Model access is denied` or `ValidationException`

**Solution**:
- Use Amazon models (Titan, Nova) instead of Claude
- Update `.env`:
  ```
  BEDROCK_MODEL_CLAUDE=amazon.titan-text-premier-v1:0
  BEDROCK_MODEL_NOVA=amazon.nova-lite-v1:0
  ```
- Restart worker

#### 4. **Inference Profile Error**
**Symptom**: `on-demand throughput isn't supported`

**Solution**:
- Don't use Claude 3.5 Sonnet directly
- Use inference profile: `us.anthropic.claude-3-5-sonnet-20241022-v2:0`
- Or switch to Titan (recommended)

#### 5. **Mockoon Not Responding**
**Symptom**: `Failed to fetch bank account data`

**Solution**:
- Check Mockoon is running (green play button)
- Verify port 3233 in Mockoon settings
- Test: `curl http://localhost:3233/bank?applicant_id=APP001`

#### 6. **Temporal Not Running**
**Symptom**: `Worker cannot connect to Temporal`

**Solution**:
- Start Temporal: `temporal server start-dev`
- Check port 7233 is not blocked
- Verify Temporal UI: http://localhost:8233

#### 7. **Frontend Not Loading**
**Symptom**: Browser shows "Cannot connect"

**Solution**:
- Check frontend is running: `npm run dev`
- Verify port 3000 is free
- Check console for errors

#### 8. **Backend API Errors**
**Symptom**: Frontend shows "Failed to submit"

**Solution**:
- Check backend is running: `python backend/main.py`
- Verify port 8000 is free
- Check backend logs for errors

---

## Project Structure

```
temporal-agentic-loan-underwriter/
├── backend/
│   ├── classes/
│   │   └── agents/
│   │       ├── bedrock_agent.py      # AI agents
│   │       ├── mcp_tools.py          # MCP integration
│   │       └── __init__.py
│   ├── activities.py                 # Temporal activities
│   ├── workflows.py                  # Temporal workflows
│   ├── worker.py                     # Temporal worker
│   └── main.py                       # FastAPI backend
├── frontend/
│   ├── app/
│   │   ├── page.tsx                  # Main page
│   │   ├── layout.tsx                # Layout
│   │   └── globals.css               # Styles
│   ├── components/
│   │   ├── SubmitApplication.tsx     # Submit form
│   │   ├── ReviewWorkflow.tsx        # Workflow details
│   │   └── WorkflowsList.tsx         # All workflows
│   ├── package.json
│   └── next.config.js
├── mockoon/
│   └── bankAPI.json                  # Mock API config
├── mcp_server/
│   └── server.py                     # MCP server (future)
├── .env                              # Environment variables
├── requirements.txt                  # Python dependencies
├── README.md                         # Project readme
├── PROJECT_OVERVIEW.md               # This file
└── TROUBLESHOOTING.md                # Troubleshooting guide
```

---

## Future Enhancements

### Planned Features

1. **MCP Server Integration**
   - Standardized tool interface
   - Better agent coordination
   - Extensible architecture

2. **Additional AI Models**
   - Claude 3.5 Sonnet (when marketplace works)
   - GPT-4 integration
   - Model comparison

3. **Enhanced UI**
   - Real-time workflow progress
   - Interactive decision tree
   - Document upload

4. **Production Features**
   - User authentication
   - Role-based access
   - Audit logging
   - Compliance reporting

5. **Advanced Analytics**
   - Approval rate tracking
   - Model performance metrics
   - Cost optimization

---

## Key Takeaways

### What Makes This System Unique

1. **Durable Workflows**: Temporal ensures no loan application is lost
2. **AI-Powered**: Multiple specialized AI agents for different aspects
3. **Explainable AI**: Every decision comes with detailed reasoning
4. **Fault Tolerant**: Automatic retries and fallback strategies
5. **Scalable**: Can handle thousands of applications
6. **Cost Effective**: Pay only for what you use (~$0.01-0.05 per application)

### Technologies Learned

- Temporal workflow orchestration
- AWS Bedrock AI integration
- LangChain agent framework
- Next.js modern web development
- FastAPI backend development
- Microservices architecture

---

## Support & Resources

### Documentation
- Temporal: https://docs.temporal.io
- AWS Bedrock: https://docs.aws.amazon.com/bedrock
- LangChain: https://python.langchain.com
- Next.js: https://nextjs.org/docs

### Project Files
- `README.md` - Quick start guide
- `TROUBLESHOOTING.md` - Common issues
- `TESTING_CHECKLIST.md` - Testing steps
- `QUICK_REFERENCE.md` - Command reference

---

**Last Updated**: February 7, 2026
**Version**: 2.0
**Status**: In Development
