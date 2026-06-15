# NoticeFlow Deployment in VS Code Terminal

## 1️⃣ OPEN VS CODE TERMINAL

In VS Code:
- Press: `Ctrl + ` (backtick)
- Or: Menu → Terminal → New Terminal

You'll see a PowerShell prompt at the bottom:
```
PS C:\Users\ok\Downloads\NoticeFlow >
```

---

## 2️⃣ RUN AUTOMATED DEPLOYMENT SCRIPT

**Paste this command:**

```powershell
.\deploy.ps1
```

Press Enter.

**What it does:**
- ✓ Initializes git
- ✓ Stages all files
- ✓ Commits code
- ✓ Checks GitHub remote
- ✓ Asks for GitHub username
- ✓ Pushes to GitHub

**Output will show:**
```
==================================================
NoticeFlow Deployment Script (PowerShell)
==================================================

[1/6] Verifying prerequisites...
✓ Git found
✓ All required files present

[2/6] Setting up Git repository...
✓ Git already initialized

[3/6] Verifying .gitignore...
✓ .gitignore correctly excludes secrets.toml

[4/6] Committing code to Git...
✓ Code committed to git

[5/6] Git remote status...
❌ Remote 'origin' not configured

Enter your GitHub username: [TYPE YOUR USERNAME]
```

---

## 3️⃣ WHEN PROMPTED: ENTER GITHUB USERNAME

**It will ask:**
```
Enter your GitHub username: 
```

Type your actual GitHub username (example: `johndoe`) and press Enter.

Script will:
```
Adding remote: git@github.com:johndoe/noticeflow.git
✓ Code pushed to GitHub
```

---

## 4️⃣ FOLLOW THE NEXT STEPS (Manual, in Browser)

Script displays:

```
==================================================
NEXT STEPS (Manual in Web Browser):
==================================================

1. Go to: https://share.streamlit.io
   - Sign up with GitHub
   - Authorize Streamlit app

2. Click 'Create app'
   - GitHub Account: [Your username]
   - Repository: noticeflow
   - Branch: main
   - Main file path: app.py

3. Wait for deployment (2-3 minutes)
   - Watch build logs
   - App goes live automatically

4. Add Secrets (CRITICAL):
   - Go to app settings → Secrets
   - Paste:

OPENAI_API_KEY = "sk-xxxxxxxx"
AZURE_DOCUMENT_INTELLIGENCE_KEY = "xxxxxxxx"
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = "https://xxxxx.api.cognitive.microsoft.com/"

   - Replace with your actual keys
   - Click Save

5. Refresh app and test:
   - Upload a test PDF
   - Verify processing works

6. Share live URL:
   - https://[YOUR_USERNAME]-noticeflow.streamlit.app

==================================================
✓ Git setup complete
✓ Ready for Streamlit Cloud deployment
==================================================
```

---

## 5️⃣ MANUAL STEPS IN BROWSER (Can't automate)

### Step 5A: Create Streamlit App

1. Go to: **https://share.streamlit.io**
2. Click: **"Sign up with GitHub"**
3. Authorize Streamlit
4. Click: **"Create app"**
5. Fill in:
   - GitHub Account: **YOUR_USERNAME** (from script)
   - Repository: **noticeflow**
   - Branch: **main**
   - Main file path: **app.py**
6. Click: **"Deploy"**
7. **Wait 2-3 minutes** ⏳

---

### Step 5B: Add API Keys

**Get keys:**
1. OpenAI: https://platform.openai.com/api/keys → Create key
2. Azure (optional): https://portal.azure.com → Document Intelligence

**Add to Streamlit:**
1. Go to: https://share.streamlit.io
2. Click your app: **noticeflow**
3. Click **⋯** (three dots) → **Settings**
4. Click **"Secrets"**
5. Paste (replace with YOUR keys):

```toml
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxx"
AZURE_DOCUMENT_INTELLIGENCE_KEY = "xxxxxxxxxxxxxxxxxxxx"
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = "https://eastus.api.cognitive.microsoft.com/"
```

6. Click **"Save"**
7. **Wait 30 seconds, then refresh**

---

### Step 5C: Test Live

1. Go to: **https://YOUR_USERNAME-noticeflow.streamlit.app**
2. Upload a tax notice PDF
3. ✓ It processes (20-30 seconds)
4. ✓ Shows deadline + explanation + checklist

---

## ⚡ ALL-IN-ONE QUICK REFERENCE

**In VS Code Terminal:**

```powershell
# Copy entire block and paste into terminal at once:

cd c:\Users\ok\Downloads\NoticeFlow
.\deploy.ps1
```

Then:
1. Type your GitHub username when asked
2. Go to browser → https://share.streamlit.io
3. Create app from noticeflow repo
4. Add secrets
5. Done ✓

---

## 🔧 IF SCRIPT FAILS: MANUAL COMMANDS

If `.\deploy.ps1` doesn't work, run these commands one-by-one in VS Code terminal:

```powershell
# Initialize git
git init

# Configure git
git config user.name "NoticeFlow Developer"
git config user.email "developer@noticeflow.local"

# Stage files
git add .

# Commit
git commit -m "NoticeFlow MVP: Deploy to Streamlit Cloud"

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin git@github.com:YOUR_USERNAME/noticeflow.git

# Push to GitHub
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## 📝 TERMINAL TIPS

**See current status:**
```powershell
git status
```

**See commit history:**
```powershell
git log --oneline
```

**See remote:**
```powershell
git remote -v
```

**Clear terminal:**
```powershell
Clear-Host
```

---

## ✅ DONE WHEN YOU SEE

In VS Code terminal:
```
✓ Code committed to git
✓ Code pushed to GitHub
✓ Ready for Streamlit Cloud deployment
```

Plus app is live at: **https://YOUR_USERNAME-noticeflow.streamlit.app**

---

## 🚀 START NOW

**Copy & paste into VS Code terminal:**

```powershell
.\deploy.ps1
```

Takes 12 minutes total. 🎯
