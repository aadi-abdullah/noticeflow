# NoticeFlow Data Strategy & Knowledge Base Design

## Part 0: Why This Matters (The Real Moat)

Your competitive advantage is NOT:
- ❌ Using GPT-4o (anyone can)
- ❌ Streamlit UI (anyone can)
- ❌ Workflow pipeline (anyone can copy)

Your competitive advantage IS:
- ✅ **Curated FBR notice dataset** (nobody else has this)
- ✅ **Section → behavior mappings** (built from real CA workflows)
- ✅ **Document checklists verified by accountants** (not AI guessing)
- ✅ **Failure case library** (what went wrong + how to fix)

This becomes your **"proprietary knowledge graph of how tax professionals actually work"**.

---

# Part 1: Data Architecture (What Gets Stored Where)

## Three-Layer System

```
┌─────────────────────────────────────────┐
│ Layer 1: Raw Data                       │
│ ├─ Original PDFs/images                 │
│ ├─ OCR text outputs                      │
│ └─ User metadata                        │
├─────────────────────────────────────────┤
│ Layer 2: Structured Knowledge Base       │
│ ├─ Section registry (what each section  │
│ │   legally means)                      │
│ ├─ Document rules (what docs required   │
│ │   per section)                        │
│ ├─ Deadline rules (how many days per    │
│ │   section type)                       │
│ └─ Response templates                   │
├─────────────────────────────────────────┤
│ Layer 3: Vector/Semantic Layer          │
│ ├─ Similar notice embeddings            │
│ ├─ Legal text similarity search         │
│ └─ Workflow pattern vectors             │
└─────────────────────────────────────────┘
```

---

## Why Three Layers?

- **Layer 1:** Auditability + compliance
- **Layer 2:** Deterministic behavior (rules always work)
- **Layer 3:** Intelligent retrieval (find similar cases)

---

# Part 2: Database Schema (Postgres + SQLite)

## 2.1 Core Tables (Phase 2 Implementation)

### notices

```sql
CREATE TABLE notices (
  id UUID PRIMARY KEY,
  user_id VARCHAR(255),  -- CA identifier (no auth yet)
  raw_notice_path VARCHAR(512),  -- S3 or local path
  ocr_text TEXT,  -- extracted text
  extracted_json JSONB,  -- structured extraction
  
  -- Curated ground truth (filled manually by CA validation)
  section VARCHAR(20),
  tax_year VARCHAR(10),
  notice_date DATE,
  deadline DATE,
  notice_type VARCHAR(50),
  
  -- Quality tracking
  ocr_confidence_score FLOAT,
  deadline_verified BOOLEAN,
  checklist_verified BOOLEAN,
  
  -- Metadata
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  tags JSONB -- ["misclassified", "edge_case", "test_data"]
);

CREATE INDEX idx_notices_section ON notices(section);
CREATE INDEX idx_notices_deadline ON notices(deadline);
CREATE INDEX idx_notices_verified ON notices(deadline_verified);
```

---

### document_checklists

```sql
CREATE TABLE document_checklists (
  id UUID PRIMARY KEY,
  notice_id UUID REFERENCES notices(id),
  
  -- What was needed
  required_documents JSONB,  -- structured list
  
  -- What was provided
  documents_collected JSONB,
  
  -- CA validation
  ca_feedback TEXT,
  was_complete BOOLEAN,  -- did CA find missing docs?
  missing_docs JSONB,  -- what was missed by system
  
  created_at TIMESTAMP
);
```

---

### section_registry (THE KNOWLEDGE BASE)

```sql
CREATE TABLE section_registry (
  section_code VARCHAR(20) PRIMARY KEY,
  category VARCHAR(100),  -- "audit", "demand", "compliance"
  
  -- What's it for?
  legal_intent TEXT,
  typical_triggers JSONB,
  
  -- Procedural knowledge
  default_response_days INTEGER,
  extensions_possible BOOLEAN,
  
  -- Risk classification
  risk_level VARCHAR(20),  -- "low", "medium", "high"
  
  -- Standard requirements
  required_documents JSONB,
  typical_amount_fields JSONB,  -- what amounts are usually mentioned
  
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

---

### response_templates (THE HIDDEN MOAT)

```sql
CREATE TABLE response_templates (
  id UUID PRIMARY KEY,
  section_code VARCHAR(20) REFERENCES section_registry(section_code),
  
  -- Template structure
  structure_outline JSONB,  -- ["intro", "notice_ref", "point_by_point", "docs", "closing"]
  sample_intro_paragraph TEXT,
  point_format TEXT,  -- how to structure each response point
  
  -- Example responses (real CAs)
  example_response TEXT,
  example_meta JSONB,  -- who submitted, approval status
  
  created_by VARCHAR(100),  -- which CA firm contributed this
  approved_by VARCHAR(100),
  
  created_at TIMESTAMP
);
```

---

### failure_cases (CRITICAL FOR LEARNING)

```sql
CREATE TABLE failure_cases (
  id UUID PRIMARY KEY,
  notice_id UUID REFERENCES notices(id),
  
  failure_type VARCHAR(100),  -- "wrong_deadline", "missing_doc", "misclassified_section"
  expected_value VARCHAR(255),  -- what it should have been
  system_output VARCHAR(255),  -- what system said
  
  root_cause TEXT,  -- why it failed
  fix_applied TEXT,  -- how we fixed it
  
  reported_by VARCHAR(100),  -- which CA found it
  created_at TIMESTAMP
);

CREATE INDEX idx_failures_type ON failure_cases(failure_type);
```

---

## 2.2 Vector Layer (Phase 3+)

```sql
CREATE TABLE notice_embeddings (
  id UUID PRIMARY KEY,
  notice_id UUID REFERENCES notices(id),
  
  embedding VECTOR(1536),  -- OpenAI embeddings dimension
  embedding_model VARCHAR(50),  -- "text-embedding-3-small"
  
  -- What was embedded
  text_segment TEXT,  -- which part of notice
  segment_type VARCHAR(50),  -- "full_notice", "allegations", "timeline"
  
  created_at TIMESTAMP
);

CREATE INDEX idx_embeddings_notice ON notice_embeddings(notice_id);
```

---

# Part 3: Knowledge Base Content (What to Populate)

## 3.1 Section Registry Data

This is YOUR competitive advantage. Curate this carefully:

```json
{
  "section_code": "122(5A)",
  "category": "audit_reassessment",
  
  "legal_intent": "FBR is questioning taxpayer's declared income. Asking for verification.",
  "typical_triggers": [
    "Income mismatch with third-party data",
    "Suspicious transactions detected",
    "Low FBR confidence in filed returns",
    "Prior year discrepancies"
  ],
  
  "default_response_days": 30,
  "extensions_possible": true,
  "max_extensions": 2,
  
  "risk_level": "high",
  
  "required_documents": [
    {
      "name": "Bank statements (12 months)",
      "why": "Verify income sources",
      "category": "financial",
      "if_missing": "risk_very_high"
    },
    {
      "name": "Sales ledger",
      "why": "Reconcile business income",
      "category": "financial",
      "if_missing": "risk_high"
    },
    {
      "name": "Purchase invoices",
      "why": "Substantiate expenses",
      "category": "financial",
      "if_missing": "risk_medium"
    },
    {
      "name": "WHT certificates",
      "why": "Prove tax withholding",
      "category": "compliance",
      "if_missing": "risk_medium"
    }
  ],
  
  "common_allegations": [
    "Income not matching expense claims",
    "Undisclosed sources of funds",
    "Related party transactions"
  ]
}
```

**Where does this come from?**
1. FBR Ordinance (manual research)
2. CA forum discussions (what they say works)
3. Past notices from beta CAs (what actually happened)

**NOT from:** ChatGPT hallucinations, random PDF embeddings

---

## 3.2 Document Checklist Rules

```json
[
  {
    "section": "122(5A)",
    "notice_type": "audit",
    "allegation_keywords": ["income", "sales"],
    "required_docs": [
      "bank_statements_12m",
      "sales_ledger",
      "purchase_invoices",
      "wht_certificates"
    ]
  },
  {
    "section": "122(5A)",
    "notice_type": "audit",
    "allegation_keywords": ["foreign", "remittance"],
    "required_docs": [
      "remittance_proofs",
      "foreign_account_docs",
      "exchange_rate_records"
    ]
  }
]
```

---

## 3.3 Response Template Library

```json
{
  "section": "122(5A)",
  "structure": {
    "intro": {
      "template": "We acknowledge receipt of your notice dated [DATE]. We respectfully submit our response as follows:",
      "tone": "professional, acknowledging"
    },
    "notice_reference": {
      "template": "Reference: Notice under Section 122(5A), tax year [YEAR], taxpayer reference [REF]",
      "tone": "factual"
    },
    "point_by_point": {
      "structure": [
        "Allegation: [FROM NOTICE]",
        "Our Response: [FACTUAL REBUTTAL]",
        "Supporting Evidence: [DOCUMENTS ENCLOSED]"
      ],
      "tone": "professional, fact-based"
    },
    "documents_section": {
      "template": "Please find attached the following documents supporting our response: [LIST]",
      "format": "bulleted list"
    },
    "closing": {
      "template": "We request a meeting to discuss if required. We remain available for any clarifications.",
      "tone": "cooperative"
    }
  }
}
```

---

# Part 4: Data Collection Protocol (How to Build the KB)

## 4.1 Phase 1: Manual Curation (Weeks 1-2)

### Step 1: Collect Real Notices

**Target: 10-20 notices**

From:
- Your contacts (CAs you know)
- IRIS download samples
- FBR case studies

Format: PDFs preferred, images acceptable

---

### Step 2: Manual Tagging (THE IMPORTANT PART)

For each notice, document:

```yaml
Notice ID: NTC_001
Source: Real CA (anonymized)
---

EXTRACTION GROUND TRUTH (human verified):
  Section: 122(5A)
  Tax Year: 2023-24
  Issue Date: 2025-01-15
  Deadline: 2025-02-14
  Notice Type: Audit Reassessment
  Taxpayer Ref: NTN-XXXXX

ALLEGATIONS (what FBR is actually asking):
  - Income declared vs. reconciled
  - Bank statement analysis
  - WHT certificate verification

REQUIRED DOCUMENTS (CA confirmed):
  - Bank statements (12 months)
  - Sales ledger
  - Purchase invoices
  - WHT certificates
  - Tax returns (last 3 years)

DOCUMENTS NOT NEEDED (avoid waste):
  - Personal tax records
  - Unrelated business docs

CA NOTES:
  "This is straightforward audit. Timeline is tight. Need docs within 2 weeks."
```

---

### Step 3: Create Ground Truth JSON

```json
{
  "notice_id": "NTC_001",
  "ground_truth": {
    "section": "122(5A)",
    "tax_year": "2023-24",
    "deadline": "2025-02-14",
    "required_documents": [
      "bank_statements_12m",
      "sales_ledger",
      "purchase_invoices",
      "wht_certificates"
    ]
  },
  "ocr_performance": {
    "deadline_extraction_correct": true,
    "section_extraction_correct": true,
    "confidence": 0.92
  },
  "system_performance": {
    "deadline_match": true,
    "section_match": true,
    "document_recall": 1.0
  }
}
```

**Do this for all 10-20 notices.**

This is your **evaluation set**.

---

## 4.2 Phase 2: Use Ground Truth for LLM Training

Once you have 10+ verified notices:

1. Use them to test prompts
2. Measure accuracy (deadline extraction, section detection, document recommendations)
3. Refine system prompt based on failures
4. Store failures in `failure_cases` table

---

## 4.3 Phase 3: Build KB from Patterns

After 50+ notices:

1. Extract common patterns
2. Add to `section_registry`
3. Create templates in `response_templates`
4. Document edge cases

---

# Part 5: RAG Architecture (When to Use What)

## 5.1 What Should Be Rules (Always Fast)

```python
# Use deterministic rules for:
if section == "122":
    deadline = issue_date + timedelta(days=30)
    required_docs = ["bank_statements", "sales_ledger", ...]

# NOT embeddings
# NOT "let LLM figure it out"
```

---

## 5.2 What Should Be Structured Query

```python
# Find section rules:
section_data = db.query(
    "SELECT * FROM section_registry WHERE section_code = ?",
    [section]
)

# Retrieve document requirements:
docs = db.query(
    "SELECT required_documents FROM document_checklists 
     WHERE section = ? AND allegation_type ILIKE ?",
    [section, "%" + allegation_keyword + "%"]
)
```

---

## 5.3 What Should Be Vector Search (Only for Insights)

```python
# Find SIMILAR past notices:
similar = embeddings.search(
    "notices with similar allegations",
    top_k=3
)

# Retrieve response template ideas:
templates = embeddings.search(
    "response templates for income reconciliation",
    top_k=5
)
```

**NOT for extraction. Only for context.**

---

# Part 6: Data Collection Template (How to Get CAs Contributing)

## 6.1 Simple Form for CAs

You send this to beta CAs:

```markdown
# Notice Submission Form

Please share a **recent tax notice** you handled. We'll use this to improve our system.

**Notice Details:**
- Section: ___________________
- Tax year: __________________
- Date received: _____________
- Deadline: __________________
- Notice type: [ ] Audit [ ] Demand [ ] Show Cause [ ] Other

**What FBR Asked For:**
List the main allegations/questions:
1. _________________________
2. _________________________
3. _________________________

**Documents You Had to Collect:**
- [ ] Bank statements
- [ ] Sales ledger
- [ ] Purchase invoices
- [ ] WHT certificates
- [ ] Tax returns
- [ ] Other: _______________

**Documents You Didn't Need (but system might suggest):**
_________________________________

**Response Timeline:**
- Days to collect docs: ___
- Days to prepare response: ___
- Total days used: ___

**Feedback:**
What did our system get right?
What did it miss?
```

---

## 6.2 How to Incentivize

```
For each notice submitted:
- You get "beta access" to improved features first
- Your firm name listed as contributor (optional)
- Early access to Phase 2 (history tracking)
```

---

# Part 7: Data Quality Gates (Non-Negotiable)

## 7.1 Before Adding to KB

```
Every piece of knowledge must pass:

☐ Legal accuracy review
  (Did we interpret the ordinance correctly?)

☐ Practitioner validation
  (Did at least one CA confirm this?)

☐ Consistency check
  (Does this conflict with other rules?)

☐ Completeness check
  (Is there missing information?)

☐ Edge case documentation
  (What exceptions exist?)
```

---

## 7.2 Failure Tracking (CRITICAL)

Whenever system gets something wrong:

```python
db.execute("""
  INSERT INTO failure_cases (
    notice_id,
    failure_type,
    expected_value,
    system_output,
    root_cause
  ) VALUES (?, ?, ?, ?, ?)
""", [
    notice_id,
    "wrong_deadline",
    "2025-02-14",
    "2025-03-14",
    "Section 122 assumed 60 days, actually 30 days"
])
```

These become:
1. Prompt refinement data
2. Test cases
3. KB improvements

---

# Part 8: Implementation Roadmap

## MVP (Now - Week 2)
```
✓ Deploy Streamlit
✓ Beta test with real CAs
✓ Collect raw notices
```

## Phase 2 (Week 3-4)
```
✓ Build database schema (notices table)
✓ Manually tag 10-20 notices
✓ Create section_registry (minimal: 6 sections)
✓ Build first failure_cases log
```

## Phase 3 (Week 5-6)
```
✓ Add persistence (save notices to DB)
✓ Expand section_registry (20+ sections)
✓ Build document_checklists validation
✓ Create response_templates (Phase 4+ feature)
```

## Phase 4+ (Month 3+)
```
✓ Add vector embeddings
✓ Build RAG retrieval
✓ Add similar-case suggestions
```

---

# Part 9: The Real Moat (Summary)

Your competitive advantage:

**NOT:** "We use AI"

**NOT:** "We process PDFs"

**YES:** 

> "We have the curated dataset of how professional accountants actually handle FBR notices"

---

## This Means

You will have:
1. Verified ground-truth on 200+ real notices
2. Structured KB of FBR section behavior
3. Library of response templates (from real CAs)
4. Failure case database (where systems usually break)

Nobody else can replicate this quickly.

---

# Part 10: What to Do Next

**Three options:**

## Option A: Start collecting data now
- Ask 5-10 beta CAs for real notices
- Manually tag them this week
- Use as evaluation set for Phase 2

## Option B: Build the schema first
- Create Postgres database
- Implement tables
- Get ready to populate

## Option C: Hybrid (recommended)
- Run MVP (already done)
- Collect 10 notices from beta users (Week 1-2)
- Build schema + tag manually (Week 3-4)
- Go live with persistence in Phase 2

---

**Which path appeals to you?**

The question is not "should we build this?"

The question is: **"When do we start building the moat?"**
