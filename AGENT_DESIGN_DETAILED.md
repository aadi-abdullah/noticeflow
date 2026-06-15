# Realistic Agent Design (Production-Ready Architecture)

## Part 0: Truth About Agents

**What you're NOT building:**
- Autonomous swarms
- Self-directed reasoning loops
- Recursive agent hierarchies
- LLM operating systems

**What you ARE building:**
- A **deterministic workflow engine** that dispatches LLM calls to specialized roles
- Each role is a **tool-using function**, not an autonomous creature
- Central orchestrator controls execution order
- Memory system provides context between steps

---

# Part 1: Core Architecture

```
                    WORKFLOW ORCHESTRATOR
                   (Deterministic Brain)
                    Controls everything
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   Planning           Execution            Memory
   Agents             Agents               System
        │                  │                  │
        └──────────────────┴──────────────────┘
                           │
                    ┌──────▼────────┐
                    │   TOOL LAYER  │
                    │ OCR / DB / RAG│
                    │ Rules Engine  │
                    └───────────────┘
```

**Key principle:** Orchestrator decides what happens next, not agents.

---

# Part 2: The 5 Agent Types (All You Need)

## 2.1 Planner Agent (Control Layer)

**Role:** Break down notice into processing steps

**Input:**
```json
{
  "ocr_text": "...",
  "notice_type": "unknown"
}
```

**Output:**
```json
{
  "steps": [
    "classify_notice",
    "extract_metadata",
    "interpret_notice",
    "generate_checklist"
  ],
  "risk_flags": ["deadline_critical", "missing_info"],
  "confidence": 0.95
}
```

**Important:**
- Suggests workflow, not executes it
- Orchestrator follows suggestion or overrides
- Returns as JSON only

**When to call:**
- Once per notice (start of pipeline)

---

## 2.2 Classification Agent

**Role:** Identify notice type and section

**Input:**
```json
{
  "ocr_text": "..."
}
```

**Output:**
```json
{
  "section": "122(5A)",
  "section_category": "audit_reassessment",
  "notice_type": "inquiry",
  "risk_level": "high",
  "confidence": 0.92
}
```

**Tools Available:**
- Tax section taxonomy (DB lookup)
- Pattern matching engine
- LLM for semantic understanding

**When to call:**
- After OCR
- Before extraction

---

## 2.3 Extraction Agent

**Role:** Pull structured facts from notice

**Input:**
```json
{
  "ocr_text": "...",
  "section": "122(5A)"
}
```

**Output:**
```json
{
  "tax_year": "2023-2024",
  "notice_date": "2024-06-10",
  "deadline": "2024-07-10",
  "authority": "FBR",
  "allegation_type": "profit_mismatch",
  "amount_in_dispute": "500000",
  "confidence": 0.94
}
```

**Tools Available:**
- Regex patterns (dates, amounts)
- LLM for semantic extraction
- Deadline rules engine

**When to call:**
- After classification
- Before interpretation

---

## 2.4 Interpretation Agent

**Role:** Convert legal text to plain language

**Input:**
```json
{
  "ocr_text": "...",
  "section": "122(5A)",
  "allegation_type": "profit_mismatch"
}
```

**Output:**
```json
{
  "summary": "FBR is questioning the declared profit margin",
  "what_fbr_wants": "Justification for 15% profit vs historical 25%",
  "why_issued": "Tax return shows profit below historical average",
  "consequences": "If not justified: assessment order + 50% penalty",
  "risk_level": "medium",
  "urgency": "high",
  "confidence": 0.89
}
```

**Tools Available:**
- Legal interpretation LLM
- Section explanation templates
- Risk scoring rules

**When to call:**
- After extraction
- Before checklist generation

---

## 2.5 Checklist Agent

**Role:** Generate required documents and actions

**Input:**
```json
{
  "section": "122(5A)",
  "allegation_type": "profit_mismatch",
  "interpretation": { ... }
}
```

**Output:**
```json
{
  "required_documents": [
    {
      "name": "Sales Ledger",
      "description": "Last 3 years sales records",
      "importance": "critical",
      "risk_if_missing": "FBR will estimate sales"
    },
    {
      "name": "Cost Ledger",
      "description": "Cost of goods sold details",
      "importance": "critical",
      "risk_if_missing": "Profit margin cannot be justified"
    }
  ],
  "supporting_documents": [
    {
      "name": "Market Analysis",
      "description": "If claiming market downturn",
      "importance": "supporting"
    }
  ],
  "next_steps": [
    "Collect financial records",
    "Calculate profit reconciliation",
    "Prepare written response"
  ],
  "confidence": 0.91
}
```

**Tools Available:**
- Knowledge Base (section → documents mapping)
- Past cases (RAG similarity search)
- Risk assessment rules

**When to call:**
- After interpretation
- Final step of core pipeline

---

## 2.6 (Optional) Drafting Agent

**Role:** Generate response structure template

**Constraint:** NEVER final output, always templated with placeholders

**Input:**
```json
{
  "section": "122(5A)",
  "allegation_type": "profit_mismatch",
  "documents_collected": true
}
```

**Output:**
```json
{
  "response_structure": [
    "introduction",
    "acknowledge_notice",
    "provide_facts",
    "justify_position",
    "submit_documents",
    "closing"
  ],
  "template": {
    "introduction": "This is response to notice dated ...",
    "acknowledge": "We acknowledge receipt of notice regarding ...",
    "facts": "[PASTE YOUR FACTS HERE]",
    "justification": "[EXPLAIN YOUR POSITION]",
    "documents": "Attached documents support our position",
    "closing": "We request favorable consideration"
  },
  "confidence": 0.85
}
```

**When to call:**
- ONLY after user confirms documents collected
- ONLY as optional Phase 3+ feature
- NOT in PoC or MVP

---

# Part 3: Tool Layer (How Agents Do Work)

Agents don't "think" in isolation. They use tools.

---

## 3.1 OCR Tool

```python
class OCRTool:
    def extract_text(file_path: str) -> str:
        """
        Try 1: Azure Document Intelligence
        Try 2: GPT-4o Vision
        Fallback: Simple PyPDF2
        """
        # Implementation
```

**When called:** Start of pipeline

---

## 3.2 Tax Knowledge Tool (RAG)

```python
class TaxKnowledgeTool:
    def get_section_rules(section: str) -> dict:
        """Return: {"documents": [...], "deadline_rule": "...", ...}"""
        
    def get_similar_cases(allegation_type: str) -> list:
        """RAG search for past cases"""
        
    def get_checklist_template(section: str) -> dict:
        """Documents typically required for this section"""
```

**When called:** Classification, Checklist generation

---

## 3.3 Deadline Rule Engine (Deterministic)

```python
class DeadlineEngine:
    RULES = {
        "122(5A)": lambda issue_date: issue_date + timedelta(days=30),
        "177": lambda issue_date: issue_date + timedelta(days=15),
        "161": lambda issue_date: issue_date + timedelta(days=60),
    }
    
    def calculate_deadline(section: str, issue_date: date) -> date:
        """Deterministic deadline calculation"""
```

**When called:** Extraction agent

---

## 3.4 Case Memory Tool

```python
class CaseMemoryTool:
    def store_result(client_id: str, notice: dict, result: dict):
        """Store in PostgreSQL"""
        
    def retrieve_client_history(client_id: str) -> list:
        """Get past notices for this client"""
        
    def find_similar_cases(allegation_type: str) -> list:
        """Vector search for similar cases"""
```

**When called:** Throughout pipeline, stored at end

---

## 3.5 Validation Tool (Schema)

```python
class ValidationTool:
    SCHEMAS = {
        "classification_output": {...},
        "extraction_output": {...},
        "interpretation_output": {...},
        "checklist_output": {...},
    }
    
    def validate(agent_name: str, output: dict) -> bool:
        """Verify output matches schema"""
```

**When called:** After every agent output

---

# Part 4: Memory Architecture

You need 3 memory layers:

---

## 4.1 Short-Term Memory (Working State)

Single JSON object passed through pipeline:

```python
class NoticeState:
    def __init__(self):
        self.notice_id = None
        self.uploaded_file = None
        self.ocr_text = ""
        
        # Agent outputs
        self.classification = {}      # From Classification Agent
        self.metadata = {}            # From Extraction Agent
        self.interpretation = {}      # From Interpretation Agent
        self.checklist = {}           # From Checklist Agent
        
        # Metadata
        self.created_at = None
        self.processing_time = None
        self.confidence_scores = {}
        self.errors = []
```

**Used by:** All agents (read + write)

---

## 4.2 Long-Term Memory (PostgreSQL)

```sql
-- Core tables

notices:
  - id (UUID)
  - client_id (for later)
  - raw_ocr_text
  - uploaded_file_path
  - created_at

notice_results:
  - notice_id (FK)
  - classification_json
  - metadata_json
  - interpretation_json
  - checklist_json
  - total_processing_time
  - created_at

case_history:
  - id (UUID)
  - client_id
  - notice_id (FK)
  - response_submitted (date)
  - outcome (assessment/closed/other)
  - notes
```

**Used by:** Case Memory Tool (store + retrieve)

---

## 4.3 Semantic Memory (Vector DB - Phase 3+)

```python
# Stores vectorized representations of:
# - Past notices (for similarity search)
# - Checklists (for template retrieval)
# - Responses (for drafting assistance)

class VectorMemory:
    def store_notice(notice: dict, embedding: list):
        """Store in pgvector or Pinecone"""
        
    def find_similar(query_embedding: list, top_k=5) -> list:
        """RAG: "What did we do in similar case?"
```

**Used by:** Checklist Agent (RAG search)
**Important:** Only add in Phase 3, after you have 50+ real notices

---

# Part 5: Orchestrator (The Brain)

This is NOT AI. This is deterministic code.

```python
class NoticeOrchestrator:
    def __init__(self):
        self.planner = PlannerAgent()
        self.classifier = ClassificationAgent()
        self.extractor = ExtractionAgent()
        self.interpreter = InterpretationAgent()
        self.checklist_gen = ChecklistAgent()
        self.validator = ValidationTool()
        self.memory = CaseMemoryTool()
    
    def process_notice(self, file_path: str) -> NoticeState:
        """Main execution method"""
        
        state = NoticeState()
        
        try:
            # Step 1: OCR
            print("Step 1: OCR extraction...")
            state.ocr_text = self._ocr_extract(file_path)
            if not state.ocr_text:
                raise ValueError("OCR failed")
            
            # Step 2: Get workflow plan
            print("Step 2: Planning workflow...")
            plan = self.planner.get_plan(state.ocr_text)
            state.workflow_plan = plan.steps
            
            # Step 3: Classification
            print("Step 3: Classification...")
            state.classification = self.classifier.classify(state.ocr_text)
            if not self.validator.validate("classification", state.classification):
                raise ValueError("Classification output invalid")
            
            # Step 4: Extraction
            print("Step 4: Metadata extraction...")
            state.metadata = self.extractor.extract(
                ocr_text=state.ocr_text,
                section=state.classification["section"]
            )
            if not self.validator.validate("extraction", state.metadata):
                raise ValueError("Extraction output invalid")
            
            # Step 5: Interpretation
            print("Step 5: Legal interpretation...")
            state.interpretation = self.interpreter.interpret(
                ocr_text=state.ocr_text,
                section=state.classification["section"],
                allegation=state.classification.get("allegation_type")
            )
            if not self.validator.validate("interpretation", state.interpretation):
                raise ValueError("Interpretation output invalid")
            
            # Step 6: Checklist Generation
            print("Step 6: Checklist generation...")
            state.checklist = self.checklist_gen.generate(
                section=state.classification["section"],
                allegation=state.classification.get("allegation_type"),
                interpretation=state.interpretation
            )
            if not self.validator.validate("checklist", state.checklist):
                raise ValueError("Checklist output invalid")
            
            # Step 7: Store in memory
            print("Step 7: Storing results...")
            self.memory.store_result(state)
            
            return state
            
        except Exception as e:
            state.errors.append(str(e))
            # Don't crash - return partial state with error flag
            return state
    
    def _ocr_extract(self, file_path: str) -> str:
        """Orchestrate OCR with fallbacks"""
        try:
            # Try 1: Azure
            return azure_ocr(file_path)
        except:
            try:
                # Try 2: GPT-4o Vision
                return gpt4o_vision(file_path)
            except:
                # Try 3: Simple PDF
                return pypdf_extract(file_path)
```

**Key principles:**
- Each step validates output before proceeding
- Errors are caught + logged, not silent
- State object carries context through pipeline
- No agent can skip steps
- No agent can call other agents directly

---

# Part 6: Sequential vs Graph Orchestration

---

## Model A: Sequential Pipeline (RECOMMENDED)

```
OCR → Classification → Extraction → Interpretation → Checklist
  ↓        ↓              ↓             ↓              ↓
State    State          State         State          State
```

**Advantages:**
- Deterministic (always same order)
- Easy to debug (each step independent)
- Production-safe (no loops)
- Fast to ship

**Disadvantages:**
- Less parallelizable
- Rigid structure

**Use when:** Building MVP + Phase 2

---

## Model B: Controlled Agent Graph (Advanced)

```
              Planner
                ↓
    ┌──────────┼──────────┐
    ▼          ▼          ▼
Classifier  Extractor  Interpreter
    └──────────┬──────────┘
               ▼
           Checklist
```

**Advantages:**
- Modular (can run in parallel)
- Scalable (add new agents later)
- Flexible (skip steps if needed)

**Disadvantages:**
- Harder to debug
- More complex orchestration
- requires graph execution engine

**Use when:** Phase 4+ with high notice volume

**DO NOT USE** for PoC or MVP. Stick to Sequential.

---

# Part 7: Control Mechanisms (Guardrails)

---

## 7.1 Schema Validation (CRITICAL)

Every agent output must match contract:

```python
SCHEMA_CLASSIFICATION = {
    "type": "object",
    "required": ["section", "risk_level", "confidence"],
    "properties": {
        "section": {"type": "string"},
        "risk_level": {"enum": ["low", "medium", "high"]},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1}
    }
}

def validate_output(agent_name: str, output: dict) -> (bool, str):
    schema = SCHEMAS.get(agent_name)
    try:
        jsonschema.validate(output, schema)
        return True, None
    except jsonschema.ValidationError as e:
        return False, f"Validation failed: {e.message}"
```

**Retry Logic:**
```python
if not is_valid:
    # Retry with correction prompt
    output = agent.retry_with_correction(
        original_output=output,
        error_message=error
    )
    # Validate again
```

---

## 7.2 Confidence Scoring + Fallback

```python
if state.metadata.get("confidence", 0) < 0.75:
    # Low confidence - flag for human review
    state.human_review_needed = True
    state.human_review_reason = "Low deadline extraction confidence"
    
    # Optional: Try fallback extraction
    alternate_deadline = self.deadline_engine.heuristic_fallback(
        ocr_text=state.ocr_text,
        section=state.classification["section"]
    )
    state.metadata["deadline_alt"] = alternate_deadline
```

---

## 7.3 Guardrails (Legal Safety)

```python
class Guardrails:
    @staticmethod
    def check_output(state: NoticeState) -> list:
        issues = []
        
        # Rule 1: Never claim legal certainty
        if "definitely" in state.interpretation.get("summary", "").lower():
            issues.append("Removed 'definitely' - use 'likely' instead")
        
        # Rule 2: Deadline must be future date
        deadline = state.metadata.get("deadline")
        if deadline < datetime.now().date():
            issues.append(f"Deadline {deadline} is in past - likely extraction error")
        
        # Rule 3: Never suggest auto-submission
        if "auto" in state.checklist.get("next_steps", []):
            issues.append("Removed auto-submission - human action required")
        
        return issues
```

---

# Part 8: Error Handling Strategy

---

## Silent Failures NOT Allowed

```python
def process_notice(file_path: str):
    try:
        # ... pipeline ...
    except Exception as e:
        # Log + flag for human review
        state.errors.append({
            "step": current_step,
            "error": str(e),
            "timestamp": now(),
            "requires_human_review": True
        })
        return state  # Return partial state, not crash
```

---

## Fallback Chain

```python
# If Primary Agent fails → Try Backup Agent → Manual mode

def robust_classification(ocr_text: str):
    try:
        # Primary: GPT-4o Classification Agent
        result = classifier_gpt4o.classify(ocr_text)
    except:
        try:
            # Backup: Pattern matching engine
            result = classifier_regex.classify(ocr_text)
        except:
            # Manual: Flag for human
            result = {"section": "unknown", "confidence": 0}
    
    return result
```

---

# Part 9: End-to-End Execution Flow

```
┌──────────────────────────────────────────────────┐
│ USER UPLOADS NOTICE                              │
└────────────────┬─────────────────────────────────┘
                 │
         ┌───────▼───────┐
         │ OCR EXTRACTION│
         │ (Multi-try)   │
         └───────┬───────┘
                 │
         ┌───────▼────────────┐
         │ PLANNER AGENT      │
         │ Suggests steps     │
         └───────┬────────────┘
                 │
         ┌───────▼────────────┐
         │ CLASSIFICATION     │
         │ Section + Risk     │
         └────────┬───────────┘
                  │
    ┌─────────────┴─────────────┐
    │ VALIDATE SCHEMA           │
    │ If invalid: Retry agent   │
    └─────────────┬─────────────┘
                  │
         ┌────────▼─────────┐
         │ EXTRACTION       │
         │ Dates + Facts    │
         └────────┬─────────┘
                  │
         ┌────────▼──────────┐
         │ VALIDATE          │
         │ Confidence check  │
         └────────┬──────────┘
                  │
         ┌────────▼──────────┐
         │ INTERPRETATION    │
         │ Plain language    │
         └────────┬──────────┘
                  │
         ┌────────▼──────────┐
         │ VALIDATE          │
         │ Guardrails check  │
         └────────┬──────────┘
                  │
         ┌────────▼──────────┐
         │ CHECKLIST         │
         │ Required docs     │
         └────────┬──────────┘
                  │
         ┌────────▼──────────┐
         │ VALIDATE          │
         │ Final schema      │
         └────────┬──────────┘
                  │
         ┌────────▼──────────┐
         │ STORE RESULT      │
         │ DB + Memory       │
         └────────┬──────────┘
                  │
         ┌────────▼──────────┐
         │ RETURN JSON       │
         │ → UI Display      │
         └───────────────────┘
```

---

# Part 10: Implementation Roadmap

---

## Phase 1 (MVP): PoC (Days 1-14)

Build:
- ✅ OCR Tool (simple)
- ✅ Classification Agent (prompt)
- ✅ Extraction Agent (prompt)
- ✅ Interpretation Agent (prompt)
- ✅ Checklist Agent (prompt)
- ✅ Basic orchestrator (sequential)
- ✅ Simple schema validation

Skip:
- ❌ Memory (just log results)
- ❌ Drafting Agent
- ❌ Sophisticated fallbacks
- ❌ Vector DB

---

## Phase 2: Persistence (Weeks 5-8)

Add:
- ✅ PostgreSQL storage
- ✅ Case History Tool
- ✅ Confidence-based flagging
- ✅ Simple error logging

---

## Phase 3: Semantic (Weeks 9-12)

Add:
- ✅ Vector DB (pgvector)
- ✅ RAG-based checklist
- ✅ Similar case retrieval

---

## Phase 4: Expansion (Week 13+)

Add:
- ✅ Drafting Agent (optional)
- ✅ Parallel agent graph
- ✅ Advanced guardrails
- ✅ Multi-agent fallbacks

---

# Part 11: The Fundamental Truth

Your system is NOT:

> "An autonomous multi-agent AI system making independent decisions"

Your system IS:

> "A deterministic workflow engine that dispatches to specialized LLM roles, each constrained by tools + schemas + guardrails"

**Why this matters:**

```
Autonomous agents = Unpredictable = Not shippable for legal domain
Deterministic pipeline = Debuggable = Production-safe

This is what makes it trustworthy.
```

---

# Part 12: What Gives You Real Moat

NOT:
- Agent sophistication
- Prompt engineering
- Model choice
- Code elegance

BUT:

> The orchestration of tax-domain knowledge into repeatable, validated workflows

Your competitive advantage is:
1. Curated tax knowledge base (hard to replicate)
2. Structured orchestration (not fancy, but reliable)
3. Real case history (data only you have)
4. Continuous learning (failures → rules → improvement)

---

# Part 13: Critical Implementation Principles

---

## 1. Local First

Develop locally with mock data before cloud deployment.

```python
# Mock mode for testing
if DEBUG_MODE:
    classification = {
        "section": "122(5A)",  # Fixed
        "risk_level": "high",
        "confidence": 0.95
    }
```

---

## 2. Deterministic Ordering

NEVER let agents decide execution order.

```python
# Good
steps = ["classify", "extract", "interpret", "checklist"]
for step in steps:
    execute_step(step)

# Bad
while not_done:
    agent.decide_next_step()  # ← No
```

---

## 3. Immutable State

Each agent gets state, doesn't modify it directly.

```python
# Good
new_state = classifier.process(state)

# Bad
classifier.process_in_place(state)  # ← No
```

---

## 4. Fail Fast, Log Everything

```python
if not valid:
    log_failure(step, error, state)
    raise Exception(f"Step {step} failed")  # Crash explicitly
    # Don't silently continue
```

---

## 5. No Infinite Loops

```python
max_retries = 3
for attempt in range(max_retries):
    try:
        result = agent.process(state)
        if valid(result):
            return result
    except:
        pass

# After max_retries, give up + flag for human
flag_for_human_review(state)
```

---

# Part 14: The Honest Assessment

If you follow this design:

✅ **You will have:**
- Debuggable system (errors are traceable)
- Shippable product (deterministic = safe)
- Scalable architecture (each agent independent)
- Trustworthy outputs (heavily validated)
- Real moat (knowledge base, not code)

❌ **You will NOT have:**
- Cutting-edge AI demos
- Viral Reddit posts about "agents"
- Research publications
- Arbitrary "intelligent" behavior

**But you will have:**
- A system that actually works
- Something CAs trust with real cases
- Foundation for scaling
- Something you can defend to users

---

# Part 15: Next Step

You now have:

1. ✅ Product definition (PRD)
2. ✅ Tech stack (FastAPI, Postgres, GPT-4o)
3. ✅ Team structure (You + Frontend + CA advisor)
4. ✅ 12-week roadmap (Ground truth → MVP → persistence → retention)
5. ✅ PoC design (14-day validation experiment)
6. ✅ Agent architecture (5 roles + orchestrator)

**What's next?**

Choose one path:

**Path A: Start PoC NOW**
- Build monolithic pipeline (all agents in one script)
- Don't worry about splitting agents yet
- Get real user validation by Week 2
- Refactor into proper agent structure in Phase 2

**Path B: Build Proper Structure First**
- Implement orchestrator + 5 agents
- Build validation + memory layer
- Then validate with CAs

**Recommendation:** Path A (PoC faster)

---

**You're ready to ship.**

The question is: do you want to start this week?

