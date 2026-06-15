# NoticeFlow Lite - Project Documentation

## Project Structure

```
NoticeFlow-Lite/
├── app.py                    # Streamlit UI (main entry point)
├── process_notice.py         # Core processing logic (OCR + GPT-4o parsing)
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── secrets.toml         # API keys template (DO NOT COMMIT)
└── README.md                # This file
```

---

## Quick Start (Local Development)

### 1. Clone or download this project
```bash
cd NoticeFlow-Lite
```

### 2. Create and activate virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API keys
Copy `.streamlit/secrets.toml` template and fill in your credentials:

**Option A: Local testing (using .streamlit/secrets.toml)**
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Then edit with your actual keys
```

**Option B: Environment variables**
```bash
export OPENAI_API_KEY="your_key_here"
export AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT="your_endpoint"
export AZURE_DOCUMENT_INTELLIGENCE_KEY="your_key_here"
```

### 5. Run the app
```bash
streamlit run app.py
```

The app will be available at: `http://localhost:8501`

---

## API Key Setup

### OpenAI API (REQUIRED)

1. Go to https://platform.openai.com/account/api-keys
2. Create a new API key
3. Copy it to `.streamlit/secrets.toml` or set `OPENAI_API_KEY` env var

**Cost estimate:**
- Per notice: ~$0.10–0.30 (depending on document length)
- Monthly budget: $50 = ~150–500 notices

### Azure Document Intelligence (OPTIONAL but RECOMMENDED)

For better OCR performance on scanned documents:

1. Create an Azure account: https://portal.azure.com
2. Create "Document Intelligence" resource
3. Copy Endpoint and Key
4. Add to `.streamlit/secrets.toml`

If NOT configured, the app falls back to GPT-4o Vision (slower, higher token usage).

---

## Deployment to Streamlit Community Cloud

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit: NoticeFlow Lite"
git remote add origin <your-repo-url>
git push -u origin main
```

**Make sure `.streamlit/secrets.toml` is in `.gitignore`:**
```bash
echo ".streamlit/secrets.toml" >> .gitignore
git add .gitignore
git commit -m "Add secrets to gitignore"
git push
```

### Step 2: Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Click "New app"
3. Select your GitHub repo
4. Leave main file as `app.py`
5. Click "Deploy"

### Step 3: Set Secrets in Streamlit Cloud
1. After deployment, click "Settings" (⚙️ icon)
2. Go to "Secrets"
3. Paste your credentials:
```
OPENAI_API_KEY=sk-...
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=https://...
AZURE_DOCUMENT_INTELLIGENCE_KEY=...
```
4. Save and the app will auto-reload

---

## File Reference

### app.py
Main Streamlit interface.

**Key functions:**
- `main()` – Entry point, handles file upload
- `display_results()` – Renders extracted data
- `display_deadline()` – Color-coded urgency indicator
- `get_urgency_level()` – Calculates days to deadline

**Sections displayed:**
- Deadline (color-coded: green >14d, yellow 7-14d, red <7d)
- Tax section and year
- Plain-English explanation
- Document checklist
- Risk assessment
- Data quality warnings

---

### process_notice.py
Core processing engine.

**Main function:**
```python
process_notice(uploaded_file) -> Dict[str, Any]
```

**Processing pipeline:**
1. **Text Extraction** (one of three methods):
   - Azure Document Intelligence (preferred for scans)
   - PyPDF2 (for text-based PDFs)
   - GPT-4o Vision (fallback for images)

2. **Structured Parsing**:
   - Sends text to GPT-4o with FBR-specific system prompt
   - Returns JSON with: section, tax_year, deadline, checklist, risk_level, uncertainties

3. **Validation**:
   - Checks all fields are present and correct types
   - Fills in safe defaults if missing

**Key functions:**
- `extract_raw_text()` – OCR orchestration
- `extract_text_from_pdf_with_azure()` – Azure OCR
- `extract_text_with_gpt4_vision()` – Vision API fallback
- `parse_notice_with_gpt4()` – Structured extraction
- `validate_result()` – Output validation

---

## Usage Examples

### Example 1: Upload a PDF notice
```
User uploads: FBR_Notice_2024.pdf
↓
System extracts text (Azure → PyPDF2 → Vision)
↓
GPT-4o parses and returns:
{
  "section_cited": "122(5A)",
  "deadline": "2024-07-30",
  "risk_level": "high",
  "document_checklist": ["Bank statements", "Sales ledger", ...]
}
↓
App displays with red urgency indicator (3 days left)
```

### Example 2: Upload a WhatsApp photo
```
User uploads: notice_scan.jpg
↓
Azure Document Intelligence or GPT-4o Vision extracts text
↓
GPT-4o parses and returns structured data
↓
App displays results
```

---

## Error Handling

The app handles common failure scenarios:

| Error | Handling |
|-------|----------|
| Document unreadable | "The document could not be read. Please try a clearer scan." |
| API rate limit | Retry once, then user-friendly error |
| Invalid JSON from GPT-4o | Retry once, fallback response |
| Deadline not found | Shows warning, user must verify manually |
| Uncertain extraction | Displays "⚠️ Data Quality Notice" with details |

---

## Performance Notes

### Processing time
- Typical notice: 10–20 seconds (OCR + GPT-4o calls)
- First API call: May take 5–10 seconds for warm-up
- Depends on: PDF quality, document length, API latency

### Optimization tips
- Use Azure Document Intelligence for best OCR speed
- Limit PDF pages to first 5 (code already does this)
- Scanned documents may be slower than clean PDFs

### Cost optimization
- One notice ≈ $0.10–0.30 in API calls
- Monthly budget: $50 covers ~150–500 notices
- Consider caching for repeat clients (Phase 2)

---

## Troubleshooting

### App won't start
```bash
# Check dependencies
pip install -r requirements.txt

# Check API keys
echo $OPENAI_API_KEY  # Should print your key
```

### "Document could not be read"
- Try a clearer scan/photo
- Ensure PDF is not password-protected
- Try JPG instead of PNG

### API errors
- Check your OPENAI_API_KEY is valid
- Verify you have API credits
- Check rate limits: https://platform.openai.com/account/rate-limits

### Slow processing
- This is normal (10–20 seconds per notice)
- Azure OCR is faster than GPT-4o Vision
- Large PDFs take longer

---

## Future Roadmap

### Phase 2: Notice History
- Save user-uploaded notices
- Track extraction history per client
- Simple SQLite database

### Phase 3: Deadline Alerts
- Email/SMS reminders
- Centralized tracking for multiple clients

### Phase 4: Draft Response Generator
- Auto-generate draft FBR replies
- Reference past similar cases

### Phase 5: Legal/Tax Computation
- Integration with tax filing systems
- Automated compliance checks

---

## Legal Notice

**NoticeFlow Lite** provides extraction and parsing assistance only.

✅ **Use it for:**
- Quick triage of incoming notices
- Organizing initial document requirements
- Assigning priority to notices

❌ **Do NOT use it for:**
- Final legal or tax decisions
- Auto-submission to FBR
- Replacing professional judgment

**Always verify extracted information against the original notice. Professional judgment and legal review are mandatory before responding to any FBR notice.**

---

## Support

For issues or feature requests:
1. Check the troubleshooting section above
2. Verify all API keys are correct
3. Test with a sample notice (see Examples)
4. Open an issue on GitHub

---

**Last Updated:** June 2024  
**Version:** 1.0 (MVP)
