# Windows Setup Guide - Step by Step

## 🪟 Complete Setup for Windows

### Step 1: Check Python Installation

```powershell
# Check if Python is installed
python --version

# Should show Python 3.8 or higher
# If not installed, download from: https://www.python.org/downloads/
```

### Step 2: Navigate to Backend Directory

```powershell
# Open PowerShell and navigate to your project
cd path\to\your\project\backend

# Example:
# cd C:\Users\YourName\Documents\bharat-content-ai\backend
```

### Step 3: Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# This creates a 'venv' folder in your backend directory
```

### Step 4: Activate Virtual Environment

```powershell
# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# If you get an error about execution policy, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again:
.\venv\Scripts\Activate.ps1

# You should see (venv) at the start of your prompt:
# (venv) PS C:\...\backend>
```

### Step 5: Install Dependencies

```powershell
# Make sure you're in the backend directory with (venv) active
pip install -r requirements.txt

# This will install all required packages including uvicorn
# Wait for installation to complete (may take a few minutes)
```

### Step 6: Create .env File

```powershell
# Create .env file from example
Copy-Item .env.example .env

# Open .env file in notepad
notepad .env

# Add your API key (replace the placeholder):
# GEMINI_API_KEY=your_actual_api_key_here

# Save and close notepad
```

### Step 7: Initialize Database

```powershell
# Still in backend directory with (venv) active
python -c "from app.config.database import init_db; init_db()"

# You should see: ✓ Database tables created successfully!
```

### Step 8: Start the Server

```powershell
# Start the FastAPI server
uvicorn app.main:app --reload

# You should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete.
```

### Step 9: Test the API (Open New PowerShell Window)

```powershell
# Open a NEW PowerShell window (keep the server running in the first one)

# Test 1: Check if server is running
curl http://localhost:8000/

# Test 2: Check AI services status
curl http://localhost:8000/api/content/ai-services/status

# Test 3: Open in browser
start http://localhost:8000/api/docs
```

---

## 🔧 Troubleshooting

### Issue 1: "uvicorn not recognized"

**Problem:** Virtual environment not activated or dependencies not installed

**Solution:**
```powershell
# Make sure you're in backend directory
cd backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Verify it's activated (should see (venv) in prompt)
# If still not working, reinstall:
pip install uvicorn
```

### Issue 2: "Execution Policy" Error

**Problem:** PowerShell script execution is disabled

**Solution:**
```powershell
# Run as Administrator or use:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating venv again
.\venv\Scripts\Activate.ps1
```

### Issue 3: "Python not found"

**Problem:** Python not installed or not in PATH

**Solution:**
1. Download Python from https://www.python.org/downloads/
2. During installation, CHECK "Add Python to PATH"
3. Restart PowerShell
4. Verify: `python --version`

### Issue 4: "Module not found" errors

**Problem:** Dependencies not installed

**Solution:**
```powershell
# Activate venv first
.\venv\Scripts\Activate.ps1

# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue 5: "Port already in use"

**Problem:** Another process is using port 8000

**Solution:**
```powershell
# Use a different port
uvicorn app.main:app --reload --port 8001

# Or find and kill the process using port 8000
netstat -ano | findstr :8000
# Note the PID and kill it:
taskkill /PID <PID> /F
```

---

## 📋 Quick Command Reference

### Starting Development

```powershell
# 1. Navigate to backend
cd backend

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Start server
uvicorn app.main:app --reload
```

### Stopping Development

```powershell
# 1. Stop server (in server window)
Ctrl + C

# 2. Deactivate virtual environment
deactivate
```

### Running Tests

```powershell
# In a new PowerShell window (with server running)
cd backend
.\venv\Scripts\Activate.ps1
cd ..
python test_api.py
```

---

## 🎯 Complete Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Navigated to backend directory
- [ ] Created virtual environment (`python -m venv venv`)
- [ ] Activated virtual environment (`.\venv\Scripts\Activate.ps1`)
- [ ] Installed dependencies (`pip install -r requirements.txt`)
- [ ] Created .env file (`Copy-Item .env.example .env`)
- [ ] Added API key to .env file
- [ ] Initialized database (`python -c "from app.config.database import init_db; init_db()"`)
- [ ] Started server (`uvicorn app.main:app --reload`)
- [ ] Tested API (opened http://localhost:8000/api/docs)

---

## 🚀 After Setup

Once everything is running:

1. **API Documentation:** http://localhost:8000/api/docs
2. **Check AI Services:** http://localhost:8000/api/content/ai-services/status
3. **Test Content Generation:** Use Swagger UI to test endpoints

---

## 💡 Pro Tips

1. **Always activate venv** before running commands
2. **Keep server window open** while developing
3. **Use separate PowerShell windows** for server and testing
4. **Check .env file** if services aren't detected
5. **Restart server** after changing .env file

---

## 🆘 Still Having Issues?

If you're still stuck, share:
1. The exact error message
2. Which step you're on
3. Output of `python --version`
4. Output of `pip list` (after activating venv)

I'll help you troubleshoot!
