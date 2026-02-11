# 🚀 Quick Start Guide - Windows Local Setup

## Prerequisites Installation

### 1. Install Python 3.9+
```powershell
# Download from https://www.python.org/downloads/
# During installation, CHECK "Add Python to PATH"

# Verify installation
python --version
```

### 2. Install Node.js 18+
```powershell
# Download from https://nodejs.org/
# Install LTS version

# Verify installation
node --version
npm --version
```

### 3. Install Temporal CLI
```powershell
# Using PowerShell as Administrator
# Option A: Using Chocolatey (if installed)
choco install temporal

# Option B: Download binary from https://github.com/temporalio/cli/releases
# Extract and add to PATH
```

### 4. Install Mockoon
```powershell
# Download from https://mockoon.com/download/
# Install the Windows version
```

### 5. Setup AWS Account
1. Go to https://aws.amazon.com/free/
2. Create a free account
3. Go to AWS Console → IAM → Create Access Key
4. Save your Access Key ID and Secret Access Key

### 6. Enable AWS Bedrock Models
1. Go to AWS Console → Bedrock
2. Click "Model access" in left sidebar
3. Click "Enable specific models"
4. Enable:
   - Anthropic Claude 3.5 Sonnet
   - Amazon Nova Pro
5. Click "Save changes" (approval is usually instant)

---

## 🎯 Project Setup (5 Minutes)

### Step 1: Clone and Setup Python
```powershell
# Clone the repository
git clone <your-repo-url>
cd temporal-agentic-loan-underwriter

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment
```powershell
# Copy example environment file
copy .env.example .env

# Edit .env file with your AWS credentials
notepad .env
```

Add your AWS credentials to `.env`:
```env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here

BEDROCK_MODEL_CLAUDE=anthropic.claude-3-5-sonnet-20241022-v2:0
BEDROCK_MODEL_NOVA=amazon.nova-pro-v1:0

TEMPORAL_NAMESPACE=default
TEMPORAL_TASK_QUEUE=loan-underwriter-queue

MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=3100

MOCK_API_BASE=http://localhost:3233
```

### Step 3: Setup Frontend
```powershell
cd frontend
npm install
cd ..
```

---

## 🏃 Running the Application

### Open 5 PowerShell/CMD Windows:

#### **Window 1: Temporal Server**
```powershell
# Start Temporal development server
temporal server start-dev
```
✅ Wait until you see "Temporal server is running"

#### **Window 2: Mockoon**
```powershell
# Open Mockoon application
# Click "Import" → Select mockoon/bankAPI.json
# Click "Start" button (green play icon)
# Ensure it's running on port 3233
```
✅ You should see "Server started on port 3233"

#### **Window 3: Temporal Worker**
```powershell
cd temporal-agentic-loan-underwriter
.venv\Scripts\activate
python backend/worker.py
```
✅ Wait for "Worker started successfully"

#### **Window 4: FastAPI Backend**
```powershell
cd temporal-agentic-loan-underwriter
.venv\Scripts\activate
uvicorn backend.main:app --reload --port 8000
```
✅ Wait for "Application startup complete"

#### **Window 5: Next.js Frontend**
```powershell
cd temporal-agentic-loan-underwriter\frontend
npm run dev
```
✅ Wait for "Ready on http://localhost:3000"

---

## 🎉 Access the Application

Open your browser and go to:
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Temporal UI**: http://localhost:8233

---

## 🧪 Test the Application

### 1. Submit a Loan Application
1. Go to http://localhost:3000
2. Click "Submit Application" tab
3. Fill in:
   - Applicant ID: `12345`
   - Name: `John Doe`
   - Loan Amount: `50000`
   - Monthly Income: `8000`
   - Monthly Expenses: `3000`
4. Click "Submit Application"
5. Copy the Workflow ID

### 2. Review the Loan
1. Click "Review Loan" tab
2. Paste the Workflow ID
3. Click "Fetch Details"
4. Review AI analysis
5. Click "Approve" or "Reject"

### 3. View All Workflows
1. Click "All Workflows" tab
2. Click "Refresh"
3. See all loan applications

---

## 🛑 Stopping the Application

Press `Ctrl+C` in each window to stop:
1. Frontend (Window 5)
2. Backend (Window 4)
3. Worker (Window 3)
4. Mockoon (Window 2) - Click Stop button
5. Temporal (Window 1)

---

## 🐛 Common Issues

### Issue: "Python not found"
**Solution**: Reinstall Python and check "Add to PATH" during installation

### Issue: "AWS credentials not found"
**Solution**: 
```powershell
# Test AWS credentials
aws configure
# Enter your Access Key ID and Secret Access Key
```

### Issue: "Port already in use"
**Solution**:
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

### Issue: "Temporal connection failed"
**Solution**: Make sure Temporal server is running in Window 1

### Issue: "Bedrock model not accessible"
**Solution**: 
1. Go to AWS Console → Bedrock → Model access
2. Enable Claude 3.5 Sonnet and Nova Pro
3. Wait for approval (usually instant)

---

## 💡 Tips

1. **Keep all 5 windows open** while using the application
2. **Check logs** in each window if something doesn't work
3. **Use Temporal UI** (http://localhost:8233) to debug workflows
4. **Check API docs** (http://localhost:8000/docs) to test endpoints directly

---

## 📊 System Requirements

- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB free space
- **Internet**: Required for AWS Bedrock API calls
- **OS**: Windows 10/11

---

## 🎓 Next Steps

1. ✅ Run the application locally
2. 📖 Read the main README.md for architecture details
3. 🔧 Customize agents in `backend/classes/agents/`
4. 🎨 Modify UI in `frontend/components/`
5. 🚀 Deploy to cloud when ready

---

**Need Help?** Check the main README.md or create an issue on GitHub!
