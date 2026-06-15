# PoC Design & Execution Sprint (14 Days)

## Part 0: What You're Actually Testing

This is NOT software development.

This is a **hypothesis validation experiment**:

```
IF:   AI can extract + explain + checklist a real notice
      faster than manual interpretation

THEN: Professional will trust it enough to act on it

PROOF: At least 2/3 CAs say "I would use this again"
```

If this hypothesis is wrong → no product exists.
If it's right → everything else is just engineering.

---

# Part 1: Single Core Hypothesis

> "Structured AI extraction of tax notices reduces professional cognitive load enough that they trust and reuse the system."

---

## What This Means
NOT testing:
- AI coolness
- code quality
- architecture elegance
- UI design

Testing:
- Does output save time?
- Does output have zero critical errors?
- Would user act on this without major revision?

---

# Part 2: PoC Scope (ABSOLUTE BOUNDARIES)

## What Goes IN:
```
Single file upload:
  - PDF (native digital)
  - Image (JPG/PNG scanned)
```

## What Comes OUT (3 THINGS ONLY):

### Output 1: Structured Metadata
```json
{
  "section": "122",
  "tax_year": "2024-2025",
  "notice_date": "2024-06-01",
  "deadline": "2024-07-31"
}
```

### Output 2: Plain Explanation
```json
{
  "summary": "FBR is asking for explanation of profit difference",
  "what_fbr_wants": "Justification for 15% profit margin vs historical 20%",
  "risk_level": "medium",
  "consequences": "If not justified: penalty up to 50% of difference + interest"
}
```

### Output 3: Document Checklist
```json
{
  "required_documents": [
    "Sales ledger (last 3 years)",
    "Cost of goods ledger",
    "Profit & loss statement"
  ],
  "supporting_documents": [
    "Market analysis (if claiming market downturn)",
    "Quotes from suppliers (if claiming cost changes)"
  ],
  "missing_risks": [
    "If no sales ledger: cannot justify profit margin claim",
    "If no cost breakdown: FBR will estimate"
  ]
}
```

---

## What Does NOT Go In (CRITICAL):

```
❌ Login system
❌ User accounts
❌ Database
❌ History tracking
❌ Dashboard
❌ Email notifications
❌ Response drafting
❌ Client management
❌ Multi-user features
❌ Reminders
❌ Integration with FBR
```

**Why?** These hide whether the core idea works.

---

# Part 3: Architecture (Brutally Simple)

```
┌─────────────────────────────────────────┐
│         Streamlit UI (single page)      │
│  [Upload] → [Processing] → [Results]    │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│        Python Script (process_notice)   │
│  - OCR extraction                       │
│  - LLM prompt chain                     │
│  - JSON schema validation               │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│      LLM Layer (GPT-4o single model)    │
│  - Extract metadata                     │
│  - Generate explanation                 │
│  - Create checklist                     │
│  (all in ONE prompt chain)              │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│          OCR (GPT-4o Vision)            │
│  Fallback: Simple PyPDF2 if image       │
└─────────────────────────────────────────┘
```

That's it. No FastAPI. No database. No complex orchestration.

---

# Part 4: The Core Prompt (THIS IS YOUR PRODUCT)

## Single Combined Prompt to GPT-4o

```
You are a tax notice analyzer for Pakistani FBR (Federal Board of Revenue).

You will receive text extracted from a tax notice.

Your job:
1. Extract key metadata
2. Explain in plain language what FBR is asking
3. Generate a checklist of required documents

OUTPUT FORMAT (strict JSON):
{
  "metadata": {
    "section": "<FBR section number>",
    "tax_year": "<tax year in format YYYY-YYYY>",
    "notice_date": "<date extracted from notice>",
    "deadline": "<response deadline from notice>"
  },
  "explanation": {
    "summary": "<1 sentence what is this notice>",
    "what_fbr_wants": "<what specific information/justification FBR requests>",
    "risk_level": "<low|medium|high>",
    "consequences": "<what happens if not addressed>"
  },
  "checklist": {
    "required_documents": ["<doc1>", "<doc2>"],
    "supporting_documents": ["<doc1>", "<doc2>"],
    "missing_risks": ["<risk1>", "<risk2>"]
  }
}

RULES:
- Section must be valid FBR section (122, 177, 161, etc)
- Deadline must be actual date, not "30 days from notice"
- Risk level: high = legal/penalty risk, medium = compliance, low = informational
- Documents must be specific to allegation, not generic
- If unsure: say "Unclear" not invented information

NOTICE TEXT:
[OCR EXTRACTED TEXT WILL GO HERE]

Respond ONLY with valid JSON. No explanation.
```

---

## Critical Rules:
1. **Structured Output Only:** If response isn't valid JSON → system fails
2. **No Hallucination:** If unclear → output "Unclear" not guesses
3. **Section-Specific:** Checklist must match section type, not generic
4. **Date Accuracy:** Deadline is critical (≥90% accuracy required)

---

# Part 5: Success Criteria (MEASURABLE)

You are successful ONLY if:

## Criterion 1: Deadline Extraction Accuracy ≥90%
```
Test: Run on 10 notices with known deadlines
Pass: ≥9/10 deadlines correctly extracted
Fail: <9/10 → debug prompt + retry
```

## Criterion 2: Section Detection ≥80%
```
Test: Run on 10 notices with known sections
Pass: ≥8/10 sections correctly identified
Fail: <8/10 → add section reference to prompt
```

## Criterion 3: Checklist Usefulness ≥2/3 Users
```
Test: Show to 3-5 CAs
Ask: "Is this checklist what you would ask for?"
Pass: ≥2/3 say "yes" or "mostly yes"
Fail: <2/3 → list complaints, fix prompt
```

## Criterion 4: Response Time <30 seconds
```
Test: Run 5 times, measure end-to-end
Pass: All <30 seconds
Fail: Optimize OCR or LLM calls
```

## Criterion 5: Would Re-use? ≥2/3 Users
```
Test: After real usage
Ask: "Would you use this on your next notice?"
Pass: ≥2/3 say "yes"
Fail: Product doesn't solve problem → kill or pivot
```

---

# Part 6: Testing Protocol (EXACTLY FOLLOW THIS)

## Phase A: Internal Testing (Days 1-7)

### Day 1-3: Collect Real Notices
```
☐ Email 5 CAs you know
  "Can you send 2-3 anonymized tax notices?
   Testing AI analysis tool for feasibility."
☐ Collect into /test_notices folder
☐ Create spreadsheet:
    - file name
    - section
    - actual deadline
    - key allegation
    - expected documents
```

### Day 4-7: Build + Test Pipeline
```
☐ Create Python script (process_notice.py)
☐ Test OCR on each notice (compare to manual)
☐ Test LLM prompt on each notice
☐ Check JSON output validity
☐ Log failures + errors
```

### Success Gate
```
✓ IF all 10 notices produce valid JSON
  → Move to Phase B (CA testing)

✗ IF any produce invalid JSON
  → Fix prompt + retry
  → If still broken after 2 retries
    → Redesign prompt
```

---

## Phase B: CA Testing (Days 8-14)

### Day 8-10: Prepare Streamlit UI
```
☐ Build simple upload screen
☐ Add processing indicator
☐ Display results (formatted JSON)
☐ Add feedback buttons (helpful/not helpful)
```

### Day 11-12: Recruit Testers
```
☐ Contact 3-5 CAs
  "I built a tool that analyzes tax notices.
   Can you test it on one of your recent notices?
   30-min screen share, watch you use it."
☐ Schedule 30-min sessions
☐ Prepare observation form
```

### Day 13-14: Observation Sessions
```
For each CA:
  ☐ Have them upload their notice
  ☐ Watch silently (do NOT explain)
  ☐ After results, ask:
    - "Is this accurate?"
    - "Does this save you time?"
    - "Would you use this again?"
    - "What's wrong?"
  ☐ Log exact responses
  ☐ Screen record (if allowed)
```

---

# Part 7: Failure Logging (YOUR TRAINING DATA)

Create a spreadsheet for EVERY failure:

```
Notice ID | Issue | Type | Root Cause | Fix Applied
----------|-------|------|-----------|---------------
N001      | Deadline wrong | Extraction | Prompt didn't extract date format | Improved date parsing
N003      | Section unclear | Detection | Similar section numbers confused | Added section examples to prompt
N005      | Checklist generic | Generation | No allegation-specific rules | Added section-to-documents mapping
```

This becomes your **debug dataset** and later your **training data**.

---

# Part 8: What "Success" Actually Looks Like

### Good PoC Result:
```
CA1: "Hmm, this is close. I'd still verify, but it saves me reading through."
CA2: "Yes, this is what I would ask for."
CA3: "The explanation is confusing, but the documents are right."

→ 2/3 would reuse
→ Proceed to Phase 2
```

### Bad PoC Result:
```
CA1: "The deadline is completely wrong."
CA2: "The checklist is generic, not specific to this notice."
CA3: "I don't trust this at all."

→ 0/3 would reuse
→ Do NOT add features
→ Fix core pipeline or kill
```

---

# Part 9: What NOT to Do (COMMON MISTAKES)

## ❌ Mistake 1: Over-engineering
```
"Let me add a database so we can save results"
→ No. You're not validating persistence yet.
```

## ❌ Mistake 2: Premature Scaling
```
"Let me add authentication and multi-user"
→ No. You don't even know if product works.
```

## ❌ Mistake 3: Feature Creep
```
"Let me add response drafting, reminders, integration..."
→ No. Focus on ONE thing: does extraction work?
```

## ❌ Mistake 4: Too Much Testing
```
"I'll run 100 notices through before showing to CAs"
→ No. Show to CAs by day 11-12 max.
   You learn faster from live usage than batch testing.
```

## ❌ Mistake 5: Ignoring Failures
```
"The deadline was wrong but I'll fix it later"
→ No. Track it NOW. Patch prompt immediately.
   This is your learning signal.
```

---

# Part 10: Decision Tree (End of Day 14)

```
Did 2/3+ CAs say they would use it again?

├─ YES (≥2/3)
│  ✓ PoC VALIDATED
│  ✓ Proceed to Phase 2: Add persistence (DB)
│  ✓ You have product-market signal
│
└─ NO (<2/3)
   ├─ "Deadline is wrong"
   │  → Fix: Improve date parsing in prompt
   │  → Retry with 2 new CAs (add 3-5 days)
   │
   ├─ "Checklist is generic"
   │  → Fix: Add more section-specific rules
   │  → Retry with 2 new CAs
   │
   ├─ "Takes too long"
   │  → Fix: Optimize OCR pipeline
   │  → Retry with 2 new CAs
   │
   └─ Multiple issues
      → Does not solve core problem
      → Consider pivoting or killing
```

---

# Part 11: Day-by-Day Execution Checklist

## DAY 1 (Monday)
```
Morning:
  ☐ Create /test_notices folder
  ☐ Email 5 CAs for notice samples
  ☐ Prepare data collection spreadsheet
  
Afternoon:
  ☐ Collect first notices (hopefully at least 3)
  ☐ Anonymize PDFs
  ☐ Create test_cases.csv
```

## DAY 2 (Tuesday)
```
Morning:
  ☐ Receive more notices (target: 8-10)
  ☐ Complete test_cases.csv (section, deadline, etc)
  ☐ Review existing process_notice.py
  
Afternoon:
  ☐ Write/refine core prompt
  ☐ Test OCR on 1 notice
  ☐ Debug JSON schema
```

## DAY 3 (Wednesday)
```
Full Day:
  ☐ Test process_notice.py on all 10 notices
  ☐ Check JSON validity (all should be valid)
  ☐ Log any failures
  ☐ Fix prompt issues
  ☐ Target: 100% valid JSON output
```

## DAY 4-5 (Thursday-Friday)
```
Full Days:
  ☐ If failures from Day 3: iterate prompt
  ☐ Run full test suite again
  ☐ Compare outputs to ground truth
  ☐ Measure deadline accuracy %
  ☐ Measure section accuracy %
```

## DAY 6-7 (Saturday-Sunday - Optional)
```
If time:
  ☐ Refine based on test results
  ☐ Document failure patterns
  ☐ Prepare for UI work

If good progress:
  ☐ Rest, prepare for user testing
```

## DAY 8-10 (Monday-Wednesday)
```
Full Days:
  ☐ Build Streamlit UI
  ☐ Connect to process_notice.py
  ☐ Test end-to-end locally
  ☐ Deploy to Streamlit Cloud (optional for testing)
  ☐ Create feedback form
```

## DAY 11 (Thursday)
```
Morning:
  ☐ Contact 3-5 CAs
  ☐ Confirm sessions for Days 12-14
  ☐ Prepare observation form
  
Afternoon:
  ☐ First CA session (30-45 min)
  ☐ Observe + log responses
  ☐ Ask: "Would you use this again?"
```

## DAY 12 (Friday)
```
Morning:
  ☐ Second CA session
  ☐ Log responses
  ☐ Note any issues
  
Afternoon:
  ☐ Third CA session (if available)
  ☐ Compile early feedback
```

## DAY 13-14 (Saturday-Sunday)
```
Remaining sessions + Analysis:
  ☐ Complete final CA sessions (up to 5 total)
  ☐ Compile all feedback
  ☐ Measure:
    - Deadline accuracy %
    - "Would re-use" %
    - Common complaints
  ☐ Make GO/NO-GO decision
```

---

# Part 12: Output Artifacts (Keep These)

### By End of PoC, You Should Have:

```
1. test_cases.csv
   - All 10 notices with ground truth

2. process_notice.py (refined)
   - Tested, debugged, reliable

3. CORE_PROMPT.txt
   - Your production prompt (can reuse later)

4. failure_log.csv
   - Every mistake logged + fix applied
   
5. testing_observations.md
   - CA feedback + behavior notes
   
6. POC_RESULTS.md
   - Success metrics
   - Go/no-go decision
   - Next phase recommendation
```

These become your **knowledge base for Phase 2**.

---

# Part 13: The Real Output of PoC

NOT code.

NOT infrastructure.

This:

```
{
  "deadline_accuracy": "92%",
  "section_accuracy": "85%",
  "ca_reuse_intent": "4/5 yes",
  "response_time": "18 seconds",
  "feedback": [
    "Saves time on manual reading",
    "Deadline extraction is reliable",
    "Checklist needs more specificity for Section 177",
    "Would use on next notice"
  ],
  "decision": "GO → Phase 2: Add persistence"
}
```

This proves the hypothesis.

---

# Part 14: If PoC Fails

Don't add features.

Ask:

```
1. What specific output was wrong?
2. Is it a prompt issue or data issue?
3. Can it be fixed with better examples in prompt?
4. Can we narrow scope further?
```

Examples:

- "Deadline always wrong" → Add more date formats to prompt
- "Section confused" → Add FBR section reference guide to prompt
- "Checklist generic" → Add section-to-documents mapping to prompt
- "Takes 2+ minutes" → Switch to GPT-4o mini for testing

Don't give up on first failure.

But don't add "next" features either.

---

# Part 15: The Mindset (CRITICAL)

## NOT: "Building a Startup"

## IS: "Running an Experiment"

Experiments have:
- Clear hypothesis
- Measurable success criteria
- Timeline (14 days)
- Decision gate
- Failure protocol

You're NOT building for scale.

You're testing if the idea works.

If it doesn't: iterate or kill.

If it does: then build for real.

---

# Part 16: When You're Done (Day 14)

Make a decision:

```
✓ GO (2/3+ users would reuse)
  → Start Phase 2 immediately
  → Add database + persistence
  → Build FastAPI backend

✗ NO-GO (<2/3 users, can't fix)
  → Kill product or pivot
  → Don't waste more time
  
? UNCLEAR (improvements possible)
  → Fix top 3 issues
  → Retest with 2 new CAs
  → Decide by Day 21
```

No middle ground.

---

# FINAL CHECKLIST: Ready to Start?

```
☐ You have access to 10 real tax notices
☐ You can reach 5+ CAs for testing
☐ You have OpenAI API credits ($20+)
☐ You have 40-50 hours over next 14 days
☐ You understand: this tests ONE hypothesis
☐ You understand: if it fails, you iterate the prompt, not add features
☐ You're ready to kill the project if it doesn't work
☐ You have this roadmap printed and on your wall
```

All checked?

**Start tomorrow.**

---

**This PoC will tell you if NoticeFlow is real or fantasy.**

Everything before was preparation.

This is execution.

Let's go.
