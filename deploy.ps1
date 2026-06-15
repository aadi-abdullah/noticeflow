# NoticeFlow MVP → Streamlit Cloud Deployment (PowerShell)
# Run this script from the project root directory

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "NoticeFlow Deployment Script (PowerShell)" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# ============================================================
# STEP 1: Verify Prerequisites
# ============================================================
Write-Host ""
Write-Host "[1/6] Verifying prerequisites..." -ForegroundColor Yellow

# Check if git is installed
try {
    git --version | Out-Null
    Write-Host "✓ Git found" -ForegroundColor Green
}
catch {
    Write-Host "❌ Git not found. Install from: https://git-scm.com/download" -ForegroundColor Red
    exit 1
}

# Check if required files exist
$requiredFiles = @("app.py", "process_notice.py", "requirements.txt")
foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "❌ Missing: $file" -ForegroundColor Red
        exit 1
    }
}
Write-Host "✓ All required files present" -ForegroundColor Green

# ============================================================
# STEP 2: Initialize Git (if needed)
# ============================================================
Write-Host ""
Write-Host "[2/6] Setting up Git repository..." -ForegroundColor Yellow

if (-not (Test-Path ".git")) {
    Write-Host "Initializing git repo..."
    git init
    git config user.name "NoticeFlow Developer"
    git config user.email "developer@noticeflow.local"
    Write-Host "✓ Git initialized" -ForegroundColor Green
}
else {
    Write-Host "✓ Git already initialized" -ForegroundColor Green
}

# ============================================================
# STEP 3: Verify .gitignore
# ============================================================
Write-Host ""
Write-Host "[3/6] Verifying .gitignore..." -ForegroundColor Yellow

if (Test-Path ".gitignore") {
    $gitignore = Get-Content ".gitignore" -Raw
    if ($gitignore -match "\.streamlit/secrets\.toml") {
        Write-Host "✓ .gitignore correctly excludes secrets.toml" -ForegroundColor Green
    }
    else {
        Write-Host "⚠ Adding .streamlit/secrets.toml to .gitignore" -ForegroundColor Yellow
        Add-Content ".gitignore" ".streamlit/secrets.toml"
    }
}
else {
    Write-Host "⚠ Creating .gitignore" -ForegroundColor Yellow
    @"
.streamlit/secrets.toml
venv/
__pycache__/
*.pyc
.env
.DS_Store
"@ | Out-File ".gitignore" -Encoding UTF8
}

# ============================================================
# STEP 4: Stage and Commit
# ============================================================
Write-Host ""
Write-Host "[4/6] Committing code to Git..." -ForegroundColor Yellow

git add .

# Check if there are changes to commit
$status = git status --short
if ($status) {
    git commit -m "NoticeFlow MVP: Deploy to Streamlit Cloud

- Streamlit UI with notice upload interface
- GPT-4o parsing engine with structured output
- Multi-fallback OCR chain (Azure/PyPDF2/GPT-4o Vision)
- Document checklist generator with section-specific mapping
- Deadline extraction and urgency color coding
- Production-ready error handling and logging

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
    Write-Host "✓ Code committed to git" -ForegroundColor Green
}
else {
    Write-Host "✓ No new changes to commit (already up to date)" -ForegroundColor Green
}

# ============================================================
# STEP 5: Check Remote
# ============================================================
Write-Host ""
Write-Host "[5/6] Git remote status..." -ForegroundColor Yellow

$remotes = git remote
if ($remotes -match "origin") {
    $remoteUrl = git config --get remote.origin.url
    Write-Host "✓ Remote 'origin' already configured: $remoteUrl" -ForegroundColor Green
    Write-Host ""
    Write-Host "To push code to GitHub:" -ForegroundColor Cyan
    Write-Host "  git push -u origin main" -ForegroundColor White
}
else {
    Write-Host "❌ Remote 'origin' not configured" -ForegroundColor Red
    Write-Host ""
    Write-Host "You need to:" -ForegroundColor Cyan
    Write-Host "  1. Create repo at: https://github.com/new" -ForegroundColor White
    Write-Host "  2. Name it: 'noticeflow' (make it PUBLIC)" -ForegroundColor White
    Write-Host "  3. Do NOT initialize with README" -ForegroundColor White
    Write-Host "  4. Copy the SSH URL (or HTTPS)" -ForegroundColor White
    Write-Host "  5. Run: git remote add origin [REPO-URL]" -ForegroundColor White
    Write-Host "  6. Run: git branch -M main" -ForegroundColor White
    Write-Host "  7. Run: git push -u origin main" -ForegroundColor White
    Write-Host ""
    $username = Read-Host "Enter your GitHub username"
    $repoUrl = "git@github.com:$username/noticeflow.git"
    
    Write-Host "Adding remote: $repoUrl" -ForegroundColor Yellow
    git remote add origin $repoUrl
    git branch -M main
    git push -u origin main
    Write-Host "✓ Code pushed to GitHub" -ForegroundColor Green
}

# ============================================================
# STEP 6: Display Streamlit Deployment Instructions
# ============================================================
Write-Host ""
Write-Host "[6/6] Streamlit Cloud Deployment Instructions" -ForegroundColor Yellow
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "NEXT STEPS (Manual in Web Browser):" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to: https://share.streamlit.io" -ForegroundColor White
Write-Host "   - Sign up with GitHub" -ForegroundColor White
Write-Host "   - Authorize Streamlit app" -ForegroundColor White
Write-Host ""
Write-Host "2. Click 'Create app'" -ForegroundColor White
Write-Host "   - GitHub Account: [Your username]" -ForegroundColor White
Write-Host "   - Repository: noticeflow" -ForegroundColor White
Write-Host "   - Branch: main" -ForegroundColor White
Write-Host "   - Main file path: app.py" -ForegroundColor White
Write-Host ""
Write-Host "3. Wait for deployment (2-3 minutes)" -ForegroundColor White
Write-Host "   - Watch build logs" -ForegroundColor White
Write-Host "   - App goes live automatically" -ForegroundColor White
Write-Host ""
Write-Host "4. Add Secrets (CRITICAL):" -ForegroundColor White
Write-Host "   - Go to app settings → Secrets" -ForegroundColor White
Write-Host "   - Paste:" -ForegroundColor White
Write-Host ""
Write-Host "OPENAI_API_KEY = ""sk-xxxxxxxx""" -ForegroundColor Cyan
Write-Host "AZURE_DOCUMENT_INTELLIGENCE_KEY = ""xxxxxxxx""" -ForegroundColor Cyan
Write-Host "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = ""https://xxxxx.api.cognitive.microsoft.com/""" -ForegroundColor Cyan
Write-Host ""
Write-Host "   - Replace with your actual keys" -ForegroundColor White
Write-Host "   - Click Save" -ForegroundColor White
Write-Host ""
Write-Host "5. Refresh app and test:" -ForegroundColor White
Write-Host "   - Upload a test PDF" -ForegroundColor White
Write-Host "   - Verify processing works" -ForegroundColor White
Write-Host ""
Write-Host "6. Share live URL:" -ForegroundColor White
Write-Host "   - https://[YOUR_USERNAME]-noticeflow.streamlit.app" -ForegroundColor White
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "✓ Git setup complete" -ForegroundColor Green
Write-Host "✓ Ready for Streamlit Cloud deployment" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
