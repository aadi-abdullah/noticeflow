# NoticeFlow Lite - Project Initialization Checklist

## Project Files Created ✅

- [x] **app.py** (10.7 KB)
  - Streamlit UI with file upload
  - Results display with color-coded urgency
  - Risk assessment and data quality warnings
  - Mobile-responsive layout
  
- [x] **process_notice.py** (17.5 KB)
  - Text extraction with fallback strategies (Azure → PyPDF2 → GPT-4o Vision)
  - Structured JSON parsing with GPT-4o
  - Error handling and validation
  - Logging for debugging

- [x] **requirements.txt**
  - streamlit
  - openai
  - azure-ai-documentintelligence
  - PyPDF2
  - Pillow

- [x] **.streamlit/secrets.toml**
  - Template for API keys
  - Add OPENAI_API_KEY (required)
  - Add AZURE_DOCUMENT_INTELLIGENCE_* (optional but recommended)

- [x] **README.md**
  - Quick start guide
  - Deployment instructions
  - Troubleshooting
  - API setup details

---

## Next Steps (Follow This Order)

### Step 1: Set Up API Keys (REQUIRED)
```bash
# Get your OpenAI API key from:
# https://platform.openai.com/account/api-keys
# 
# Then edit .streamlit/secrets.toml and fill in:
OPENAI_API_KEY = "sk-..."
```

### Step 2: Install Dependencies
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Step 3: Run Locally
```bash
streamlit run app.py
```

### Step 4: Test with a Sample Notice
- Upload a PDF or image of a tax notice
- Verify that extraction works
- Check if deadline is correct
- Review document checklist for accuracy

### Step 5: Deploy to Streamlit Cloud (Optional)
1. Push to GitHub (ensure .streamlit/secrets.toml is in .gitignore)
2. Go to share.streamlit.io
3. Connect your repo
4. Set secrets in the Streamlit Cloud dashboard
5. App deployed at `https://<username>-<repo>.streamlit.app`

---

## Key Features Implemented

✅ **PDF & Image Upload**
- Accepts PDF, PNG, JPG, JPEG
- Handles scanned documents (low quality)
- WhatsApp photos supported

✅ **OCR (Text Extraction)**
- Azure Document Intelligence (preferred for scans)
- PyPDF2 (for text-based PDFs)
- GPT-4o Vision (universal fallback)

✅ **Structured Data Extraction**
- Tax section (122(5A), 114, etc.)
- Tax year
- Deadline (with urgency color-coding)
- Plain-English explanation
- Document checklist (tailored by section)
- Risk level (low/medium/high)

✅ **Data Quality Indicators**
- Flags uncertain fields
- Never fabricates data
- User-friendly error messages

✅ **UI/UX**
- Instant processing feedback (spinner)
- Color-coded deadline urgency
- Risk assessment with reasoning
- Mobile-responsive design
- Professional styling

✅ **Error Handling**
- Graceful fallbacks for failed OCR
- Retry logic for API errors
- User-friendly error messages
- Logging for debugging

---

## How the App Works

```
1. User uploads tax notice (PDF or image)
                ↓
2. System extracts text using best-available OCR method
                ↓
3. GPT-4o parses extracted text with FBR-specific rules
                ↓
4. Structured JSON returned with:
   - Deadline (flagged by urgency)
   - Section & Tax Year
   - Allegations summary
   - Document checklist
   - Risk assessment
   - Uncertainty warnings
                ↓
5. App displays results in clear, actionable sections
```

---

## Processing Pipeline Details

### OCR Fallback Strategy
1. **Azure Document Intelligence** ← Fastest, best for scans
   - Superior handling of low-quality images
   - Preserves layout and structure
   
2. **PyPDF2** ← For text-based PDFs
   - Fast, no external API calls
   - Works for digital PDFs (not scans)
   
3. **GPT-4o Vision** ← Universal fallback
   - Works on any image
   - More token usage
   - Slower but reliable

### Parsing Engine
- **Model:** GPT-4o with JSON mode
- **System Prompt:** FBR-specific instructions
  - Cites exact sections (122, 114, 177, etc.)
  - Knows document requirements per section
  - Flags uncertain extractions
  - Never guesses or fabricates
  
- **Output:** Structured JSON with confidence tracking

---

## API Cost Estimate

### Per Notice
- Text extraction: $0.01–0.05 (depends on OCR method)
- GPT-4o parsing: $0.05–0.25 (depends on document length)
- **Total: ~$0.10–0.30 per notice**

### Monthly Budget Scenarios
| Budget | Notices/Month | Cost per Notice |
|--------|---------------|-----------------|
| $10    | ~30–100       | $0.10–0.30      |
| $50    | ~150–500      | $0.10–0.30      |
| $100   | ~300–1000     | $0.10–0.30      |

### Cost Optimization Tips
1. Use Azure Document Intelligence (not GPT Vision)
2. Limit PDF pages (app already does this)
3. Use bulk pricing for high volume

---

## Customization Ideas (Later Phases)

### Immediate (After MVP Validation)
- [ ] Add more FBR section templates
- [ ] Support Urdu text in notices
- [ ] Better deadline parsing for different date formats
- [ ] Export results as PDF/Excel

### Phase 2
- [ ] Save notice history per client
- [ ] Track notice status (draft, submitted, approved)
- [ ] Deadline reminders via email

### Phase 3
- [ ] Draft response generator
- [ ] Knowledge base of similar cases
- [ ] Client portal for document upload

### Phase 4
- [ ] Integration with accounting software
- [ ] Tax computation support
- [ ] Compliance verification

---

## Troubleshooting Quick Links

| Issue | Solution |
|-------|----------|
| "ModuleNotFoundError: openai" | Run: `pip install -r requirements.txt` |
| "OPENAI_API_KEY not found" | Check .streamlit/secrets.toml or set env var |
| App won't start | Verify Python 3.9+ installed |
| Document not read | Try clearer scan or JPG format |
| Slow processing | Normal (10–20s). Check internet speed. |
| JSON parsing error | Retry upload. If persists, check API quota. |

---

## Important Reminders

⚠️ **NEVER commit .streamlit/secrets.toml to GitHub**
```bash
# Add this to .gitignore:
.streamlit/secrets.toml
```

⚠️ **This tool is an ASSISTANT, not a replacement**
- Always verify extracted data against original notice
- Professional judgment is mandatory
- Not a substitute for legal/tax advice

✅ **Test with real notices before deploying**
- Try 3-5 sample notices locally
- Verify deadline extraction accuracy
- Review document checklist completeness

---

**Ready to go!** Start with Step 1 above. 🚀
