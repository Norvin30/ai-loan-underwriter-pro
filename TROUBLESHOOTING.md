# 🔧 Troubleshooting Guide

Common issues and their solutions when testing the AI-Powered Loan Underwriter in VS Code.

---

## 🐍 Python Issues

### Issue: "Python not found" or "python is not recognized"

**Symptoms**: 
```
'python' is not recognized as an internal or external command
```

**Solutions**:
1. **Check Python installation**:
   ```powershell
   python --version
   py --version
   ```

2. **Reinstall Python**:
   - Download from https://python.org/downloads/
   - **IMPORTANT**: Check "Add Python to PATH" during installation
   - Restart VS Code after installation

3. **Use `py` instead of `python`**:
   ```powershell
   py -m venv .venv
   ```

---

### Issue: "Module not found" or "No module named 'X'"

**Symptoms**:
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solutions**:
1. **Activate virtual environment**:
   ```powershell
   .venv\Scripts\activate
   # You should see (.venv) in your prompt
   ```

2. **Reinstall dependencies**:
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Check Python interpreter in VS Code**:
   - Press `Ctrl+Shift+P`
   - Type: "Python: Select Interpreter"
   - Choose: `.venv\Scripts\python.exe`

4. **Verify installation**:
   ```powershell
   pip list
   ```

---

### Issue: "Virtual environment activation fails"

**Symptoms**:
```
.venv\Scripts\activate : File cannot be loaded because running scripts is disabled
```

**Solution** (PowerShell execution policy):
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again
.venv\Scripts\activate
```

---

## 🌐 Node.js / Frontend Issues

### Issue: "npm not found" or "node not found"

**Symptoms**:
```
'npm' is not recognized as an internal or external command
```

**Solutions**:
1. **Install Node.js**:
   - Download from https://nodejs.org/
   - Install LTS version
   - Restart VS Code

2. **Verify installation**:
   ```powershell
   node --version
   npm --version
   ```

---

### Issue: "npm install fails" or "dependency errors"

**Symptoms**:
```
npm ERR! code ERESOLVE
npm ERR! ERESOLVE unable to resolve dependency tree
```

**Solutions**:
1. **Clear npm cache**:
   ```powershell
   cd frontend
   npm cache clean --force
   ```

2. **Delete node_modules and reinstall**:
   ```powershell
   cd frontend
   rmdir /s /q node_modules
   del package-lock.json
   npm install
   ```

3. **Use legacy peer deps** (if still failing):
   ```powershell
   npm install --legacy-peer-deps
   ```

---

### Issue: "Frontend won't start" or "Port 3000 already in use"

**Symptoms**:
```
Error: listen EADDRINUSE: address already in use :::3000
```

**Solutions**:
1. **Find and kill process using port 3000**:
   ```powershell
   # Find process
   netstat -ano | findstr :3000
   
   # Kill process (replace 1234 with actual PID)
   taskkill /PID 1234 /F
   ```

2. **Use different port**:
   ```powershell
   # Edit frontend/package.json
   # Change: "dev": "next dev"
   # To: "dev": "next dev -p 3001"
   ```

3. **Clear Next.js cache**:
   ```powershell
   cd frontend
   rmdir /s /q .next
   npm run dev
   ```

---

## ☁️ AWS / Bedrock Issues

### Issue: "AWS credentials not found"

**Symptoms**:
```
botocore.exceptions.NoCredentialsError: Unable to locate credentials
```

**Solutions**:
1. **Check .env file exists**:
   ```powershell
   # Make sure you have .env (not .env.example)
   dir .env
   ```

2. **Verify .env content**:
   ```env
   AWS_REGION=us-east-1
   AWS_ACCESS_KEY_ID=AKIA...  (your actual key)
   AWS_SECRET_ACCESS_KEY=wJalr...  (your actual secret)
   ```

3. **Test AWS credentials**:
   ```powershell
   # Install AWS CLI if not installed
   pip install awscli
   
   # Configure credentials
   aws configure
   
   # Test connection
   aws bedrock list-foundation-models --region us-east-1
   ```

4. **Restart backend** after fixing .env:
   ```powershell
   # In Backend tab (Tab 4)
   # Press Ctrl+C to stop
   # Then restart:
   uvicorn backend.main:app --reload --port 8000
   ```

---

### Issue: "Bedrock model not accessible" or "AccessDeniedException"

**Symptoms**:
```
botocore.exceptions.ClientError: An error occurred (AccessDeniedException) when calling the InvokeModel operation
```

**Solutions**:
1. **Enable models in AWS Console**:
   - Go to https://console.aws.amazon.com/bedrock/
   - Click "Model access" in left sidebar
   - Click "Manage model access"
   - Enable:
     - ✅ Anthropic Claude 3.5 Sonnet v2
     - ✅ Amazon Nova Pro
   - Click "Save changes"
   - Wait for status to show "Access granted"

2. **Check IAM permissions**:
   - Go to IAM → Users → Your user
   - Ensure you have `bedrock:InvokeModel` permission
   - Or attach policy: `AmazonBedrockFullAccess`

3. **Verify model IDs in .env**:
   ```env
   BEDROCK_MODEL_CLAUDE=anthropic.claude-3-5-sonnet-20241022-v2:0
   BEDROCK_MODEL_NOVA=amazon.nova-pro-v1:0
   ```

4. **Test model access**:
   ```powershell
   aws bedrock get-foundation-model --model-identifier anthropic.claude-3-5-sonnet-20241022-v2:0 --region us-east-1
   ```

---

### Issue: "Bedrock throttling" or "Rate limit exceeded"

**Symptoms**:
```
botocore.exceptions.ClientError: An error occurred (ThrottlingException)
```

**Solutions**:
1. **Wait and retry** - AWS has rate limits
2. **Request quota increase** in AWS Console
3. **Add retry logic** (already implemented in the code)
4. **Use different models** to distribute load

---

## ⏱️ Temporal Issues

### Issue: "Temporal CLI not found"

**Symptoms**:
```
'temporal' is not recognized as an internal or external command
```

**Solutions**:
1. **Install Temporal CLI**:
   - Download from https://github.com/temporalio/cli/releases
   - Extract `temporal.exe`
   - Add to PATH or move to `C:\Windows\System32\`

2. **Verify installation**:
   ```powershell
   temporal --version
   ```

3. **Restart VS Code** after installation

---

### Issue: "Temporal server won't start"

**Symptoms**:
```
Error: unable to start server
```

**Solutions**:
1. **Check port 7233 is free**:
   ```powershell
   netstat -ano | findstr :7233
   ```

2. **Kill process if port is in use**:
   ```powershell
   taskkill /PID <PID> /F
   ```

3. **Try starting with different port**:
   ```powershell
   temporal server start-dev --port 7234
   # Then update .env: TEMPORAL_ADDRESS=localhost:7234
   ```

4. **Check for Docker conflicts** (if you have Docker running)

---

### Issue: "Worker can't connect to Temporal"

**Symptoms**:
```
temporalio.exceptions.TemporalError: Failed to connect to Temporal server
```

**Solutions**:
1. **Ensure Temporal server is running** (Tab 1):
   ```powershell
   temporal server start-dev
   ```

2. **Check Temporal UI** is accessible:
   - Open http://localhost:8233
   - Should see Temporal Web UI

3. **Verify connection in code**:
   ```python
   # In backend/worker.py, check:
   client = await Client.connect("localhost:7233")
   ```

4. **Restart worker** after Temporal is running

---

### Issue: "Workflow not found" or "Workflow execution failed"

**Symptoms**:
```
temporalio.exceptions.WorkflowNotFoundError
```

**Solutions**:
1. **Check worker is running** (Tab 3)
2. **Verify task queue name matches**:
   - In `.env`: `TEMPORAL_TASK_QUEUE=loan-underwriter-queue`
   - In `worker.py`: Same queue name
3. **Check Temporal UI** for workflow status
4. **Look at worker logs** for errors

---

## 🔌 Port Issues

### Issue: "Port already in use"

**Symptoms**:
```
Error: listen EADDRINUSE: address already in use
```

**Solutions**:

#### For any port (8000, 3000, 7233, 3233):

1. **Find process using the port**:
   ```powershell
   netstat -ano | findstr :8000
   # Replace 8000 with your port number
   ```

2. **Kill the process**:
   ```powershell
   taskkill /PID <PID> /F
   # Replace <PID> with the number from previous command
   ```

3. **Or use different port**:
   - Backend: `uvicorn backend.main:app --reload --port 8001`
   - Frontend: Edit `package.json` → `"dev": "next dev -p 3001"`
   - Temporal: `temporal server start-dev --port 7234`

---

## 🎭 Mockoon Issues

### Issue: "Mockoon won't start" or "Port 3233 in use"

**Solutions**:
1. **Check if another Mockoon instance is running**
2. **Change port in Mockoon**:
   - Click on environment settings
   - Change port from 3233 to 3234
   - Update `.env`: `MOCK_API_BASE=http://localhost:3234`

3. **Restart Mockoon**

---

### Issue: "Mock API returns 404"

**Solutions**:
1. **Verify Mockoon is running** (green status)
2. **Check routes are configured**:
   - Should have: `/bank`, `/documents`, `/cibil`, `/experian`
3. **Re-import configuration**:
   - File → Import → Select `mockoon/bankAPI.json`

---

## 🌐 Network / API Issues

### Issue: "CORS errors in browser"

**Symptoms**:
```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solutions**:
1. **Check CORS is enabled in backend**:
   ```python
   # In backend/main.py
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3000"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Restart backend** after changes

---

### Issue: "API calls fail" or "Network error"

**Solutions**:
1. **Check backend is running** (Tab 4)
2. **Verify URL is correct**:
   - Backend: `http://localhost:8000`
   - Frontend: `http://localhost:3000`
3. **Check browser console** (F12) for errors
4. **Test API directly**:
   - Go to http://localhost:8000/docs
   - Try endpoints in Swagger UI

---

## 🖥️ VS Code Issues

### Issue: "Terminal not working" or "Commands not found"

**Solutions**:
1. **Change default shell**:
   - Press `Ctrl+Shift+P`
   - Type: "Terminal: Select Default Profile"
   - Choose: "Command Prompt" or "PowerShell"

2. **Restart VS Code**

3. **Open new terminal**:
   - Close all terminals
   - Open new one: `` Ctrl+` ``

---

### Issue: "Python extension not working"

**Solutions**:
1. **Reinstall Python extension**:
   - Extensions → Python → Uninstall
   - Restart VS Code
   - Reinstall Python extension

2. **Reload window**:
   - Press `Ctrl+Shift+P`
   - Type: "Developer: Reload Window"

---

## 🔍 Debugging Tips

### How to check if services are running:

```powershell
# Check Temporal
curl http://localhost:8233

# Check Backend
curl http://localhost:8000/docs

# Check Frontend
curl http://localhost:3000

# Check Mockoon
curl http://localhost:3233/bank?applicant_id=12345
```

### How to view detailed logs:

1. **Backend logs**: Check Tab 4 in VS Code
2. **Worker logs**: Check Tab 3 in VS Code
3. **Frontend logs**: Check Tab 5 in VS Code
4. **Browser logs**: Press F12 → Console tab
5. **Temporal logs**: Go to http://localhost:8233

### How to test individual components:

1. **Test AWS Bedrock**:
   ```python
   # Create test.py
   import boto3
   client = boto3.client('bedrock-runtime', region_name='us-east-1')
   response = client.invoke_model(
       modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
       body='{"prompt": "Hello", "max_tokens": 100}'
   )
   print(response)
   ```

2. **Test Temporal**:
   ```powershell
   temporal workflow list
   ```

3. **Test Backend**:
   - Go to http://localhost:8000/docs
   - Try POST /submit endpoint

---

## 🆘 Still Having Issues?

### Checklist before asking for help:

- [ ] All prerequisites installed (Python, Node.js, Temporal CLI, Mockoon)
- [ ] Virtual environment activated
- [ ] All dependencies installed
- [ ] .env file created with real AWS credentials
- [ ] Bedrock models enabled in AWS Console
- [ ] All 5 services started in correct order
- [ ] No port conflicts
- [ ] Checked all terminal tabs for errors
- [ ] Checked browser console (F12) for errors
- [ ] Restarted VS Code
- [ ] Restarted computer (sometimes helps!)

### Collect this information:

1. **Error message** (full text)
2. **Which step** you're on
3. **Which terminal tab** shows the error
4. **Screenshots** of the error
5. **Your environment**:
   ```powershell
   python --version
   node --version
   npm --version
   temporal --version
   ```

### Where to get help:

1. Check **VSCODE_TESTING_GUIDE.md** for detailed steps
2. Check **README.md** for architecture details
3. Check **QUICK_REFERENCE.md** for commands
4. Search error message on Google/Stack Overflow
5. Check AWS Bedrock documentation
6. Check Temporal documentation

---

## 💡 Prevention Tips

1. **Always activate virtual environment** before running Python commands
2. **Keep all 5 terminal tabs open** while testing
3. **Don't close terminals** until you're done testing
4. **Save your .env file** - don't lose your AWS credentials
5. **Check logs regularly** - catch errors early
6. **Use Temporal UI** - great for debugging workflows
7. **Test incrementally** - don't skip steps
8. **Keep VS Code updated**
9. **Keep Python/Node.js updated**
10. **Restart services** if something feels off

---

**Remember**: Most issues are simple fixes! Check the basics first (services running, credentials correct, ports free). 🚀
