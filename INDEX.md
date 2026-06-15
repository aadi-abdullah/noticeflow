# NoticeFlow – Complete Project Index

## 📋 Document Map

This is your guide to every document in the NoticeFlow project. Start here.

---

## 🎯 START HERE (Choose Your Role)

### If you're a **Developer** (Ready to run code)
1. **QUICKSTART.md** – Install + run in 5 minutes
2. **app.py** – Read the UI code (well-commented)
3. **process_notice.py** – Read the parsing logic
4. **README.md** – Full reference

### If you're a **Product Manager** (Tracking requirements)
1. **PRD_ALIGNMENT.md** – PRD requirements ↔ implementation
2. **PRODUCT_VISION.md** – Long-term north star
3. **LAUNCH_STRATEGY.md** – MVP validation + roadmap

### If you're a **CA/User** (Testing the product)
1. **QUICKSTART.md** – Setup (ask your developer)
2. **README.md** → Troubleshooting section
3. **DEPLOYMENT_CHECKLIST.md** → "What to expect"

### If you're **Deploying to production**
1. **DEPLOYMENT_CHECKLIST.md** – Pre-launch checklist
2. **README.md** → Deployment section
3. **SETUP.md** → Detailed configuration

---

## 📚 Document Descriptions

### QUICKSTART.md (5 min read)
**Purpose:** Get the app running locally in 5 minutes
**Contains:**
- Virtual environment setup
- Dependency installation
- API key configuration
- First run commands
- Quick troubleshooting

**Read if:** You want to run the app today.

---

### README.md (15 min read)
**Purpose:** Complete reference for development, deployment, and troubleshooting
**Contains:**
- Project structure overview
- Local setup (detailed)
- API key setup (OpenAI + Azure)
- Deployment to Streamlit Cloud
- Performance notes
- Comprehensive troubleshooting
- Future roadmap

**Read if:** You're setting up for the first time or need detailed help.

---

### SETUP.md (10 min read)
**Purpose:** Structured initialization checklist
**Contains:**
- Step-by-step installation
- Pre-deployment verification
- File reference guide
- Usage examples
- Customization ideas

**Read if:** You're following a specific workflow checklist.

---

### PRD_ALIGNMENT.md (20 min read)
**Purpose:** Map every PRD requirement to implementation
**Contains:**
- All 14 PRD sections mapped to code
- Feature-by-feature validation
- Testing checklist
- How each goal is met
- What was intentionally excluded

**Read if:** You're validating that the MVP meets requirements.

---

### PRODUCT_VISION.md (25 min read)
**Purpose:** Strategic north star and 5-phase roadmap
**Contains:**
- Vision statement
- Core problem definition
- 5-phase evolution path (MVP → Phase 5)
- Success metrics aligned to vision
- Risk mitigation strategy
- How MVP enables future growth

**Read if:** You're planning the product's future direction.

---

### LAUNCH_STRATEGY.md (20 min read)
**Purpose:** Step-by-step guide to MVP validation and Phase 2+ planning
**Contains:**
- Pre-launch checklist
- MVP validation criteria (Week 1-4)
- Phase 2-5 feature breakdown with timeline
- Decision framework for new features
- Launch checklist
- Success playbook

**Read if:** You're launching the product or planning next phases.

---

### DEPLOYMENT_CHECKLIST.md (10 min read)
**Purpose:** Final pre-production verification
**Contains:**
- Complete file inventory
- PRD coverage matrix (14/14 sections)
- Technical implementation details
- Performance & cost estimates
- Pre-deployment checklist (20 items)
- Known limitations (intentional)
- Next steps

**Read if:** You're about to deploy to production.

---

## 🗂️ Code Files

### app.py (10.8 KB)
**Purpose:** Streamlit user interface
**Key Sections:**
- Lines 1-133: CSS styling (color-coded UI)
- Lines 136-166: Urgency level calculation
- Lines 169-193: Deadline display
- Lines 196-214: Uncertainty warnings
- Lines 217-388: Results display
- Lines 391-420: Main app logic
- Lines 425-427: Entry point

**To customize:**
- Colors: Edit CSS (lines 26-130)
- Text/copy: Search `st.markdown` or `st.metric`
- Layout: Adjust column widths in `display_results()`

---

### process_notice.py (17.5 KB)
**Purpose:** Core processing engine (OCR → parsing)
**Key Sections:**
- Lines 49-100: FBR system prompt (GPT-4o instructions)
- Lines 86-112: Azure Document Intelligence OCR
- Lines 115-147: PyPDF2 fallback OCR
- Lines 150-185: GPT-4o Vision fallback
- Lines 188-220: Raw text extraction orchestration
- Lines 357-378: GPT-4o JSON parsing
- Lines 385-425: Main orchestration function

**To customize:**
- System prompt: Edit `FBR_SYSTEM_PROMPT` (lines 49-100)
- Add new OCR method: Create function, add to `extract_raw_text()` fallback chain
- Change parsing model: Replace `gpt-4o` with `claude-3` (would need API changes)

---

### requirements.txt (103 B)
**Purpose:** Python dependencies
**Contains:**
- streamlit==1.39.0
- openai>=1.3.0
- azure-ai-documentintelligence>=1.0.0
- PyPDF2>=4.0.0
- Pillow>=10.0.0

**To modify:**
- Add new package: Add line with exact version
- Remove optional package: Comment out (e.g., Azure if not using)
- Update version: Change version number

---

### .streamlit/secrets.toml (1.2 KB)
**Purpose:** API keys template (NOT committed to git)
**Contains:**
- OPENAI_API_KEY = placeholder
- AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = placeholder
- AZURE_DOCUMENT_INTELLIGENCE_KEY = placeholder

**To use:**
- Fill in your actual keys
- Never commit to GitHub
- .gitignore already prevents this ✅

---

### .gitignore (303 B)
**Purpose:** Prevent committing secrets and build artifacts
**Contains:**
- venv/ (virtual environment)
- .streamlit/secrets.toml (API keys)
- __pycache__/ (Python cache)
- .env (local env files)
- .DS_Store, Thumbs.db (OS files)

**To modify:**
- Add new patterns as needed
- Standard patterns already included

---

## 🔑 Key Concepts

### The MVP Philosophy
```
Core: Upload → Extract → Display (nothing else)
No: Database, auth, storage, automation, multi-user
Why: Validates core value before premature scaling
Result: Production-ready ≠ feature-complete
```

---

### The OCR Fallback Chain
```
1. Azure Document Intelligence (preferred, best for scans)
   └─ Falls back to:
2. PyPDF2 (fast, for text-based PDFs)
   └─ Falls back to:
3. GPT-4o Vision (universal fallback, works on any image)
```

**Why:** Never fails. Always returns results (even if degraded).

---

### The Parsing Confidence Model
```
Extract all data → Mark uncertainty → Never guess
System: "I'm 80% confident on deadline, 40% on section"
User sees: Red flag for low-confidence fields
Not: "I think it might be..."
```

---

### The 5-Phase Roadmap
```
MVP (Now):        Upload → Extract → Display
Phase 2 (Month 3):  + History + Client tracking
Phase 3 (Month 6):  + Document coordination
Phase 4 (Month 12): + Response templates
Phase 5 (Month 18): + Multi-user firm OS
```

**Each phase unlocks the next** (not independent features).

---

## ✅ Validation Checklist

Before going live:

- [x] Code complete and documented
- [x] All PRD requirements met
- [x] Error handling in place
- [x] Logging configured
- [x] Security verified (no hardcoded keys)
- [ ] Tested with ≥3 real tax notices
- [ ] Deadline extraction verified
- [ ] Mobile responsiveness checked
- [ ] API costs estimated

---

## 🚀 Recommended Reading Order

### For First-Time Setup
1. QUICKSTART.md (5 min)
2. Run the app locally (10 min)
3. Test with a sample notice (10 min)
4. Read README.md Troubleshooting (if needed)

### For Deployment
1. DEPLOYMENT_CHECKLIST.md (10 min)
2. README.md → Deployment section (10 min)
3. Run pre-deployment checklist (5 min)
4. Deploy to Streamlit Cloud

### For Product Planning
1. PRD_ALIGNMENT.md (20 min) – Understand current MVP
2. PRODUCT_VISION.md (25 min) – Understand future direction
3. LAUNCH_STRATEGY.md (20 min) – Plan validation + phases

### For Extended Development
1. app.py (code read-through with comments)
2. process_notice.py (code read-through with comments)
3. README.md → Architecture section
4. Start building Phase 2

---

## 📞 FAQ

### Q: Can I modify the OCR method?
**A:** Yes. Edit `extract_raw_text()` in `process_notice.py`. It's designed for easy swaps.

### Q: What if deadline extraction is wrong?
**A:** Expected for now. MVP learns from user corrections (Phase 2+).

### Q: Can I add a database?
**A:** Yes, Phase 2 adds SQLite. Current MVP intentionally avoids this.

### Q: When do I add user accounts?
**A:** Phase 3+ (multi-user). MVP is single-session for simplicity.

### Q: Can I host this on my own server?
**A:** Yes. Docker setup needed (not included in MVP). Streamlit Cloud is simpler.

### Q: How do I track costs?
**A:** Monitor OpenAI API dashboard. Budget is ~$0.10-0.30 per notice.

---

## 📊 Project Statistics

| Metric | Count |
|--------|-------|
| Python Files | 2 (app.py, process_notice.py) |
| Configuration Files | 3 (.gitignore, requirements.txt, secrets.toml) |
| Documentation Files | 7 (README, SETUP, QUICKSTART, PRD_ALIGNMENT, PRODUCT_VISION, LAUNCH_STRATEGY, DEPLOYMENT_CHECKLIST) |
| Total Codebase | ~28 KB (focused, no bloat) |
| Total Documentation | ~50 KB (comprehensive) |
| Lines of Code (app.py) | ~427 |
| Lines of Code (process_notice.py) | ~456 |
| Code Comments | ~60 (clear explanations) |
| Docstrings | Every function has one |

---

## 🎯 Success Indicators

### MVP Success = When users ask
```
"Can you save my notices?" → Phase 2 trigger
"Can I track documents?" → Phase 2 insight
"Can clients upload docs?" → Phase 3 trigger
"Can you draft responses?" → Phase 4 trigger
```

### Product Success = When users say
```
"First thing I do is upload the notice"
(Instead of manually decoding it)
```

---

## 🔐 Important Reminders

1. **Don't commit secrets.toml** – .gitignore handles this ✅
2. **Always verify extractions manually** – Tool is assistant, not authority
3. **Test with real notices before promoting** – Accuracy matters
4. **Monitor API costs** – Budget $50/month for 150-500 notices

---

## 📈 Next Milestones

```
Week 1:   Deploy MVP
Week 2-4: Gather feedback from 3-5 CAs
Week 5:   Evaluate exit criteria
Week 6+:  Plan & execute Phase 2 (if metrics met)
```

---

**That's everything.** Choose a document above and start. Good luck! 🚀
