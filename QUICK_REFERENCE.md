# 🚀 Quick Reference Card

## One-Time Setup Commands

```powershell
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install frontend dependencies
cd frontend
npm install
cd ..

# 4. Create .env file (copy from .env.example and add your AWS credentials)
copy .env.example .env
```

---

## Starting the Application (5 Terminal Tabs)

### Tab 1: Temporal Server
```powershell
temporal server start-dev
```
✅ Wait for: "Temporal server is running"

### Tab 2: Mockoon
```powershell
# Open Mockoon app → Import mockoon/bankAPI.json → Click Start
# This tab is just for reference
```
✅ Wait for: Green "Running" status in Mockoon

### Tab 3: Worker
```powershell
.venv\Scripts\activate
python backend/worker.py
```
✅ Wait for: "Worker started successfully"

### Tab 4: Backend
```powershell
.venv\Scripts\activate
uvicorn backend.main:app --reload --port 8000
```
✅ Wait for: "Application startup complete"

### Tab 5: Frontend
```powershell
cd frontend
npm run dev
```
✅ Wait for: "Ready on http://localhost:3000"

---

## Access URLs

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:3000 |
| **Backend API** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |
| **Temporal UI** | http://localhost:8233 |

---

## Testing Flow

1. **Submit Application** → http://localhost:3000
   - Fill form → Submit → Copy Workflow ID

2. **Monitor Workflow** → http://localhost:8233
   - See workflow progress in real-time

3. **Review Loan** → http://localhost:3000 (Review tab)
   - Paste Workflow ID → Fetch Details → Approve/Reject

4. **View All** → http://localhost:3000 (All Workflows tab)
   - Click Refresh → See all applications

---

## Stopping the Application

Press `Ctrl+C` in each tab (reverse order):
1. Tab 5 (Frontend)
2. Tab 4 (Backend)
3. Tab 3 (Worker)
4. Mockoon (Stop button)
5. Tab 1 (Temporal)

---

## Common Issues Quick Fix

| Issue | Quick Fix |
|-------|-----------|
| "Module not found" | `.venv\Scripts\activate` then `pip install -r requirements.txt` |
| "Port in use" | `netstat -ano \| findstr :8000` then `taskkill /PID <PID> /F` |
| "AWS credentials" | Check `.env` file has real credentials |
| "Temporal connection" | Make sure Tab 1 is running |
| "Frontend error" | `cd frontend` → `npm install` → `npm run dev` |

---

## Test Data Examples

### Good Applicant (Should Approve)
```
ID: 11111
Name: Bob Perfect
Amount: 20000
Income: 15000
Expenses: 4000
```

### Risky Applicant (Should Reject)
```
ID: 99999
Name: Jane Risk
Amount: 100000
Income: 3000
Expenses: 2800
```

### Borderline Case
```
ID: 55555
Name: Alice Maybe
Amount: 40000
Income: 6000
Expenses: 3500
```

---

## VS Code Tips

- **Split Terminal**: Right-click terminal tab → "Split Terminal"
- **Toggle Terminal**: `` Ctrl+` ``
- **Switch Tabs**: `Ctrl+PageUp/PageDown`
- **Select Python Interpreter**: `Ctrl+Shift+P` → "Python: Select Interpreter"

---

## File Structure Quick Reference

```
├── backend/
│   ├── main.py              # FastAPI app
│   ├── workflows.py         # Temporal workflows
│   ├── activities.py        # Temporal activities
│   ├── worker.py           # Temporal worker
│   └── classes/agents/
│       ├── bedrock_agent.py # LangChain agents
│       └── mcp_tools.py     # MCP tools
├── frontend/
│   ├── app/page.tsx        # Main page
│   └── components/         # React components
├── mockoon/
│   └── bankAPI.json        # Mock API config
├── .env                    # Your credentials (create this!)
└── requirements.txt        # Python packages
```

---

## Need Help?

1. Check **VSCODE_TESTING_GUIDE.md** for detailed steps
2. Check **README.md** for architecture details
3. Check logs in terminal tabs
4. Check Temporal UI (http://localhost:8233)
5. Check browser console (F12)

---

**Quick Start**: Follow VSCODE_TESTING_GUIDE.md from Step 1!
