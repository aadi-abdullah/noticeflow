#!/bin/bash
# NoticeFlow MVP → Streamlit Cloud Deployment (Fully Automated)
# Run this script from the project root directory

set -e  # Exit on any error

echo "=================================================="
echo "NoticeFlow Deployment Script"
echo "=================================================="

# ============================================================
# STEP 1: Verify Prerequisites
# ============================================================
echo ""
echo "[1/6] Verifying prerequisites..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Install from: https://git-scm.com/download"
    exit 1
fi
echo "✓ Git found"

# Check if required files exist
required_files=("app.py" "process_notice.py" "requirements.txt")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing: $file"
        exit 1
    fi
done
echo "✓ All required files present"

# ============================================================
# STEP 2: Initialize Git (if needed)
# ============================================================
echo ""
echo "[2/6] Setting up Git repository..."

if [ ! -d ".git" ]; then
    echo "Initializing git repo..."
    git init
    git config user.name "NoticeFlow Developer"
    git config user.email "developer@noticeflow.local"
    echo "✓ Git initialized"
else
    echo "✓ Git already initialized"
fi

# ============================================================
# STEP 3: Verify .gitignore
# ============================================================
echo ""
echo "[3/6] Verifying .gitignore..."

if grep -q "\.streamlit/secrets\.toml" .gitignore 2>/dev/null; then
    echo "✓ .gitignore correctly excludes secrets.toml"
else
    echo "⚠ Adding .streamlit/secrets.toml to .gitignore"
    echo ".streamlit/secrets.toml" >> .gitignore
fi

# ============================================================
# STEP 4: Stage and Commit
# ============================================================
echo ""
echo "[4/6] Committing code to Git..."

git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "✓ No new changes to commit (already up to date)"
else
    git commit -m "NoticeFlow MVP: Deploy to Streamlit Cloud

- Streamlit UI with notice upload interface
- GPT-4o parsing engine with structured output
- Multi-fallback OCR chain (Azure/PyPDF2/GPT-4o Vision)
- Document checklist generator with section-specific mapping
- Deadline extraction and urgency color coding
- Production-ready error handling and logging

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
    echo "✓ Code committed to git"
fi

# ============================================================
# STEP 5: Check Remote
# ============================================================
echo ""
echo "[5/6] Git remote status..."

if git remote | grep -q "origin"; then
    REMOTE_URL=$(git config --get remote.origin.url)
    echo "✓ Remote 'origin' already configured: $REMOTE_URL"
    echo ""
    echo "To push code to GitHub:"
    echo "  git push -u origin main"
else
    echo "❌ Remote 'origin' not configured"
    echo ""
    echo "You need to:"
    echo "  1. Create repo at: https://github.com/new"
    echo "  2. Name it: 'noticeflow' (make it PUBLIC)"
    echo "  3. Do NOT init with README"
    echo "  4. Copy the SSH URL"
    echo "  5. Run: git remote add origin [SSH-URL]"
    echo "  6. Run: git branch -M main"
    echo "  7. Run: git push -u origin main"
    echo ""
    read -p "Press Enter after creating GitHub repo..."
    
    read -p "Enter GitHub username: " USERNAME
    REPO_URL="git@github.com:$USERNAME/noticeflow.git"
    
    echo "Adding remote: $REPO_URL"
    git remote add origin "$REPO_URL"
    git branch -M main
    git push -u origin main
    echo "✓ Code pushed to GitHub"
fi

# ============================================================
# STEP 6: Display Streamlit Deployment Instructions
# ============================================================
echo ""
echo "[6/6] Streamlit Cloud Deployment Instructions"
echo ""
echo "=================================================="
echo "NEXT STEPS (Manual in Web Browser):"
echo "=================================================="
echo ""
echo "1. Go to: https://share.streamlit.io"
echo "   - Sign up with GitHub"
echo "   - Authorize Streamlit app"
echo ""
echo "2. Click 'Create app'"
echo "   - GitHub Account: [Your username]"
echo "   - Repository: noticeflow"
echo "   - Branch: main"
echo "   - Main file path: app.py"
echo ""
echo "3. Wait for deployment (2-3 minutes)"
echo "   - Watch build logs"
echo "   - App goes live automatically"
echo ""
echo "4. Add Secrets (CRITICAL):"
echo "   - Go to app settings → Secrets"
echo "   - Paste:"
echo ""
cat << 'EOF'
OPENAI_API_KEY = "sk-xxxxxxxx"
AZURE_DOCUMENT_INTELLIGENCE_KEY = "xxxxxxxx"
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = "https://xxxxx.api.cognitive.microsoft.com/"
EOF
echo ""
echo "   - Replace with your actual keys"
echo "   - Click Save"
echo ""
echo "5. Refresh app and test:"
echo "   - Upload a test PDF"
echo "   - Verify processing works"
echo ""
echo "6. Share live URL:"
echo "   - https://[YOUR_USERNAME]-noticeflow.streamlit.app"
echo ""
echo "=================================================="
echo "✓ Git setup complete"
echo "✓ Ready for Streamlit Cloud deployment"
echo "=================================================="
