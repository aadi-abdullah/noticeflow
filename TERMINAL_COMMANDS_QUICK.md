# NoticeFlow Deployment: Terminal Commands (Quick Reference)

## For Windows (PowerShell)

### Option 1: Automated Script (Recommended)

```powershell
# Navigate to project folder
cd c:\Users\ok\Downloads\NoticeFlow

# Run deployment script
.\deploy.ps1
```

This runs all steps automatically, then shows next steps.

---

### Option 2: Manual Commands (Step-by-Step)

```powershell
# 1. Initialize git
cd c:\Users\ok\Downloads\NoticeFlow
git init
git config user.name "NoticeFlow Developer"
git config user.email "developer@noticeflow.local"

# 2. Stage all files
git add .

# 3. Commit
git commit -m "NoticeFlow MVP: Deploy to Streamlit Cloud

- Streamlit UI with notice upload interface
- GPT-4o parsing engine with structured output
- Multi-fallback OCR chain (Azure/PyPDF2/GPT-4o Vision)
- Document checklist generator with section-specific mapping
- Deadline extraction and urgency color coding
- Production-ready error handling and logging

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

# 4. Add GitHub remote (replace YOUR_USERNAME)
git remote add origin git@github.com:YOUR_USERNAME/noticeflow.git

# 5. Push to GitHub
git branch -M main
git push -u origin main
```

---

### Option 3: HTTPS Instead of SSH (If SSH doesn't work)

```powershell
# Use HTTPS instead of SSH
git remote add origin https://github.com/YOUR_USERNAME/noticeflow.git
git branch -M main
git push -u origin main

# When prompted, enter GitHub username and personal access token (not password)
# Personal token: https://github.com/settings/tokens
```

---

## For Mac/Linux (Bash)

### Option 1: Automated Script

```bash
cd ~/path/to/NoticeFlow
chmod +x deploy.sh
./deploy.sh
```

---

### Option 2: Manual Commands

```bash
cd ~/path/to/NoticeFlow

# Initialize git
git init
git config user.name "NoticeFlow Developer"
git config user.email "developer@noticeflow.local"

# Stage and commit
git add .
git commit -m "NoticeFlow MVP: Deploy to Streamlit Cloud

- Streamlit UI with notice upload interface
- GPT-4o parsing engine with structured output
- Multi-fallback OCR chain (Azure/PyPDF2/GPT-4o Vision)
- Document checklist generator
- Deadline extraction and urgency color coding
- Production-ready error handling and logging

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

# Add remote
git remote add origin git@github.com:YOUR_USERNAME/noticeflow.git

# Push
git branch -M main
git push -u origin main
```

---

## All-In-One One-Liner (PowerShell)

```powershell
cd c:\Users\ok\Downloads\NoticeFlow; git init; git config user.name "NoticeFlow Developer"; git config user.email "developer@noticeflow.local"; git add .; git commit -m "NoticeFlow MVP: Deploy to Streamlit Cloud"; Read-Host "Create GitHub repo at https://github.com/new (name: noticeflow, PUBLIC, no README). Press Enter when done"; $u = Read-Host "GitHub username"; git remote add origin "git@github.com:$u/noticeflow.git"; git branch -M main; git push -u origin main; Write-Host "✓ Pushed to GitHub. Next: https://share.streamlit.io"
```

---

## After Git Push: Streamlit Cloud Setup (Web Browser)

Once code is on GitHub, you must do this in browser (can't automate):

### 1. Deploy on Streamlit Cloud

```
1. Go: https://share.streamlit.io
2. Sign up with GitHub
3. Authorize Streamlit
4. Click "Create app"
5. Select:
   - GitHub account: [YOUR_USERNAME]
   - Repository: noticeflow
   - Branch: main
   - Main file path: app.py
6. Click "Deploy"
7. Wait 2-3 minutes for build to complete
```

---

### 2. Add Secrets (Critical)

After app is live:

```
1. Go: https://share.streamlit.io/[YOUR_USERNAME]/noticeflow
2. Click three dots (•••) → Settings
3. Click "Secrets"
4. Paste:

OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxx"
AZURE_DOCUMENT_INTELLIGENCE_KEY = "xxxxxxxxxxxxxxxxxxxx"
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = "https://eastus.api.cognitive.microsoft.com/"

5. Replace with your actual keys (from OpenAI + Azure portals)
6. Click "Save"
7. Wait 30 seconds and refresh app
```

---

### 3. Get API Keys

#### OpenAI API Key
```
Go: https://platform.openai.com/api/keys
Click: Create new secret key
Copy immediately (won't show again)
```

#### Azure Document Intelligence (Optional)
```
Go: https://portal.azure.com
Search: Document Intelligence
Create resource → copy Endpoint + Primary Key
```

---

## Quick Verification

### Check Git Status
```powershell
git status
git log --oneline
git remote -v
```

### Check Files Committed
```powershell
git ls-files
```

### Check Secrets NOT Committed
```powershell
# This should return NOTHING (secrets not in history)
git log --all --full-history -p -- ".streamlit/secrets.toml"
```

---

## Troubleshooting Commands

### If git push fails: "failed to push some refs"
```powershell
# Pull first, then push
git pull origin main
git push origin main
```

### If git push fails: "host key verification failed"
```powershell
# Add GitHub to known hosts (SSH only)
ssh-keyscan github.com >> ~/.ssh/known_hosts
git push origin main
```

### If git remote is wrong
```powershell
# List current remotes
git remote -v

# Change remote
git remote remove origin
git remote add origin git@github.com:YOUR_USERNAME/noticeflow.git
git push -u origin main
```

### If file permissions wrong (Linux/Mac)
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## Final Result

After all commands:

✓ Git initialized locally  
✓ All files committed  
✓ Code pushed to GitHub  
✓ GitHub repo at: https://github.com/YOUR_USERNAME/noticeflow  
✓ App deployed on: https://YOUR_USERNAME-noticeflow.streamlit.app  
✓ Secrets added via Streamlit dashboard  
✓ Ready for beta testing  

---

## Total Time
- Git setup: 5 minutes
- Streamlit deploy: 5 minutes
- Add secrets: 2 minutes
- **Total: ~12 minutes from terminal to live app**

---

## Next Steps

1. Run the script (or commands above)
2. Open browser → https://share.streamlit.io
3. Create app from noticeflow repo
4. Add secrets
5. Test with real tax notice PDF
6. Share link with beta CAs
7. Collect feedback Week 1-4
8. Go/no-go decision for Phase 2

**See:** DEPLOY_TO_STREAMLIT_CLOUD.md for full context
