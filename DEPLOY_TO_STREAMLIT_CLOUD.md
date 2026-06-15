# Deploy NoticeFlow MVP to Streamlit Cloud (Exact Steps)

## Overview
This guide walks you through deploying NoticeFlow to Streamlit Cloud in ~15 minutes, with validation and beta testing setup.

**End State:** Live at `https://<github-username>-noticeflow.streamlit.app`

---

# Part 1: Prerequisites (5 minutes)

## 1.1 What You Need
- [ ] GitHub account (free)
- [ ] Streamlit Community Cloud account (free, linked to GitHub)
- [ ] API keys (ready to paste):
  - `OPENAI_API_KEY` (GPT-4o access)
  - `AZURE_DOCUMENT_INTELLIGENCE_KEY` (optional but recommended)
  - `AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT` (optional but recommended)

## 1.2 Get API Keys

### OpenAI API Key (Required)
1. Go to https://platform.openai.com/api/keys
2. Click "Create new secret key"
3. Copy it (you won't see it again)
4. Keep it safe — add to clipboard temp file

### Azure Document Intelligence (Optional but Recommended)
1. Go to https://portal.azure.com
2. Create resource: "Document Intelligence"
3. Copy:
   - Endpoint (e.g., `https://eastus.api.cognitive.microsoft.com/`)
   - API Key (primary key)
4. Keep both ready

---

# Part 2: Prepare GitHub Repository (5 minutes)

## 2.1 Create GitHub Repository

1. Go to https://github.com/new
2. Fill in:
   - **Repository name:** `noticeflow` (lowercase, no spaces)
   - **Description:** "Tax notice triage tool for Pakistani accountants"
   - **Visibility:** Public (required for Streamlit Community Cloud)
3. **DO NOT** initialize with README (we have one)
4. Click "Create repository"

**Result:** Empty repo with SSH clone URL

---

## 2.2 Push Code to GitHub

### On Your Local Machine:

```bash
# Navigate to project folder
cd c:\Users\ok\Downloads\NoticeFlow

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: NoticeFlow MVP

- Streamlit UI with notice upload
- GPT-4o parsing engine
- OCR fallback chain (Azure/PyPDF2/GPT Vision)
- Document checklist generator
- Deadline extraction and urgency tracking

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/noticeflow.git

# Push to main branch
git branch -M main
git push -u origin main
```

**Verify:** Go to https://github.com/YOUR_USERNAME/noticeflow → files visible

---

## 2.3 Verify Files in GitHub

Make sure these are present:
```
✓ app.py
✓ process_notice.py
✓ requirements.txt
✓ .streamlit/secrets.toml          ← SHOULD NOT be visible (in .gitignore)
✓ README.md
✓ .gitignore                        ← Must be present
```

**Critical:** `.streamlit/secrets.toml` must NOT appear in repo (git history) — it's in .gitignore.

---

# Part 3: Deploy to Streamlit Cloud (3 minutes)

## 3.1 Connect to Streamlit Community Cloud

1. Go to https://share.streamlit.io
2. Sign up with GitHub (authorize app)
3. After auth, click "Create app"

---

## 3.2 Deploy Settings

**Fill in these fields:**

| Field | Value |
|-------|-------|
| GitHub account | YOUR_USERNAME |
| Repository | noticeflow |
| Branch | main |
| File path | app.py |
| App URL | (auto-generated) |

Click "Deploy"

**Result:** Streamlit starts building (watch logs)

---

## 3.3 Wait for Build to Complete

Streamlit will:
1. Clone your repo ✓
2. Install requirements ✓
3. Run app.py ✓

Watch the build logs. If errors appear → see Part 6 (Troubleshooting).

**Expected output:**
```
2025-XX-XX XX:XX:XX.XXX
   WARNING: The app is running in headless mode.
   App available at: https://YOUR_USERNAME-noticeflow.streamlit.app
```

---

# Part 4: Add Secrets to Streamlit Cloud (2 minutes)

Your app is now live, but needs API keys. Do NOT hardcode them in code.

## 4.1 Add Secrets via Streamlit Dashboard

1. Go to https://share.streamlit.io/your-workspace
2. Find your "noticeflow" app
3. Click three dots → "Settings"
4. Go to "Secrets"
5. Paste into the text area:

```toml
OPENAI_API_KEY = "sk-xxxxxxxxxxxx"
AZURE_DOCUMENT_INTELLIGENCE_KEY = "xxxxxxxxxxxxx"
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = "https://xxxxx.api.cognitive.microsoft.com/"
```

Replace with your actual keys.

Click "Save"

---

## 4.2 Verify Secrets Loaded

1. Refresh your app: https://YOUR_USERNAME-noticeflow.streamlit.app
2. Upload a test notice PDF
3. If it processes → secrets are loaded ✓

If you see "API key error":
- Check if secrets were saved correctly
- Wait 30 seconds and refresh
- Clear browser cache

---

# Part 5: Beta Testing Setup (Validation Protocol)

## 5.1 Create Beta Testing Checklist

Before inviting users, run this yourself:

### Local Validation (Before Going Live)

```markdown
# Pre-Launch Checklist (30 min)

## Upload Functionality
- [ ] Upload PDF (text-based) — processes in <30 seconds
- [ ] Upload PNG/JPG (scanned image) — processes in <30 seconds
- [ ] Upload low-quality WhatsApp screenshot — returns graceful error

## Data Extraction
- [ ] Deadline extracted correctly (compare to original)
- [ ] Section identified (e.g., "122" shows in results)
- [ ] Tax year shown
- [ ] Authority shown (FBR/IRIS)

## Explanation Quality
- [ ] Plain language explanation is understandable (not legal jargon)
- [ ] Risk level color coding matches urgency (red = <7 days)
- [ ] "What FBR is asking" section is clear

## Document Checklist
- [ ] Checklist items are relevant to section
- [ ] No generic advice ("collect all documents")
- [ ] Items are actionable

## Deadline Urgency
- [ ] Green (>14 days) — notice doesn't appear alarming
- [ ] Yellow (7-14 days) — notice appears moderately important
- [ ] Red (<7 days) — notice appears urgent
- [ ] Overdue (negative) — prominently flagged

## Error Handling
- [ ] Upload non-PDF/image → "Invalid file type" message
- [ ] Upload corrupted PDF → fallback OCR works or graceful error
- [ ] API key missing → "Configuration error" message (not crash)

## UI/UX
- [ ] Mobile phone (landscape): App is readable
- [ ] Mobile phone (portrait): App is readable
- [ ] Desktop: Layout is clean
- [ ] All buttons clickable and responsive

## Performance
- [ ] Page loads in <5 seconds
- [ ] Processing takes 15-25 seconds (Azure) or 20-30 (GPT fallback)
- [ ] No timeout errors
```

Run through this before launch.

---

## 5.2 Recruit Beta Users

Target: **3-5 Chartered Accountants** (small firms)

**Outreach template:**
```
Subject: Free tax notice triage tool — testing needed

Hi [Name],

I'm building a tool to convert tax notices into structured 
data (deadline, documents needed, plain explanation).

Takes 20 seconds. No signup required.

Would you be willing to test it on 3-5 real notices?
Your feedback will directly shape what we build next.

Try it: https://YOUR_USERNAME-noticeflow.streamlit.app

Let me know if you have questions.

[Your Name]
```

---

## 5.3 Beta Validation Metrics

When users test, track:

| Metric | Target | Question |
|--------|--------|----------|
| **Deadline Accuracy** | ≥80% | "Did the deadline match the notice?" |
| **Usefulness** | ≥2/3 "yes" | "Would you use this on your next notice?" |
| **Time Saved** | ≥5 min | "How much time did this save vs. manual review?" |
| **Re-upload Rate** | ≥70% | "Will you use it again?" |
| **Checklist Quality** | ≥70% "useful" | "Did the checklist save you time collecting docs?" |

**Success Criteria (Phase 1 → Phase 2 go/no-go):**
- ≥3/4 metrics met → **PROCEED to Phase 2**
- <2/4 metrics met → **ITERATE MVP (1-2 weeks)**

---

# Part 6: Common Issues & Fixes

## Issue: App shows "ModuleNotFoundError"

**Cause:** Package not in requirements.txt

**Fix:**
```bash
# Locally, add the package
pip install [package_name]

# Update requirements.txt
pip freeze > requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Add missing dependency"
git push
```

Streamlit auto-redeploys on push.

---

## Issue: "Invalid API key" or "API key not found"

**Cause:** Secrets not loaded or formatted wrong

**Fix:**
1. Go to Streamlit dashboard → Secrets
2. Ensure format is exactly:
   ```toml
   OPENAI_API_KEY = "sk-xxxxx"
   ```
   (NOT `OPENAI_API_KEY="sk-xxxxx"` — space after `=`)
3. Save and wait 30 seconds
4. Refresh app and try again

---

## Issue: OCR fails, returns "Unable to extract text"

**This is expected for:**
- Handwritten notices (not supported)
- Urdu-only text (Phase 2+ feature)
- Extremely low-quality scans

**For beta testing:**
- Use printed PDFs or high-quality scans (>150 DPI)
- Note: "OCR failed" message is correct — doesn't break system

---

## Issue: App times out after 60 seconds

**Cause:** Large file or slow API

**Fix:**
- For PDF files >10 MB: Compress before upload
- For users in slow regions: Streamlit Cloud has latency
- Azure Document Intelligence is faster than GPT Vision fallback

**User message:** "Processing takes longer with large files. Compress PDF if possible."

---

## Issue: Secrets visible in git history

**Critical security issue.**

**Fix:**
```bash
# If secrets were ever committed:
git log --oneline
# Find the commit with secrets
git revert [COMMIT_SHA]
# Or: git filter-branch (more complex)

# Immediately rotate all API keys:
# - OpenAI: Delete and recreate key
# - Azure: Regenerate key in portal
```

**Prevention:**
- Always check `.gitignore` includes `.streamlit/secrets.toml`
- Never paste actual keys into code or docs

---

# Part 7: Monitor & Iterate

## 7.1 Check App Health

Streamlit dashboard shows:
- **Runtime:** How long app has been live
- **Last deploy:** When code was last pushed
- **Activity:** How many users accessed
- **Logs:** Real-time error logs

Visit: https://share.streamlit.io/your-workspace

---

## 7.2 Collect User Feedback

Template form (share with beta users):

```
# NoticeFlow Beta Feedback

1. What FBR section/type was your notice?
   [ ] 114  [ ] 122  [ ] 177  [ ] Other: ___

2. Did the deadline extraction match your notice?
   [ ] Yes  [ ] No  [ ] Partially

3. Was the document checklist useful?
   [ ] Yes (saved time)
   [ ] Partially (missed some items)
   [ ] No (didn't need it)

4. Would you use this on your next notice?
   [ ] Definitely yes
   [ ] Maybe
   [ ] No

5. What's one thing that would make this 10x better?
   [Free text]

6. Any errors or crashes?
   [Free text]
```

---

## 7.3 Decision Point (Week 4)

| Outcome | Decision |
|---------|----------|
| ≥3/4 success metrics met | **GO**: Start Phase 2 (Notice History) |
| 2/4 metrics met | **ITERATE**: Debug, refine MVP (1-2 weeks) |
| <2/4 metrics met | **PIVOT**: Rethink value prop, investigate why |

See LAUNCH_STRATEGY.md for full decision framework.

---

# Part 8: Security Checklist (Pre-Public Launch)

Before sharing link widely, verify:

```markdown
# Pre-Public Launch Security

- [ ] No API keys in app.py or process_notice.py
- [ ] No API keys in git history (check: git log -p)
- [ ] .gitignore includes .streamlit/secrets.toml
- [ ] Secrets added via Streamlit dashboard (not .gitignore'd file)
- [ ] Disclaimer visible: "For assistance only, not legal advice"
- [ ] No permanent storage of user data (stateless MVP)
- [ ] No auto-submission or auto-send (manual only)
- [ ] Privacy policy link (or simple: "Your data is not stored")
- [ ] Terms of use link (or simple: "This is a beta tool, use at own risk")
```

If any unchecked, fix before sharing with users.

---

# Part 9: Quick Reference

## Deployment Timeline
```
Step 1: GitHub repo           ~5 min
Step 2: Deploy to Cloud       ~3 min
Step 3: Add secrets           ~2 min
Step 4: Validate locally      ~15 min
Step 5: Recruit beta users    ~1 day
Step 6: Collect feedback      ~1 week
Step 7: Make go/no-go decision ~30 min
```

**Total: 15 minutes to live, 1-2 weeks to validate**

---

## Troubleshooting Quick Links
- Streamlit docs: https://docs.streamlit.io
- GitHub help: https://docs.github.com
- OpenAI API status: https://status.openai.com
- Azure status: https://azure.status.microsoft.com/

---

## Live App URL
```
https://YOUR_USERNAME-noticeflow.streamlit.app
```

Replace `YOUR_USERNAME` with your GitHub username.

---

# Part 10: What's Next (After Validation)

### If MVP Succeeds (Proceed to Phase 2)
See PRODUCT_VISION.md + LAUNCH_STRATEGY.md for Phase 2 features:
- Notice history (save to local SQLite)
- Client tracking
- Multi-document support
- Timeline: 4-6 weeks

### If MVP Needs Refinement
Debug:
- Which metric failed most?
- Is deadline extraction the problem?
- Is checklist too generic?
- Is UI confusing?

Iterate for 1-2 weeks, then revalidate.

### If MVP Fundamentals Don't Work
Pivot:
- Do CAs actually want this?
- Is the problem different than assumed?
- Should we focus on a different notice type (e.g., Section 114 only)?

---

# End of Deployment Guide

**Status:** Ready to deploy

**Next:** Follow Part 1 → Part 4 sequentially.

**Questions?** Refer to README.md or TROUBLESHOOTING section above.

**Go live:** 15 minutes from now.
